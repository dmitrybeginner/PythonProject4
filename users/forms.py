from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "password1", "password2")


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

