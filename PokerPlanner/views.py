from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from PokerPlanner.models import ScrumStory, PokerPlayer


class Home(View):

    def get(self, request):
        story_amount = ScrumStory.objects.count()
        player_amount = PokerPlayer.objects.count()
        user_amount = User.objects.count()
        return render(request, 'index/index.html',
                      {'user': request.user, 'story_amount': story_amount, 'player_amount': player_amount,
                       'user_amount': user_amount})


def stories_overview(request):
    story_amount = ScrumStory.objects.count()
    return render(request, 'index/story_overview.html', {'story_amount': story_amount})
