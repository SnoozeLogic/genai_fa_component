from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    """Model for assignments created by teachers"""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.teacher.username}"


class StudentRepo(models.Model):
    """Model for student GitHub repositories"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='repos')
    student_name = models.CharField(max_length=100)
    repo_url = models.URLField()
    
    # GitHub Data
    commit_count = models.IntegerField(default=0)
    languages = models.JSONField(default=dict)
    readme_content = models.TextField(blank=True, null=True)
    last_commit_message = models.TextField(blank=True, null=True)
    last_commit_date = models.DateTimeField(blank=True, null=True)
    contributors = models.JSONField(default=list)
    
    # AI Analysis
    ai_summary = models.TextField(blank=True, null=True)
    performance_score = models.FloatField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_analyzed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['assignment', 'repo_url']

    def __str__(self):
        return f"{self.student_name} - {self.assignment.title}"


class AnalysisLog(models.Model):
    """Log of AI analysis runs"""
    repo = models.ForeignKey(StudentRepo, on_delete=models.CASCADE, related_name='analysis_logs')
    analysis_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ])
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-analysis_date']

    def __str__(self):
        return f"{self.repo.student_name} - {self.status} - {self.analysis_date}"
