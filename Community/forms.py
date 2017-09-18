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
	
	class meta:
		model = CommunityExtraRatings
		exclude = ('user', 'community')
