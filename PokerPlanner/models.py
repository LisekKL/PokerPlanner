from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.


class ScrumStory(models.Model):
    name = models.CharField(max_length=200, default="")
    story_points = models.IntegerField(default=0)
    dateCreated = models.DateTimeField()
    dateCompleted = models.DateTimeField(null=True, blank=True)
    author = models.CharField(max_length=200, default="")

    def __init__(self):
        self.name = "New SCRUM story"
        self.dateCreated = timezone.now()
        self.dateCompleted = None

    def __str__(self):
        if self.dateCompleted:
            status = "Completed"
        else:
            status = "In progress"
        return "NAME: " + self.storyName + " DATE CREATED: " + self.dateCreated + " STATUS = " + status

    def get_story_points(self):
        return self.storyPoints

    def complete(self):
        self.dateCompleted = timezone.now()
        self.save()


class PokerTable(models.Model):
    playerLimit = models.IntegerField()
    deck = None

    def set_deck(self, deck):
        self.deck = deck

    def set_player_limit(self, limit):
        self.playerLimit = limit

    def add_player(self, player):
        if 0 < len(self.PlayerList) < self.PlayerLimit:
            self.PlayerList.append(player)


class PokerGame(models.Model):
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(PokerTable)
    story = models.ForeignKey(ScrumStory)
    playerList = []

    def __init__(self):
        self.endDate = None

    def start_game(self):
        self.startDate = timezone.now()
        self.save()

    def end_game(self):
        self.endDate = timezone.now()
        self.save()

    def get_points_for_story(self):
        return self.story.get_story_points()

    def add_player(self, player):
        self.playerList.__add__(player)
        self.save()

    def remove_player(self, player):
        self.playerList.remove(player)
        self.save()

    def get_current_players(self):
        return self.playerList;

    def get_story_info(self):
        return self.story.__str__()


class PokerPlayer(models.Model):
    user = models.OneToOneField(User)
    is_currently_in_game = models.BooleanField(default=False)
    currentPokerGame = None
    chosenCard = None

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name

    def make_choice(self, card):
        self.chosenCard = card

    def get_choice(self):
        return self.chosenCard

    def join_game(self, game):
        if self.is_currently_in_game:
            return "Player is currently in an other game! Please finish the other game first!"
        self.pokerGame = game
        self.is_currently_in_game = True

    def leave_game(self):
        self.pokerGame = None
        self.is_currently_in_game = False
        self.chosenCard = None


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
    style = None

    def __str__(self):
        return "CARD " + self.cardId + " WITH POINT VALUE: " + self.story_points

    def set_points(self, points):
        self.story_points = points

    def get_points(self):
        return self.story_points


class PokerCardStyle:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.image = None

    def change_image(self, image):
        self.image = image

    def change_width(self, width):
        self.width = width

    def change_height(self, height):
        self.height = height


class PokerTableStyle:
    def __init__(self):
        self.image = None

    def change_image(self, image):
        self.image = image


class Image:
    def __init__(self):
        self.url = ""
        self.width = 0
        self.height = 0
        self.alternativeText = ""

    def set_alternative_text(self, text):
        self.alternativeText = text

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_url(self, url):
        self.url = url
