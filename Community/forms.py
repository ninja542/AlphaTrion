from django import forms
from django.core.exceptions import ValidationError
from .models import CommunityGameRatings, CommunityPacingRatings, CommunityExtraRatings

class CommunityGameRatingsForm(forms.ModelForm):

	class Meta:
		model = CommunityGameRatings
		exclude = ("user", "games")
		widgets = {
		'game_rating': forms.RadioSelect(attrs={'class': 'game_rating'},),
		'game_comments': forms.Textarea(attrs={'placeholder': 'Describe what you thought of the game here! (Optional)'})
		}

class CommunityPacingRatingsForm(forms.ModelForm):
	
	class Meta:
		model = CommunityPacingRatings
		exclude = ('user', 'community')

class CommunityExtraRatingsForm(forms.ModelForm):

	class Meta:
		model = CommunityExtraRatings
		exclude = ('user', 'community')
		widgets = {
		'extra_comments': forms.Textarea(attrs={'placeholder': 'Describe some other thoughts that you have about community here (Optional)'}),
		'how_can_we_improve_survey': forms.Textarea(attrs={'placeholder': 'We take data collection very seriously and would love to hear student\'s thoughts about how it can be improved (Optional)'}),
		}
