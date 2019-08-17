from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, f'Account created for you!')
            return redirect('profiles:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('news:home')
    else:
        form = AuthenticationForm()

    return render(request, 'profiles/login.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('profiles:login')

@login_required()
def update_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Yout account has been updated!')
    else:
        form = UserUpdateForm()
    return render(request, 'profiles/profile.html', {'form':form})
