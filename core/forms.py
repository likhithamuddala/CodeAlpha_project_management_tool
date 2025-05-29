from django import forms
from .models import Project, Task, Comment, CustomUser, Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reply


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to', 'due_date']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['assigned_to'].queryset = project.collaborators.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'location', 'birthdate']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'location', 'birthdate', 'password1', 'password2')
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
print("Defined in forms.py:", dir())

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content'] 