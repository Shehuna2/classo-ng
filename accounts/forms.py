from django import forms
from django.contrib.auth.models import User

from .models import Profile

class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'role']