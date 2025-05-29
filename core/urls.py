from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Project management
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/tasks/create/', views.create_task, name='add_task'),
    path('projects/<int:pk>/add-collaborator/', views.add_collaborator, name='add_collaborator'),
    path('projects/<int:project_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inbox/', views.inbox, name='inbox'),

    # Profile and user
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('search-users/', views.search_users, name='search_users'),
    path('profile/<int:user_id>/', views.profile, name='view_profile'),

    # Messaging
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:user_id>/', views.thread_view, name='thread'),
    path('messages/<int:user_id>/delete/', views.delete_thread, name='delete_thread'),
    path('messages/delete/<int:user_id>/', views.delete_chat, name='delete_chat'),
    path('messages/thread/<int:user_id>/', views.thread_view, name='thread_view_alt'),
    path('messages/<int:user_id>/', views.thread_view, name='thread_view'), 
]
