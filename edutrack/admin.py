from django.contrib import admin
from .models import Assignment, StudentRepo, AnalysisLog


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'created_at', 'deadline']
    list_filter = ['created_at', 'teacher']
    search_fields = ['title', 'description']


@admin.register(StudentRepo)
class StudentRepoAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'assignment', 'commit_count', 'is_analyzed', 'last_updated']
    list_filter = ['is_analyzed', 'assignment', 'created_at']
    search_fields = ['student_name', 'repo_url']


@admin.register(AnalysisLog)
class AnalysisLogAdmin(admin.ModelAdmin):
    list_display = ['repo', 'status', 'analysis_date']
    list_filter = ['status', 'analysis_date']
    search_fields = ['repo__student_name']
