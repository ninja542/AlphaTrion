from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.template.loader import render_to_string
from s3direct.widgets import S3DirectWidget


# http://www.hoboes.com/Mimsy/hacks/replicating-djangos-admin/
class SelectWithPop(forms.Select):
	def render(self, name, *args, **kwargs):
		html = super(SelectWithPop, self).render(name, *args, **kwargs)
		rawname = name.split('-')[-1];
		popupplus = render_to_string("surveys/popup.html", {'field': rawname})

		return html+popupplus


class CommunityGameRatingsForm(forms.ModelForm):

	class Meta:
		model = CommunityGameRatings
		exclude = ("user", "games")
		widgets = {
		'game_rating': forms.RadioSelect(attrs={'class': 'game_rating'},),
		'game_comments': forms.Textarea(attrs={'placeholder': 'Describe what you thought of the game here! (Optional)'})
		}


class CommunityExtraRatingsForm(forms.ModelForm):

	class Meta:
		model = CommunityExtraRatings
		exclude = ('user', 'community')
		widgets = {
		'extra_comments': forms.Textarea(attrs={'placeholder': 'Describe some other thoughts that you have about community here (Optional)'}),
		'how_can_we_improve_survey': forms.Textarea(attrs={'placeholder': 'We take data collection very seriously and would love to hear student\'s thoughts about how it can be improved (Optional)'}),
		'overall_rating': forms.RadioSelect(attrs={'class': 'overall_rating'})
		}

class CommunityInstanceCreationForm(forms.ModelForm):
	photo = forms.URLField(widget=S3DirectWidget(dest='community'))
	class Meta:
		model = CommunityInst
		exclude = ('spectrum_id', 'occuring_games')
		widgets = {
			'date': forms.DateInput(attrs={'class': 'datepicker'}),
		}

class CommunityGamesCreationForm(forms.ModelForm):
	game = forms.ModelChoiceField(Game.objects, widget=SelectWithPop)
	class Meta:
		model = CommunityGames
		exclude = ('communityinst',)

class GameCreationForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ('__all__')

