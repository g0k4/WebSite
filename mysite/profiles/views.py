from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import HttpResponse


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for you!')
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
        user_person = User.objects.filter(username=request.user)
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user_form = form.save(commit=False)
            if not user_form.email:
                user_form.email = user_person[0].email
            if not user_form.username:
                user_form.username = user_person[0].username
            user_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profiles:update')
    else:
        form = UserUpdateForm()
        form_p = PasswordChangeForm(request.user)
    return render(request, 'profiles/profile.html', {
        'form':form,
        'form_p':form_p,
        })

@login_required()
def update_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was successfully updated!')
            return redirect('profiles:update')
        else:
            messages.error(request, f'Please correct the error below.')
            return redirect('profiles:update')
    else:
        return redirect('profiles:update')