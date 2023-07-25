from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.backends import ModelBackend  # Import the ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from urllib.parse import urlencode

from social_core.exceptions import AuthCanceled
from social_django.utils import load_strategy
from social_django.models import UserSocialAuth

from .forms import ProfileForm
from .models import Profile
from core.models import Download



def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create the User model and save it to the database
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()

            # Create the Profile model (or update if already exists)
            name = form.cleaned_data.get('username')
            role = 'VISITOR'  # Default role for new users (you can change this as needed)

            try:
                profile = Profile.objects.get(user=user)
                # If profile exists, update the name and role
                profile.name = name
                profile.role = role
                profile.save()
            except ObjectDoesNotExist:
                # If profile doesn't exist, create a new one
                profile = Profile.objects.create(user=user, name=name, role=role)

            # Specify the authentication backend
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserCreationForm()

    # Handle social authentication (remaining code as it is)
    # ...

    return render(request, 'register.html', {'form': form})



def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('core:home')  # Replace 'core:home' with the appropriate URL name for your home page
        else:
            messages.error(request, 'Login failed. Please correct the errors.')
    else:
        form = AuthenticationForm()
    
    next_param = request.GET.get('next')
    if next_param:
        form_action_url = f"{request.path}?{urlencode({'next': next_param})}"
    else:
        form_action_url = request.path

    if request.method == 'GET' and request.GET.get('process') == 'social':
        try:
            backend = request.GET.get('backend')
            user = request.backend.do_auth(request.backend.strategy, redirect_name='login')
            login(request, user)
            return redirect('core:home')
        except AuthCanceled:
            pass

    return render(request, 'login.html', {'form': form, 'form_action_url': form_action_url})



def userLogout(request):
    logout(request)
    return redirect('core:home')

@login_required
def userProfile(request):
    user = request.user
    recent_downloads = Download.objects.filter(user=request.user)

    context = {
        'recent_downloads': recent_downloads, 'user':user,
    }

    return render(request, 'profile.html', context)



def aboutUs(request):
    return render(request, 'about.html')

