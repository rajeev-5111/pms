from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, StudentProfile, Company, Job, Application
from .forms import UserRegisterForm, StudentProfileForm, CompanyForm, JobForm, ApplicationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if 'is_student' in request.POST:
                user.is_student = True
            elif 'is_company' in request.POST:
                user.is_company = True
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Profile management view
@login_required
def profile(request):
    try:
        if request.user.is_student:
            profile = StudentProfile.objects.get(user=request.user)
            if request.method == 'POST':
                form = StudentProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
            else:
                form = StudentProfileForm(instance=profile)
        elif request.user.is_company:
            profile = Company.objects.get(user=request.user)
            if request.method == 'POST':
                form = CompanyForm(request.POST, instance=profile)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
            else:
                form = CompanyForm(instance=profile)
    except (StudentProfile.DoesNotExist, Company.DoesNotExist):
        # If profile does not exist, create an empty profile
        if request.user.is_student:
            profile = StudentProfile(user=request.user)
            profile.save()
            form = StudentProfileForm(instance=profile)
        elif request.user.is_company:
            profile = Company(user=request.user)
            profile.save()
            form = CompanyForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

# View job listings
@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

# View job detail and apply
@login_required
def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        application = Application(job=job, student=request.user)
        application.save()
        return redirect('job_list')
    return render(request, 'job_detail.html', {'job': job})

# Post job listing (company)
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = Company.objects.get(user=request.user)
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

# View applicants (company)
@login_required
def view_applicants(request):
    company = Company.objects.get(user=request.user)
    jobs = Job.objects.filter(company=company)
    applications = Application.objects.filter(job__in=jobs)
    return render(request, 'view_applicants.html', {'applications': applications})

# Admin views
@login_required
def admin_dashboard(request):
    students = User.objects.filter(is_student=True)
    companies = User.objects.filter(is_company=True)
    jobs = Job.objects.all()
    applications = Application.objects.all()
    return render(request, 'admin_dashboard.html', {
        'students': students,
        'companies': companies,
        'jobs': jobs,
        'applications': applications
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to profile or any other desired page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})