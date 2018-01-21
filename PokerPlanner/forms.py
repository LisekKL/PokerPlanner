from django import forms

from PokerPlanner.models import ScrumStory


class AddStoryForm(forms.ModelForm):
    storyTitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    storyPoints = forms.IntegerField(required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Points'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}))

    class Meta:
        model = ScrumStory
        fields = {'storyTitle', 'description', 'storyPoints'}

    def clean_storyTitle(self):
        data = self.cleaned_data['storyTitle']
        if ScrumStory.objects.filter(name=data).exists():
            raise forms.ValidationError("A story by this name already exists in the database!")
        return data
