#!/usr/bin/env python
"""
Test script to verify assignment statistics calculation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from edutrack.models import Assignment, StudentRepo

print("\n" + "="*60)
print("ASSIGNMENT STATISTICS VERIFICATION")
print("="*60)

assignments = Assignment.objects.all()
print(f"\nTotal assignments: {assignments.count()}\n")

for assignment in assignments:
    repos = StudentRepo.objects.filter(assignment=assignment)
    
    # Calculate statistics (matching view logic)
    total_repos = repos.count()
    analyzed_repos = repos.filter(is_analyzed=True).count()
    pending_repos = total_repos - analyzed_repos
    
    # Commit statistics
    total_commits = sum(repo.commit_count for repo in repos)
    avg_commits = round(total_commits / total_repos, 1) if total_repos > 0 else 0
    
    # Language count
    all_languages = set()
    for repo in repos:
        if repo.languages:
            all_languages.update(repo.languages.keys())
    total_languages = len(all_languages)
    
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
    
    print(f"Assignment: {assignment.title}")
    print(f"  Created: {assignment.created_at.strftime('%Y-%m-%d')}")
    if assignment.deadline:
        print(f"  Deadline: {assignment.deadline.strftime('%Y-%m-%d %H:%M')}")
    print(f"\n  Statistics:")
    print(f"    Total Students: {total_repos}")
    print(f"    Analyzed: {analyzed_repos}")
    print(f"    Pending: {pending_repos}")
    print(f"    Total Commits: {total_commits}")
    print(f"    Avg Commits: {avg_commits}")
    print(f"    Languages Used: {total_languages}")
    print(f"    Avg Score: {avg_score if avg_score else 'N/A'}")
    if avg_score:
        print(f"    Score Range: {min_score} - {max_score}")
    print(f"    Completion: {round((analyzed_repos / total_repos * 100), 1) if total_repos > 0 else 0}%")
    print()
    
    # Show individual repo details
    if total_repos > 0:
        print(f"  Individual Repositories:")
        for repo in repos:
            status = "✓ Analyzed" if repo.is_analyzed else "✗ Pending"
            score = f"Score: {repo.performance_score}" if repo.performance_score else "No score"
            print(f"    - {repo.student_name}: {repo.commit_count} commits | {status} | {score}")
    print("\n" + "-"*60)

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60 + "\n")
