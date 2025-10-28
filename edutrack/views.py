from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Assignment, StudentRepo, AnalysisLog
from .api.github_handler import GitHubHandler
from .api.gemini_handler import GeminiHandler
from datetime import datetime


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """Main dashboard view"""
    assignments = Assignment.objects.filter(teacher=request.user)
    
    # Calculate statistics
    total_assignments = assignments.count()
    total_repos = StudentRepo.objects.filter(assignment__teacher=request.user).count()
    analyzed_repos = StudentRepo.objects.filter(assignment__teacher=request.user, is_analyzed=True).count()
    
    context = {
        'assignments': assignments[:5],  # Latest 5 assignments
        'total_assignments': total_assignments,
        'total_repos': total_repos,
        'analyzed_repos': analyzed_repos,
        'pending_analysis': total_repos - analyzed_repos,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def assignment_list(request):
    """List all assignments"""
    assignments = Assignment.objects.filter(teacher=request.user)
    return render(request, 'assignment_list.html', {'assignments': assignments})


@login_required
def assignment_detail(request, assignment_id):
    """View assignment details and student repos"""
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    repos = StudentRepo.objects.filter(assignment=assignment)
    
    context = {
        'assignment': assignment,
        'repos': repos,
    }
    
    return render(request, 'assignment_detail.html', context)


@login_required
def assignment_create(request):
    """Create new assignment"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        
        assignment = Assignment.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            deadline=datetime.fromisoformat(deadline) if deadline else None
        )
        
        messages.success(request, f'Assignment "{title}" created successfully!')
        return redirect('assignment_detail', assignment_id=assignment.id)
    
    return render(request, 'assignment_create.html')


@login_required
def add_student_repo(request, assignment_id):
    """Add student repository to assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        repo_url = request.POST.get('repo_url')
        
        # Check if repo already exists
        if StudentRepo.objects.filter(assignment=assignment, repo_url=repo_url).exists():
            messages.warning(request, 'This repository is already added to the assignment.')
            return redirect('assignment_detail', assignment_id=assignment.id)
        
        # Create repo entry
        repo = StudentRepo.objects.create(
            assignment=assignment,
            student_name=student_name,
            repo_url=repo_url
        )
        
        messages.success(request, f'Repository for {student_name} added successfully!')
        return redirect('assignment_detail', assignment_id=assignment.id)
    
    return render(request, 'add_repo.html', {'assignment': assignment})


@login_required
@require_POST
def analyze_repo(request, repo_id):
    """Analyze a repository using GitHub and Gemini APIs"""
    repo = get_object_or_404(StudentRepo, id=repo_id, assignment__teacher=request.user)
    
    try:
        # Create analysis log
        log = AnalysisLog.objects.create(repo=repo, status='pending')
        
        # Fetch GitHub data
        github_handler = GitHubHandler()
        github_data = github_handler.fetch_repo_data(repo.repo_url)
        
        if not github_data.get('success'):
            log.status = 'failed'
            log.error_message = github_data.get('error', 'Unknown error')
            log.save()
            return JsonResponse({'success': False, 'error': github_data.get('error')})
        
        # Update repo with GitHub data
        repo.commit_count = github_data.get('commit_count', 0)
        repo.languages = github_data.get('languages', {})
        repo.readme_content = github_data.get('readme_content', '')
        
        last_commit = github_data.get('last_commit')
        if last_commit:
            repo.last_commit_message = last_commit.get('message')
            commit_date_str = last_commit.get('date')
            if commit_date_str:
                repo.last_commit_date = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00'))
        
        repo.contributors = github_data.get('contributors', [])
        
        # Analyze with Gemini
        gemini_handler = GeminiHandler()
        analysis_result = gemini_handler.analyze_repository(github_data)
        
        if analysis_result.get('success'):
            analysis = analysis_result.get('analysis', {})
            repo.ai_summary = analysis.get('full_text', '')
            repo.performance_score = analysis.get('score')
            
            # Combine improvements and recommendations as suggestions
            suggestions = analysis.get('improvements', []) + analysis.get('recommendations', [])
            repo.suggestions = '\n'.join(suggestions) if suggestions else ''
            
            repo.is_analyzed = True
            log.status = 'success'
        else:
            log.status = 'failed'
            log.error_message = analysis_result.get('error', 'Analysis failed')
        
        repo.save()
        log.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Repository analyzed successfully!',
            'score': repo.performance_score
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def repo_detail(request, repo_id):
    """View detailed analysis of a repository"""
    repo = get_object_or_404(StudentRepo, id=repo_id, assignment__teacher=request.user)
    logs = AnalysisLog.objects.filter(repo=repo)
    
    context = {
        'repo': repo,
        'logs': logs,
    }
    
    return render(request, 'repo_detail.html', context)


@login_required
def bulk_add_repos(request, assignment_id):
    """Bulk add student repositories"""
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    
    if request.method == 'POST':
        repos_data = request.POST.get('repos_data', '')
        
        added_count = 0
        skipped_count = 0
        
        for line in repos_data.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(',')
            if len(parts) >= 2:
                student_name = parts[0].strip()
                repo_url = parts[1].strip()
                
                # Check if already exists
                if not StudentRepo.objects.filter(assignment=assignment, repo_url=repo_url).exists():
                    StudentRepo.objects.create(
                        assignment=assignment,
                        student_name=student_name,
                        repo_url=repo_url
                    )
                    added_count += 1
                else:
                    skipped_count += 1
        
        messages.success(request, f'Added {added_count} repositories. Skipped {skipped_count} duplicates.')
        return redirect('assignment_detail', assignment_id=assignment.id)
    
    return render(request, 'bulk_add_repos.html', {'assignment': assignment})
