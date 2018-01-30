import random

from django.contrib.auth.models import User
from django.db import models
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


class PokerPlayer(models.Model):
    user = models.OneToOneField(User)
    # Acceptance by scrum master through dashboard
    isAccepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name


class PokerGame(models.Model):
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(null=True, blank=True)
    story = models.ForeignKey(ScrumStory)
    players = models.ManyToManyField(PokerPlayer)
    playerChoices = {}
    deck = None

    def start_game(self):
        self.startDate = timezone.now()
        self.save()

    def end_game(self):
        self.endDate = timezone.now()
        self.save()

    def get_points_for_story(self):
        return self.story.get_story_points()

    def add_player(self, player):
        if 0 < len(self.players) < self.playerLimit:
            self.players.append(player)
            self.save()

    def remove_player(self, player):
        self.players.remove(player)
        self.save()

    def get_current_players(self):
        return self.players

    def get_story_info(self):
        return self.story

    def set_player_limit(self, limit):
        self.playerLimit = limit
        self.save()

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck


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
        random.shuffle(self.cards_in_deck)


class PokerCard(models.Model):
    story_points = models.IntegerField()

    def __str__(self):
        return "CARD " + str(self.id) + " WITH POINT VALUE: " + self.story_points

    def set_points(self, points):
        self.story_points = points

    def get_points(self):
        return self.story_points
