from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, Job, Application,Company

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['name', 'email', 'phone', 'resume', 'education', 'skills']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
