from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('post_job/', views.post_job, name='post_job'),
    path('view_applicants/', views.view_applicants, name='view_applicants'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]