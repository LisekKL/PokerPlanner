from django.contrib import admin

from PokerPlanner.models import PokerPlayer, ScrumStory, PokerGame, PokerTable

admin.site.register(PokerPlayer)
admin.site.register(ScrumStory)
admin.site.register(PokerGame)
admin.site.register(PokerTable)
