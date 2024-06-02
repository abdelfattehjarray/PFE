# your_project/accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude password field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']