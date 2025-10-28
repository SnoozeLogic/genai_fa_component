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
    from django.utils import timezone
    
    assignments = Assignment.objects.filter(teacher=request.user)
    
    # Calculate statistics
    total_assignments = assignments.count()
    total_repos = StudentRepo.objects.filter(assignment__teacher=request.user).count()
    analyzed_repos = StudentRepo.objects.filter(assignment__teacher=request.user, is_analyzed=True).count()
    
    # Annotate assignments with student count
    from django.db.models import Count
    assignments_with_stats = assignments.annotate(
        student_count=Count('repos')
    ).order_by('-created_at')
    
    # Add additional stats for each assignment
    assignment_list = []
    for assignment in assignments_with_stats[:10]:  # Latest 10 assignments
        repos = StudentRepo.objects.filter(assignment=assignment)
        analyzed_count = repos.filter(is_analyzed=True).count()
        
        assignment_data = {
            'assignment': assignment,
            'student_count': assignment.student_count,
            'analyzed_count': analyzed_count,
            'pending_count': assignment.student_count - analyzed_count,
            'completion_percentage': round((analyzed_count / assignment.student_count * 100), 1) if assignment.student_count > 0 else 0,
        }
        assignment_list.append(assignment_data)
    
    context = {
        'assignments': assignments[:5],  # For backward compatibility
        'assignment_list': assignment_list,
        'total_assignments': total_assignments,
        'total_repos': total_repos,
        'analyzed_repos': analyzed_repos,
        'pending_analysis': total_repos - analyzed_repos,
        'now': timezone.now(),
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
    
    # Calculate statistics
    total_repos = repos.count()
    analyzed_repos = repos.filter(is_analyzed=True).count()
    pending_repos = total_repos - analyzed_repos
    
    # Commit statistics
    total_commits = sum(repo.commit_count for repo in repos)
    avg_commits = round(total_commits / total_repos, 1) if total_repos > 0 else 0
    
    # Debug output
    print(f"\n=== Assignment Detail Stats Debug ===")
    print(f"Assignment: {assignment.title}")
    print(f"Total repos: {total_repos}")
    print(f"Analyzed repos: {analyzed_repos}")
    print(f"Total commits: {total_commits}")
    print(f"Avg commits: {avg_commits}")
    print(f"=====================================\n")
    
    # Score statistics
    scored_repos = repos.filter(is_analyzed=True, performance_score__isnull=False)
    if scored_repos.exists():
        scores = [repo.performance_score for repo in scored_repos]
        avg_score = round(sum(scores) / len(scores), 1)
        max_score = max(scores)
        min_score = min(scores)
    else:
        avg_score = None
        max_score = None
        min_score = None
    
    # Language count
    all_languages = set()
    for repo in repos:
        if repo.languages:
            all_languages.update(repo.languages.keys())
    total_languages = len(all_languages)
    
    # Top performers
    top_repos = repos.filter(is_analyzed=True, performance_score__isnull=False).order_by('-performance_score')[:3]
    
    context = {
        'assignment': assignment,
        'repos': repos,
        # Statistics
        'total_repos': total_repos,
        'analyzed_repos': analyzed_repos,
        'pending_repos': pending_repos,
        'total_commits': total_commits,
        'avg_commits': avg_commits,
        'avg_score': avg_score,
        'max_score': max_score,
        'min_score': min_score,
        'total_languages': total_languages,
        'top_repos': top_repos,
        'completion_percentage': round((analyzed_repos / total_repos * 100), 1) if total_repos > 0 else 0,
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
            
            # Extract and validate score
            extracted_score = analysis.get('score')
            print(f"[VIEW DEBUG] Extracted score from analysis: {extracted_score}")
            
            if extracted_score is not None:
                # Ensure it's an integer or float
                try:
                    repo.performance_score = float(extracted_score)
                    print(f"[VIEW DEBUG] ✓ Saved performance_score: {repo.performance_score}")
                except (ValueError, TypeError) as e:
                    print(f"[VIEW DEBUG] ✗ Could not convert score {extracted_score} to number: {e}")
                    repo.performance_score = None
            else:
                print(f"[VIEW DEBUG] ✗ No score in analysis result")
                repo.performance_score = None
            
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
        
        print(f"[VIEW DEBUG] Repository saved. Final performance_score in DB: {repo.performance_score}")
        
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
