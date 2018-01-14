from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse

from PokerPlanner.models import ScrumStory, PokerPlayer
from .forms import LoginForm, RegisterForm


# Create your views here.


def index(request):
    story_amount = ScrumStory.objects.count()
    player_amount = PokerPlayer.objects.count()
    user_amount = User.objects.count()
    template = get_template('index.html')
    variables = {'user': request.user, 'story_amount': story_amount, 'player_amount': player_amount,
                 'user_amount': user_amount}
    output = template.render(variables)
    return HttpResponse(output)


def register(request):
    error_text = "Error registering new player!"
    if request.method == "GET":
        form = RegisterForm()
    if request.method == "POST":
        if request.POST.get('cancel'):
            return render(request, 'index.html', {'user': request.user})
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                player = form.save()
                player.refresh_from_db()
                PokerPlayer.objects.create(user=player, is_currently_in_game=False)
                if player.is_authenticated():
                    if player.is_active:
                        login(request, player)
                        return render(request, 'story_overview.html', {'user': player})
                    else:
                        return render(request, 'authorization/login.html', {'error_text': "Account is inactive."})
                    # return redirect('home', {'user': player})

                user = authenticate(username=player.username, password=player.password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'story_overview.html', {'user': request.user})
                    else:
                        return render(request, 'authorization/login.html', {'error_text': "Account is inactive."})
            except Exception as ex:
                error_text = ex
    return render(request, 'authorization/register.html', {'form': form, 'error_text': error_text})


def login_player(request):
    error_text = "Username or password is incorrect."
    if request.method == 'GET':
        return render(request, 'authorization/login.html', {'form': LoginForm()})
    elif request.method == 'POST':
        if request.POST.get('cancel'):
            return index(request)

        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # username = form.cleaned_data.get('username')
                # password = form.cleaned_data.get('username')
                username = user.username
                password = user.password
            except Exception as ex:
                error_text = ex
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

        if username and password:
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return index(request)
                    else:
                        return render(request, 'authorization/login.html', {'error_text': "Account is inactive."})
            except Exception as ex:
                error_text = ex
    return render(request, 'authorization/login.html', {'error_text': error_text})


def logout_player(request):
    logout(request)
    return index(request)


def stories_overview(request):
    story_amount = ScrumStory.objects.count()
    return render(request, 'story_overview.html', {'story_amount': story_amount})

