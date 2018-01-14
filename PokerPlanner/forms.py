from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password'}
        widgets = {'password': forms.PasswordInput()}
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password', 'first_name', 'last_name', 'email'}
        widgets = {'password': forms.PasswordInput()}
    username = forms.CharField(label='Username', max_length=20)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=150)
    email = forms.CharField(label='Email', max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
