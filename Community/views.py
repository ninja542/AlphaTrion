from django.shortcuts import render
from django.views import generic 	
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import CommunityInst, CommunityGameRatings, CommunityGames, CommunityPacingRatings
from .forms import CommunityGameRatingsForm, CommunityPacingRatingsForm


class CommunityInstView(generic.ListView): 
	model = CommunityInst
	template_name = 'survey_list.html'

@login_required
@user_passes_test(lambda u: u.groups.filter(name="Senate Members").exists(), login_url='/community/home')
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
				#else:
					#CommunityPacingRatings.objects.create(user=user, community=community, pacing_rating=pacing_rating)

			for games in community.occuring_games.all():
				if CommunityGameRatings.objects.filter(user=user, games=CommunityGames.objects.filter(communityinst=community, game=games)[0]):
					raise ValidationError("You've already submitted this survey!")
				#else: 
				#	game_rating = game_form_dict[games.name].cleaned_data['game_rating']
				#	game_comments = game_form_dict[games.name].cleaned_data['game_comments']
					#CommunityGameRatings.objects.create(user=user, games=CommunityGames.objects.filter(communityinst=community, game=games)[0], game_rating=game_rating, game_comments=game_comments)
			return HttpResponseRedirect(reverse('community-home', current_app='Community'))

	else:
		game_form_dict = dict()
		for games in community.occuring_games.all():
			game_form_dict[games.name] = CommunityGameRatingsForm(prefix='{}'.format(games.name))
		pacing_section = CommunityPacingRatingsForm()

#	if not community.occuring_games.all():
#		return HttpResponseRedirect('/DBbroke/')

	return render(request, 'survey_community.html', {'community': community, 'game_form_dict': game_form_dict, 'user': user, 'pacing_section': pacing_section})


def survey_results(request, communityid):
	community = get_object_or_404(CommunityInst, pk=communityid)	
	game_rating_dict = dict()
	counter = 0
	total_sum = 0 
	for games in CommunityGames.objects.filter(communityinst=community):
		for instances in CommunityGameRatings.objects.filter(games=games):
			game_rating_dict[counter] = instances 
			total_sum += instances.game_rating
			counter += 1 

		mean = total_sum/counter

	return render(request, 'survey_specific_result.html', {'community': community, 'mean': mean, 'game_ratings_dict': game_rating_dict, })




