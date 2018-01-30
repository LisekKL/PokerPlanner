from datetime import datetime
from django import forms
from django.core.validators import RegexValidator

from PokerPlanner.models import ScrumStory, PokerGame, PokerPlayer, PokerDeck

title_validator = RegexValidator(regex=r'^(\w)+', message=u'Title must start with a word!')


class AddStoryForm(forms.ModelForm):
    storyTitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                                 required=True, validators=[title_validator])
    storyPoints = forms.IntegerField(required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Points'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
                                  required=True)

    class Meta:
        model = ScrumStory
        fields = {'storyTitle', 'description', 'storyPoints'}

    def clean_storyTitle(self):
        data = self.cleaned_data['storyTitle']
        if ScrumStory.objects.filter(name=data).exists():
            raise forms.ValidationError("A story by this name already exists in the database!")
        return data


class AddGameForm(forms.ModelForm):
    players = forms.ModelChoiceField(queryset=PokerPlayer.objects.filter(isAccepted=True), required=True,
                                     help_text="Choose players that may join the pokergame")
    startDate = forms.DateTimeField(initial=datetime.now())
    endDate = forms.DateTimeField(initial=datetime.now())
    story = forms.ModelChoiceField(queryset=ScrumStory.objects.filter(dateCompleted=None))
    playerChoices = {}
    deck = forms.ModelChoiceField(queryset=PokerDeck.objects.all())

    class Meta:
        model = PokerGame
        fields = {'players', 'startDate', 'endDate', 'story', 'deck'}

    def clean_story(self):
        story = self.cleaned_data.get('story')
        if not story:
            raise forms.ValidationError("A game must be linked to a scrum story! Please choose a story and try again.")
        if PokerGame.objects.filter(story__name=story).exists():
            raise forms.ValidationError("A story with this title already exists!")

    def clean_players(self):
        players = self.cleaned_data.get('players')
        if not players:
            raise forms.ValidationError("Can't add a game with no players to play!")
        if len(players) == 1:
            raise forms.ValidationError("No sense in pokering with one player!")
        return players

    def clean_startDate(self):
        startDate = self.cleaned_data['startDate']
        if startDate is not None and startDate.lte(datetime.now()):
            raise forms.ValidationError("You cannot start a game in the past! Please choose a later date!")
        return startDate

    def clean_endDate(self):
        endDate = self.cleaned_data['endDate']
        startDate = self.cleaned_data['startDate']
        if endDate is not None and startDate is not None and endDate.lte(startDate):
            raise forms.ValidationError("Ending date cannot be before the start! Please choose a different date!")


class AddPlayerForm(forms.ModelForm):
    player = forms.ModelChoiceField(queryset=PokerPlayer.objects.filter(isAccepted=False or None), required=True,
                                    help_text="Add valid players from set of registered users")

    class Meta:
        model = PokerPlayer
        fields = {'player'}

    def clean_player(self):
        player = self.cleaned_data['player']
        if not player:
            raise forms.ValidationError("You have to select a registered user!")
