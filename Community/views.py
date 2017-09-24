from __future__ import division	
import numpy as np
from django.shortcuts import render
from django.views import generic 	
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.models import Group
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.core.properties import Instance, String 
from bokeh.models import ColumnDataSource, LayoutDOM
from bokeh.io import show
from .models import CommunityInst, CommunityGameRatings, CommunityGames, CommunityPacingRatings, CommunityExtraRatings, Game
from .forms import CommunityGameRatingsForm, CommunityPacingRatingsForm, CommunityExtraRatingsForm
JS_CODE = """ 
	# Taken from https://bokeh.pydata.org/en/latest/docs/user_guide/extensions_gallery/wrapping.html

	import * as p from "core/properties"
	import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"

	OPTIONS = 
	  width:  '600px'
	  height: '600px'
	  style: 'dot-line'
	  showPerspective: true
	  showGrid: true
	  keepAspectRatio: false
	  verticalRatio: 1.0
	  legendLabel: 'stuff'
	  showlegend: true
	  xLabel: 'Number of Participants'
	  yLabel: 'Length Of Game'
	  zLabel: 'Overall Rating'
	  cameraPosition:
	    horizontal: -0.35
	    vertical: 0.22
	    distance: 1.8

	export class Surface3dView extends LayoutDOMView
	  initialize: (options) ->
	    super(options)

	    url = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"

	    script = document.createElement('script')
	    script.src = url
	    script.async = false
	    script.onreadystatechange = script.onload = () => @_init()
	    document.querySelector("head").appendChild(script)

	  _init: () ->
	    @_graph = new vis.Graph3d(@el, @get_data(), OPTIONS)
	    @connect(@model.data_source.change, () =>
	        @_graph.setData(@get_data())
	    )

	  get_data: () ->
	    data = new vis.DataSet()
	    source = @model.data_source
	    for i in [0...source.get_length()]
	      data.add({
	        x:     source.get_column(@model.x)[i]
	        y:     source.get_column(@model.y)[i]
	        z:     source.get_column(@model.z)[i]
	        style: source.get_column(@model.color)[i]
	      })
	    return data


	export class Surface3d extends LayoutDOM
	  default_view: Surface3dView
	  type: "Surface3d"


	  @define {
	    x:           [ p.String           ]
	    y:           [ p.String           ]
	    z:           [ p.String           ]
	    color:       [ p.String           ]
	    data_source: [ p.Instance         ]
	  }
	"""
class Surface3d(LayoutDOM):
	'''This is taken from the Surface 3d example on bokeh'''
	__implementation__ = JS_CODE
	data_source = Instance(ColumnDataSource)
	x = String
	y = String
	z = String
	color = String

class CommunityInstView(generic.ListView): 
	model = CommunityInst
	template_name = 'survey_list.html'

@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def communityinstviewresults(request):
	communities = CommunityInst.objects.all()
	return render(request, 'survey_result_list.html', {'communityinst': communities})


#def handler400(request):
#	return render(request, '404.html', status=404)

def review_community_instance(request, communityid, userid):
	user = get_object_or_404(User, pk=userid) 
	community = get_object_or_404(CommunityInst, pk=communityid)
	
	if request.method == "POST":
		game_valid = False 
		pacing_valid = False 

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
				CommunityExtraRatings.objects.create(user=user, community=community, overall_rating=overall_rating, extra_comments=extra_comments, how_can_we_improve_survey=how_can_we_improve_survey)

			for games in community.occuring_games.all():
				if CommunityGameRatings.objects.filter(user=user, games=CommunityGames.objects.filter(communityinst=community, game=games)[0]):
					raise ValidationError("You've already submitted this survey!")
				else: 
					game_rating = game_form_dict[games.name].cleaned_data['game_rating']
					game_comments = game_form_dict[games.name].cleaned_data['game_comments']
					CommunityGameRatings.objects.create(user=user, games=CommunityGames.objects.filter(communityinst=community, game=games)[0], game_rating=game_rating, game_comments=game_comments)
			return HttpResponseRedirect(reverse('community-home', current_app='Community'))

	else:
		game_form_dict = dict()
		for games in community.occuring_games.all():
			game_form_dict[games.name] = CommunityGameRatingsForm(prefix='{}'.format(games.name))
		pacing_section = CommunityPacingRatingsForm()
		extra_section = CommunityExtraRatingsForm()

#	if not community.occuring_games.all():
#		return HttpResponseRedirect('/DBbroke/')

	return render(request, 'survey_community.html', {'community': community, 'game_form_dict': game_form_dict, 'user': user, 'pacing_section': pacing_section, 'extra_ratings': extra_section})

@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def survey_results(request, communityid):

	community = get_object_or_404(CommunityInst, pk=communityid)	
	game_rating_dict = dict()
	counter = 0
	index = 0
	total_sum = 0 
	for games in CommunityGames.objects.filter(communityinst=community):
		for instances in CommunityGameRatings.objects.filter(games=games):
			game_rating_dict[counter] = instances 
			total_sum += instances.game_rating
			counter += 1 
	mean = total_sum/counter 
	z = []
	x = []
	y = []
	for games in game_rating_dict.values():
		z.append(games.game_rating)
	for games in game_rating_dict.values():
		x.append(games.games.game.number_of_participants)
	for games in game_rating_dict.values():
		y.append(games.games.game.estimated_length)
	value = z
	source = ColumnDataSource(data=dict(x=x, y=y, z=value, color=value))
	surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)
	script, div = components(surface)

	return render(request, 'survey_specific_result.html', {'community': community, 'mean': mean, 'game_ratings_dict': game_rating_dict, 'script': script, 'div': div})


def overall_survey_results(request):
	z = [] 
	x = [] 
	y = [] 

	for games in CommunityGameRatings.objects.all():
		z.append(games.game_rating)
	for games in CommunityGameRatings.objects.all():
		x.append(games.games.game.number_of_participants)
	for games in CommunityGameRatings.objects.all():
		y.append(games.games.game.estimated_length)
	value = z 
	source = ColumnDataSource(data=dict(x=x, y=y, z=value, color=value))
	surface = Surface3d(x='x', y='y', z='z', color='color', data_source=source)
	script, div = components(surface)

	return render(request, 'survey_overall_results.html', {'div': div, 'script': script})
