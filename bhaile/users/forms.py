from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    owner = forms.BooleanField(required=False)
    student = forms.BooleanField()

    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2', 'owner', 'student']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    owner = forms.BooleanField(required=False)
    student = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'email', 'owner', 'student']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
