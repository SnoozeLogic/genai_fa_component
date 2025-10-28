from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Assignment, StudentRepo
from collections import Counter
import json


@login_required
def assignment_analytics(request, assignment_id):
    """
    Comprehensive analytics view for an assignment
    Shows overview of all students, commits, languages, etc.
    """
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    repos = StudentRepo.objects.filter(assignment=assignment)
    
    # Calculate analytics
    analytics = {
        'assignment': assignment,
        'total_students': repos.count(),
        'analyzed_repos': repos.filter(is_analyzed=True).count(),
        'pending_repos': repos.filter(is_analyzed=False).count(),
    }
    
    # Total commits
    total_commits = sum(repo.commit_count for repo in repos)
    analytics['total_commits'] = total_commits
    
    # Average commits per student
    if repos.count() > 0:
        analytics['avg_commits'] = round(total_commits / repos.count(), 1)
    else:
        analytics['avg_commits'] = 0
    
    # Language statistics (aggregate all languages used)
    all_languages = Counter()
    for repo in repos:
        if repo.languages:
            # Add language bytes counts
            for lang, bytes_count in repo.languages.items():
                all_languages[lang] += bytes_count
    
    # Convert to percentages
    total_bytes = sum(all_languages.values())
    language_stats = []
    if total_bytes > 0:
        for lang, bytes_count in all_languages.most_common(10):
            percentage = (bytes_count / total_bytes) * 100
            language_stats.append({
                'language': lang,
                'percentage': round(percentage, 1),
                'bytes': bytes_count
            })
    
    analytics['language_stats'] = language_stats
    analytics['total_languages'] = len(all_languages)
    
    # Performance score statistics
    analyzed_repos = repos.filter(is_analyzed=True, performance_score__isnull=False)
    if analyzed_repos.exists():
        scores = [repo.performance_score for repo in analyzed_repos]
        analytics['avg_score'] = round(sum(scores) / len(scores), 1)
        analytics['max_score'] = max(scores)
        analytics['min_score'] = min(scores)
        
        # Score distribution
        analytics['excellent'] = len([s for s in scores if s >= 90])
        analytics['good'] = len([s for s in scores if 75 <= s < 90])
        analytics['average'] = len([s for s in scores if 60 <= s < 75])
        analytics['needs_improvement'] = len([s for s in scores if s < 60])
    else:
        analytics['avg_score'] = None
        analytics['max_score'] = None
        analytics['min_score'] = None
        analytics['excellent'] = 0
        analytics['good'] = 0
        analytics['average'] = 0
        analytics['needs_improvement'] = 0
    
    # Top performers
    analytics['top_performers'] = repos.filter(
        is_analyzed=True, 
        performance_score__isnull=False
    ).order_by('-performance_score')[:5]
    
    # Most active students (by commits)
    analytics['most_active'] = repos.filter(
        commit_count__gt=0
    ).order_by('-commit_count')[:5]
    
    # Student list with stats
    students_data = []
    for repo in repos:
        student_data = {
            'name': repo.student_name,
            'commits': repo.commit_count,
            'languages': list(repo.languages.keys()) if repo.languages else [],
            'score': repo.performance_score,
            'analyzed': repo.is_analyzed,
            'id': repo.id
        }
        students_data.append(student_data)
    
    analytics['students'] = students_data
    
    # Prepare data for charts (JSON)
    analytics['language_chart_data'] = json.dumps({
        'labels': [ls['language'] for ls in language_stats[:5]],
        'data': [ls['percentage'] for ls in language_stats[:5]]
    })
    
    analytics['score_distribution_data'] = json.dumps({
        'labels': ['Excellent (90+)', 'Good (75-89)', 'Average (60-74)', 'Needs Work (<60)'],
        'data': [analytics['excellent'], analytics['good'], analytics['average'], analytics['needs_improvement']]
    })
    
    return render(request, 'assignment_analytics.html', analytics)


@login_required
def generate_assignment_report(request, assignment_id):
    """
    Generate a comprehensive text report for the assignment
    """
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    repos = StudentRepo.objects.filter(assignment=assignment)
    
    # Calculate all statistics
    total_students = repos.count()
    analyzed_repos = repos.filter(is_analyzed=True).count()
    total_commits = sum(repo.commit_count for repo in repos)
    
    # Language statistics
    all_languages = Counter()
    for repo in repos:
        if repo.languages:
            for lang, bytes_count in repo.languages.items():
                all_languages[lang] += bytes_count
    
    # Performance scores
    analyzed_repos_with_scores = repos.filter(is_analyzed=True, performance_score__isnull=False)
    avg_score = None
    if analyzed_repos_with_scores.exists():
        scores = [repo.performance_score for repo in analyzed_repos_with_scores]
        avg_score = round(sum(scores) / len(scores), 1)
    
    # Generate report
    report = f"""
# Assignment Analysis Report: {assignment.title}

**Generated:** {assignment.created_at.strftime('%B %d, %Y')}
**Teacher:** {assignment.teacher.username}

---

## 📊 Overview Statistics

- **Total Students:** {total_students}
- **Repositories Analyzed:** {analyzed_repos} / {total_students}
- **Total Commits (All Students):** {total_commits}
- **Average Commits per Student:** {round(total_commits / total_students, 1) if total_students > 0 else 0}
- **Average Performance Score:** {avg_score if avg_score else 'Not yet analyzed'}

---

## 💻 Programming Languages Used

"""
    
    # Add language breakdown
    total_bytes = sum(all_languages.values())
    if total_bytes > 0:
        for lang, bytes_count in all_languages.most_common():
            percentage = (bytes_count / total_bytes) * 100
            report += f"- **{lang}:** {percentage:.1f}%\n"
    else:
        report += "- No language data available\n"
    
    report += "\n---\n\n## 👥 Student Details\n\n"
    
    # Add individual student details
    for repo in repos.order_by('student_name'):
        report += f"\n### {repo.student_name}\n"
        report += f"- **Repository:** {repo.repo_url}\n"
        report += f"- **Commits:** {repo.commit_count}\n"
        
        if repo.languages:
            langs = ', '.join(repo.languages.keys())
            report += f"- **Languages:** {langs}\n"
        
        if repo.is_analyzed:
            report += f"- **Performance Score:** {repo.performance_score if repo.performance_score else 'N/A'}\n"
            if repo.ai_summary:
                report += f"- **AI Summary:** {repo.ai_summary[:200]}...\n"
        else:
            report += f"- **Status:** Not yet analyzed\n"
        
        report += "\n"
    
    # Return as downloadable text
    response = JsonResponse({
        'success': True,
        'report': report,
        'filename': f"{assignment.title.replace(' ', '_')}_report.md"
    })
    
    return response
