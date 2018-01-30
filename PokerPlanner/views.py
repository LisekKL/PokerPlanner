from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from PokerPlanner.forms import AddStoryForm, AddPlayerForm
from PokerPlanner.models import ScrumStory, PokerPlayer, PokerGame


class Home(View):
    def get(self, request):
        story_amount = ScrumStory.objects.count()
        player_amount = PokerPlayer.objects.count()
        user_amount = User.objects.count()
        stories = ScrumStory.objects.all()
        return render(request, 'index/index.html',
                      {'user': request.user, 'story_amount': story_amount, 'player_amount': player_amount,
                       'user_amount': user_amount, 'stories': stories})


class StoriesOverview(View):
    def get(self, request):
        stories = ScrumStory.objects.all()
        return render(request, 'index/stories/story_overview.html', {'stories': stories})


def get_story_overview(request):
    stories = ScrumStory.objects.all()
    return render(request, 'index/stories/story_overview.html', {'stories': stories})


class AddStory(View):
    def get(self, request):
        story_form = AddStoryForm()
        return render(request, 'index/stories/add_story.html', {'story_form': story_form})

    def post(self, request):
        story_form = AddStoryForm(data=request.POST)
        if story_form.is_valid():
            try:
                if request.user.is_authenticated():
                    author = request.user.first_name + ' ' + request.user.last_name
                    if author == ' ':
                        author = request.user.username
                    story = ScrumStory.objects.create(name=story_form.cleaned_data['storyTitle'],
                                                      description=story_form.cleaned_data['description'],
                                                      story_points=0,
                                                      dateCreated=datetime.now(),
                                                      dateCompleted=None,
                                                      author=author)
            except Exception as ex:
                error_text = ex

        return get_story_overview(request)


class GamesOverview(View):
    def get(self, request):
        active_games = PokerGame.objects.filter(endDate__gte=datetime.now())
        return render(request, 'index/games/current_games_overview.html', {'active_games': active_games})


def delete_story(request, storyId):
    story = ScrumStory.objects.get(id=storyId)
    story.delete()
    return get_story_overview(request)


class PlayerListView(ListView):
    model = PokerPlayer
    template_name = 'index/players/players_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class AddPokerPlayers(View):
    def get(self, request):
        users = PokerPlayer.objects.filter(isAccepted=False)
        players = PokerPlayer.objects.filter(isAccepted=True)
        return render(request, 'index/players/add_player.html', {'users': users, 'players': players})

    def post(self, request):
        add_player_form = AddPlayerForm(data=request.POST)
        if add_player_form.is_valid():
            player = add_player_form.cleaned_data['player']
            PokerPlayer.objects.create(user=player)
        return HttpResponseRedirect(reverse('Home:players_overview'))


def start_poker_game(request, storyId):
    story = ScrumStory.objects.get(id=storyId)
    return render(request, 'index/games/start_game.html', {'story': story})
