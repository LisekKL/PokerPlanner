from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from PokerPlanner.models import PokerPlayer
from authorization.forms import RegisterForm, LoginForm


class Register(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'authorization/register.html', {'register_form': register_form})

    def post(self, request):
        error_text = "Error registering new player!"
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                user = User.objects.create_user(username=register_form.cleaned_data['username'],
                                                email=register_form.cleaned_data['email'],
                                                password=register_form.cleaned_data['password1'],
                                                first_name=register_form.cleaned_data['first_name'],
                                                last_name=register_form.cleaned_data['last_name'])
                PokerPlayer.objects.create(user=user)
                if user.is_authenticated():
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('Home:stories_overview'))
                    else:
                        return HttpResponseRedirect(reverse('Authorization:login', kwargs={'error_text': 'Account is '
                                                                                                         'inactive.'}))

                user = authenticate(username=user.username, password=user.password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('Home:stories_overview'))
                    else:
                        return HttpResponseRedirect(reverse('Authorization:login', kwargs={'error_text': 'Account is '
                                                                                                         'inactive.'}))
            except Exception as ex:
                error_text = ex

        return render(request, 'authorization/register.html', {'register_form': register_form, 'error_text': error_text})


class Login(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'authorization/login.html', {'login_form': login_form})

    def post(self, request):
        error_text = "Error loggining player!"

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.save(commit=False)

        if login_form.instance.username and login_form.instance.password:
            try:
                user = authenticate(username=login_form.instance.username, password=login_form.instance.password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse("Home:home"))
                    else:
                        return render(request, 'authorization/login.html',
                                      {'login_form': login_form, 'error_text': "Account is inactive."})
                else:
                    return render(request, 'authorization/login.html',
                                  {'login_form': login_form, 'error_text': "Username or password are "
                                                                           "incorrect"})
            except Exception as ex:
                error_text = ex
        return render(request, 'authorization/login.html', {'login_form': login_form, 'error_text': error_text})


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("Home:home"))
