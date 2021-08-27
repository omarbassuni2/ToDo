from django.contrib.auth import logout, login
from django.core.checks import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import *

# Create your views here.
from accounts.models import *


@login_required(login_url='login')
def home(request):
    buckets = Bucket.objects.filter(user=request.user.id)
    context = {'buckets': buckets}
    return render(request, "accounts/home.html", context)

@login_required(login_url='login')
def create_task(request):
    form = CreateTaskForm(request.POST)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        form = CreateTaskForm()
    context = {'form': form}
    return render(request, 'accounts/create_task.html', context)


def register(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')  # the user comes here from the GET request if he's authenticated
    else:
        form = UserAuthenticationForm(
            request.POST)  # removed the request.POST and it removed the error, didn't solve the problem
    context = {'form': form}  # should be put in else, supposedly?
    return render(request, 'accounts/login.html', context)


# Requires admin login
def dashboard(request):
    if not request.user.is_admin:
        return redirect('home')
    buckets = Bucket.objects.all().order_by('date_created')
    buckets_count = Bucket.objects.count()
    users_count = User.objects.count()
    context = {'buckets': buckets, 'buckets_count': buckets_count, 'users_count': users_count}
    return render(request, 'accounts/dashboard.html', context)
