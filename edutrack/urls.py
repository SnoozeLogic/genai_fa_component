from django.urls import path
from . import views
from . import analytics

urlpatterns = [
    # Home and Auth
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Assignments
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    
    # Analytics & Reports
    path('assignments/<int:assignment_id>/analytics/', analytics.assignment_analytics, name='assignment_analytics'),
    path('assignments/<int:assignment_id>/report/', analytics.generate_assignment_report, name='generate_report'),
    
    # Repositories
    path('assignments/<int:assignment_id>/add-repo/', views.add_student_repo, name='add_student_repo'),
    path('assignments/<int:assignment_id>/bulk-add/', views.bulk_add_repos, name='bulk_add_repos'),
    path('repo/<int:repo_id>/', views.repo_detail, name='repo_detail'),
    path('repo/<int:repo_id>/analyze/', views.analyze_repo, name='analyze_repo'),
]
