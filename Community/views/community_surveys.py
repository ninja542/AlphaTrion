from __future__ import division	
import numpy as np
from django.shortcuts import render
from django.views import generic 	
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.models import Group
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.core.properties import Instance, String 
from bokeh.models import ColumnDataSource, LayoutDOM
from bokeh.io import show
from django.forms import formset_factory
from django.utils.html import escape
from Community.models import *
from Community.forms import *

class CommunityInstView(generic.ListView): 
	model = CommunityInst
	template_name = 'surveys/survey_list.html'

# Specfic Survey for a community
def review_community_instance(request, communityid):
	user = None
	if request.user.is_authenticated():
		user = request.user
	if not user:
		return render(request, 'not_logged_in.html')


	community = get_object_or_404(CommunityInst, pk=communityid)
	
	if request.method == "POST":
		game_form_dict = dict()
		for games in community.occuring_games.all():
			game_form_dict[games.name] = CommunityGameRatingsForm(request.POST, prefix='{}'.format(games.name))

		pacing_section = CommunityPacingRatingsForm(request.POST)
		extra_section = CommunityExtraRatingsForm(request.POST)
		true_condintions = 0 
		for y in game_form_dict.values():
			if y.is_valid():
				true_condintions += 1
			else: 
				pass

		if true_condintions == len(game_form_dict.values()):
			if pacing_section.is_valid():
				pacing_rating = pacing_section.cleaned_data['pacing_rating']
				if CommunityPacingRatings.objects.filter(user=user, community=community):
					raise ValidationError("You've already submitted this survey!")
				else:
					CommunityPacingRatings.objects.create(user=user, community=community, pacing_rating=pacing_rating)

			if extra_section.is_valid():
				overall_rating = extra_section.cleaned_data['overall_rating']
				extra_comments = extra_section.cleaned_data['extra_comments']
				how_can_we_improve_survey = extra_section.cleaned_data['how_can_we_improve_survey']
				CommunityExtraRatings.objects.create(
					user=user, 
					community=community, 
					overall_rating=overall_rating, 
					extra_comments=extra_comments, 
					how_can_we_improve_survey=how_can_we_improve_survey
				)

			for games in community.occuring_games.all():
				if CommunityGameRatings.objects.filter(user=user, games=CommunityGames.objects.filter(communityinst=community, game=games)[0]): # Checks if the user has submitted a survey for the game
					raise ValidationError("You've already submitted this survey!")
				else: 
					game_rating = game_form_dict[games.name].cleaned_data['game_rating']
					game_comments = game_form_dict[games.name].cleaned_data['game_comments']
					CommunityGameRatings.objects.create(
						user=user, 
						games=CommunityGames.objects.filter(communityinst=community, game=games)[0], 
						game_rating=game_rating, 
						game_comments=game_comments
					)

			return HttpResponseRedirect(reverse('community-home', current_app='Community'))

	else:
		game_form_dict = dict()
		for games in community.occuring_games.all():
			game_form_dict[games.name] = CommunityGameRatingsForm(prefix='{}'.format(games.name))
		pacing_section = CommunityPacingRatingsForm()
		extra_section = CommunityExtraRatingsForm()

	return render(request, 'surveys/survey_community.html', {'community': community, 'game_form_dict': game_form_dict, 'user': user, 'pacing_section': pacing_section, 'extra_ratings': extra_section})

@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='accounts/login')
def add_community(request):
	CommunityGamesFormset = formset_factory(CommunityGamesCreationForm, extra=1)
	if request.method == 'POST':
		community_creation_form = CommunityInstanceCreationForm(request.POST)
		community_games = CommunityGamesFormset(request.POST, request.FILES)
		if community_games.is_valid():
			for tests in community_games.forms:
				print(tests)

	else:
		community_games = CommunityGamesFormset()
		community_creation_form = CommunityInstanceCreationForm()

	return render(request, 'surveys/add_community.html', {'com': community_creation_form, 'comgame': community_games})


def add_handler(request, form, field):
	if request.method == "POST":
		form = form(request.POST)
		if form.is_valid():
			
			try:
				add_object = form.save()

			except (forms.ValidationError, Error):
				add_object = None

			if add_object:
				return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "{}", "{}");</script>'.format(escape(add_object._get_pk_val()), escape(add_object)))
	else:
		form = form()
	return render(request, 'surveys/popup-form.html', {'form': form, 'field': field})


@login_required 
@user_passes_test(lambda u: u.groups.filter(name='Senators').exists(), login_url='accounts/login')
def add_game(request):
	return add_handler(request, GameCreationForm, 'game')

