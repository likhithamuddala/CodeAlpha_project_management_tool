from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Comment, Message
from .forms import ProjectForm, TaskForm, CommentForm, EditProfileForm
#from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import CustomUserCreationForm, MessageForm
from django.db.models import Q, Max
from collections import defaultdict
from django.db.models import Count
from django.db import models
from .models import Project, ProjectCollaborator, Thread


User = get_user_model()


def home(request):
    print("Logged-in user:", request.user)
    print("Username:", request.user.username)
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(creator=request.user)
    return render(request, 'core/project_list.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)

    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'core/project_detail.html', context)

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()

            # Add the creator to members
            project.members.add(request.user)

            # Handle collaborators and jobs
            collaborator_ids = request.POST.getlist('collaborator[]')
            jobs = request.POST.getlist('job[]')

            for user_id, role in zip(collaborator_ids, jobs):
                try:
                    user = User.objects.get(id=user_id)
                    project.members.add(user)

                    # Add to ProjectCollaborator table
                    ProjectCollaborator.objects.create(
                        project=project,
                        user=user,
                        role=role
                    )
                except User.DoesNotExist:
                    continue

            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'projects/create_project.html', {
        'project_form': form,
        'users': users,
    })



def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()  # Required if using ManyToMany fields
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm()
    return render(request, 'core/create_task.html', {'form': form, 'project': project})


@login_required
def task_detail(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)
    comments = Comment.objects.filter(task=task).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', project_id=project.id, task_id=task.id)
    else:
        form = CommentForm()

    return render(request, 'core/task_detail.html', {
        'project': project,
        'task': task,
        'comments': comments,
        'form': form
    })

@login_required
def add_collaborator(request, pk):
    project = get_object_or_404(Project, pk=pk)
    User = get_user_model()  # Correctly get the custom user model
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            project.members.add(user)
        except User.DoesNotExist:
            return render(request, 'core/add_collaborator.html', {
                'project': project,
                'error': "User does not exist."
            })
        return redirect('project_detail', pk=pk)
    return render(request, 'core/add_collaborator.html', {'project': project})

@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')
    context = {
        'tasks': tasks,
    }
    return render(request, 'core/dashboard.html', context)




@login_required
def profile_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    projects = Project.objects.filter(members=user)
    tasks = Task.objects.filter(assigned_to=user)

    return render(request, 'core/profile.html', {
        'profile_user': user,
        'projects': projects,
        'tasks': tasks,
    })

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    # Show projects where user is a member or the creator
    user_projects = Project.objects.filter(
        Q(members=profile_user) | Q(creator=profile_user)
    ).distinct()

    # Show tasks assigned to the user
    tasks = Task.objects.filter(assigned_to=profile_user)

    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'user_projects': user_projects,
        'tasks': tasks
    })



@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=user.username)  
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_projects = Project.objects.filter(
        Q(creator=profile_user) | Q(members=profile_user)
    ).distinct()
    tasks = Task.objects.filter(assigned_to=profile_user)

    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'user_projects': user_projects,
        'tasks': tasks,
    })

@login_required
def inbox_view(request):
    user = request.user
    messages = Message.objects.filter(receiver=user).order_by('-timestamp')

    conversations = {}
    for message in messages:
        sender = message.sender
        if sender not in conversations:
            conversations[sender] = message

    context = {
        'conversations': conversations
    }
    return render(request, 'core/inbox.html', context)

@login_required
def thread(request, user_id):
    recipient = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('thread', user_id=recipient.id)

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')

    return render(request, 'messages/thread.html', {
        'recipient': recipient,
        'messages': messages,
    })



@login_required
def thread_view(request, user_id):
    recipient = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        print("Message content:", content)  # DEBUG
        if content:
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            print("Message saved")  # DEBUG
            return redirect('thread_view', user_id=recipient.id)

    messages = Message.objects.filter(
        sender__in=[request.user, recipient],
        recipient__in=[request.user, recipient]
    ).order_by('timestamp')

    return render(request, 'messages/thread.html', {
        'recipient': recipient,
        'messages': messages,
    })


@login_required
def delete_thread(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).delete()
        return redirect('inbox')

    return redirect('thread_view', user_id=other_user.id)

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_message_count': count}
    return {'unread_message_count': 0}


@login_required
def delete_chat(request, user_id):
    recipient = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        Message.objects.filter(
            sender__in=[request.user, recipient],
            recipient__in=[request.user, recipient]
        ).delete()
        return redirect('thread_view', user_id=user_id)

@login_required
def search_users(request):
    query = request.GET.get('q')
    users = []
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    
    threads = get_user_threads(request.user)
    return render(request, 'core/inbox.html', {'users': users, 'threads': threads})




@login_required
def inbox(request):
    """
    Displays a list of users the current user has messaged with,
    showing the most recent message from each conversation.
    """
    query = request.GET.get('q', '')
    search_results = []

    if query:
        search_results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    # Fetch all messages involving the current user
    messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('-timestamp')
    conversations = {}

    for message in messages:
        other_user = message.recipient if message.sender == request.user else message.sender
        if other_user not in conversations:
            conversations[other_user] = {
                'user': other_user,
                'message': message
            }

    return render(request, 'core/inbox.html', {
        'query': query,
        'search_results': search_results,
        'conversations': conversations.values()
    })


def get_user_threads(user):
    # Get all messages involving the current user
    messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
    threads = {}
    
    for msg in messages.order_by('-timestamp'):
        other_user = msg.receiver if msg.sender == user else msg.sender
        if other_user not in threads:
            threads[other_user] = {
                'other_user': other_user,
                'last_message': msg,
            }
    return list(threads.values())

def some_view(request):
    # Suppose you're passing a user object to template
    user = get_object_or_404(User, id=some_id)
    return render(request, 'template.html', {'user': user})

def view_profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('inbox')  # or show a custom 404 page

    return render(request, 'core/profile.html', {'user': user})