def host_score(overall_rating_list, pacing_rating_list):
	overall_rating_average = sum(overall_rating_list)/len(overall_rating_list)
	pacing_rating_average = sum(pacing_rating_list)/len(pacing_rating_list)

	if not pacing_rating_average:
		return overall_rating_average
	else:
		return overall_rating_average/pacing_rating_average

def game_likeability(game_rating_list, see_again_list):
	game_average = sum(game_rating_list)/len(game_rating_list) 
	see_again_average = sum(see_again_list)/len(see_again_list)
	return game_average * see_again_average