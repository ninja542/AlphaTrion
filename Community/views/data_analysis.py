from __future__ import division	
from Community.forms import CommunityGameRatingsForm, CommunityPacingRatingsForm, CommunityExtraRatingsForm
from Community.models import CommunityInst, CommunityGameRatings, CommunityGames, CommunityPacingRatings, CommunityExtraRatings, Game
from bokeh.core.properties import Instance, String 
from bokeh.embed import components
from bokeh.io import show
from bokeh.models import ColumnDataSource, LayoutDOM
from bokeh.plotting import figure, output_file, show
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic 	
import numpy as np

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


@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def communityinstviewresults(request):
	"""
	Displays a list of all communities. 

	**Context**
	''communityinst''
		All Community objects

	**Template:**
	:template:'data_analysis/survey_result_list.html'
	"""

	communities = CommunityInst.objects.all()
	return render(request, 'data_analysis/survey_result_list.html', {'communityinst': communities})


@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def survey_results(request, communityid):
	"""
	Builds data structures to display for a individual community 

	**Context**
	''community''
		Community object
	
	''mean''
		Mean of all game ratings for all games in Community object 
	
	''game_ratings_dict'' 
		a list of all games formated {index, GameRatingObject} 
	
	''rating_correlation_list'' 
		a list of all games ratings with 'want to see again'
	
	''ramean'' 
		mean of rating_correlation_list

	**Template:**
	:template:'data_analysis/survey_specific_result.html'

	"""

	community = get_object_or_404(CommunityInst, pk=communityid)	
	game_rating_dict = dict()
	index = 0 
	for games in CommunityGames.objects.filter(communityinst=community):
		for instances in CommunityGameRatings.objects.filter(games=games):
			game_rating_dict[index] = instances 
			index += 1 

	mean = sum(game_rating_dict.values.game_rating)/ ( len(game_rating_dict.values) - 1 )  	

	rating_again_list = [r
	 for r,a in 
	 zip((game_rating_dict.values.game_rating, game_rating_dict.values.like_to_see_again)) 
	 if a == 'Yes']
	ramean = sum(rating_again_list) / ( len(rating_again_list) -1 ) 


	return render(request, 'data_analysis/survey_specific_result.html', 
		{'community': community, 'mean': mean, 'game_ratings_dict': game_rating_dict, 
		'rating_correlation_list': rating_again_list, 'ramean': ramean})


@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senators").exists(), login_url='/accounts/login')
def overall_survey_results(request):
	"""
	Builds data structures to display for all communities  

	**Context**
	''div''
		div of 3D Bokeh/Vis.js graph
	
	''script''
		Script of 3D Bokeh/Vis.js graph

	**Template:**
	:template:'data_analysis/survey_overall_results.html'
	"""

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

	return render(request, 'data_analysis/survey_overall_results.html', {'div': div, 'script': script})
