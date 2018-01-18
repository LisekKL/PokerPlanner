from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class ScrumStory(models.Model):
    name = models.CharField(max_length=200, default="No name")
    description = models.TextField(default="")
    story_points = models.IntegerField(null=True, blank=True)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateCompleted = models.DateTimeField(null=True, blank=True)
    author = models.CharField(max_length=200, default="")

    def __str__(self):
        if self.dateCompleted:
            status = "Completed"
        else:
            status = "In progress"
        return "NAME: " + self.name + " DATE CREATED: " + str(self.dateCreated) + " STATUS = " + status

    def get_author(self):
        return self.author

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_date_created(self):
        return str(self.dateCreated)

    def get_date_completed(self):
        return str(self.dateCompleted)

    def get_story_points(self):
        return self.story_points

    def complete(self):
        self.dateCompleted = timezone.now()
        self.save()


class PokerTable(models.Model):
    deck = None

    def set_deck(self, deck):
        self.deck = deck


class PokerGame(models.Model):
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(PokerTable)
    story = models.ForeignKey(ScrumStory)
    playerLimit = models.IntegerField(null=True)
    playerList = []

    def start_game(self):
        self.startDate = timezone.now()
        self.save()

    def end_game(self):
        self.endDate = timezone.now()
        self.save()

    def get_points_for_story(self):
        return self.story.get_story_points()

    def add_player(self, player):
        if 0 < len(self.playerList) < self.playerLimit:
            self.playerList.append(player)
            self.save()

    def remove_player(self, player):
        self.playerList.remove(player)
        self.save()

    def get_current_players(self):
        return self.playerList;

    def get_story_info(self):
        return self.story.__str__()

    def set_player_limit(self, limit):
        self.playerLimit = limit
        self.save()


class PokerPlayer(models.Model):
    user = models.OneToOneField(User)
    chosenCard = None

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name

    def make_choice(self, card):
        self.chosenCard = card
        self.save()

    def get_choice(self):
        return self.chosenCard

    def join_game(self, game):
        self.pokerGame = game
        self.save()

    def leave_game(self):
        self.pokerGame = None
        self.chosenCard = None
        self.save()


class PokerDeck(models.Model):
    cards_in_deck = []

    def create_deck(self, array_points):
        for points in array_points:
            self.cards_in_deck.append(PokerCard(points))

    def get_available_cards(self):
        return self.cards_in_deck

    def remove_card(self, card):
        self.cards_in_deck.remove(card)

    def add_card(self, card):
        self.cards_in_deck.append(card)

    def shuffle_deck(self):
        """shuffle deck - random generator"""


class PokerCard(models.Model):
    story_points = models.IntegerField()
    deck = models.ForeignKey(PokerDeck)

    def __str__(self):
        return "CARD " + self.cardId + " WITH POINT VALUE: " + self.story_points

    def set_points(self, points):
        self.story_points = points

    def get_points(self):
        return self.story_points
