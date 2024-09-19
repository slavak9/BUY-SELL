from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth']