from django.db import models
from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone
from s3direct.fields import S3DirectField
import uuid

def get_first_name(self):
	return self.first_name

User.add_to_class("__str__", get_first_name)


RATING_CHOICES = (
	(1, '1'),
	(2, '2'),
	(3, '3'), 
	(4, '4'),
	(5, '5'),
	(6, '6'),
	(7, '7'),
	(8, '8'),
	(9, '9'),
	(10, '10')  
)


class Game(models.Model):
	"""
	Represents a Community game
	"""
	name = models.CharField(max_length=250)
	description = models.TextField(blank=True, default="No description")
	estimated_length = models.PositiveIntegerField(help_text="Minutes", default=10)
	number_of_participants = models.PositiveIntegerField(default=1)
	
	def __str__(self):
		return "{}".format(self.name)

# Community
class CommunityInst(models.Model):
	"""
	Represents a single community, 
	links to :model:'Community.Game'
	links to :model:'Community.CommunityGames'
	"""
	date = models.DateField(default=timezone.now)
	spectrum_id = models.PositiveIntegerField(default=0)
	occuring_games = models.ManyToManyField(Game, through='CommunityGames')
	minutes_ended_early = models.PositiveIntegerField(default=5)
	photo = S3DirectField(dest='community')

	def __str__(self):
		return"{}".format(self.date)
   
	class Meta:
		verbose_name = 'Community Instance'
		verbose_name_plural = 'Community Instances'
		ordering = ["-date"]


class CommunityGames(models.Model):
	"""
	Links a community to a game, 
	links to :model:'Community.CommunityInst'
	links to :model:'Community.Game'
	"""
	communityinst = models.ForeignKey(CommunityInst, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Community Games'

	def __str__(self):
		return "{}".format(self.game)



class CommunityGameRatings(models.Model):
	"""
	Attaches a community's game to a user rating,
	links to :model:'auth.User' 
	links to :model:'Community.CommunityInst'
	links to :model:'Community.Game'
	links to :model:'Community.CommunityGames'
	"""
	user = models.ForeignKey(User)
	games = models.ForeignKey(CommunityGames)

	game_rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
	
	LIKE_TO_SEE_AGAIN = (
		('y', 'Yes'),
		('n', 'No')
	)

	like_to_see_again = models.CharField(max_length=1, choices=LIKE_TO_SEE_AGAIN, default='n')
	game_comments = models.TextField(blank=True, null=True,)

	class Meta:
		verbose_name = 'Community Game Rating'
		verbose_name_plural = 'Community Game Ratings'

	def __str__(self):
		return "{}-{}".format(self.user.first_name, self.games)

class CommunityExtraRatings(models.Model):
	"""
	Attaches a community's extras to a user rating,
	links to :model:'auth.User' 
	links to :model:'Community.CommunityInst'
	"""
	user = models.ForeignKey(User)
	community = models.ForeignKey(CommunityInst)
	overall_rating = models.PositiveIntegerField(default=5, choices=RATING_CHOICES)
	extra_comments = models.TextField(blank=True)
	how_can_we_improve_survey = models.TextField(blank=True)
	COMMUNITY_PACING_RATINGS = (
		('v', 'Very Good'),
		('g', 'Good'),
		('d', 'Decent'),
		('b', 'Bad'),
		('h', 'Very Bad') # h for horrible
	)

	pacing_rating = models.CharField(max_length=20, choices=COMMUNITY_PACING_RATINGS, default='d')

	class Meta:
		verbose_name='Community Extra Ratings'
		verbose_name_plural='Community Extra Ratings'

	def __str__(self):
		return "{}-{}".format(self.user.first_name, self.community)



# Temporary Storage in case of bad things
# class CommunityPacingRatings(models.Model):
# 	"""
# 	Attaches a community's extras to a user rating (to be merged into extras),
# 	links to :model:'auth.User' 
# 	links to :model:'Community.CommunityInst'
# 	"""
# 	user = models.ForeignKey(User)
# 	community = models.ForeignKey(CommunityInst)
# 	COMMUNITY_PACING_RATINGS = (
# 			('v', 'Very Good'),
# 			('g', 'Good'),
# 			('d', 'Decent'),
# 			('b', 'Bad'),
# 			('h', 'Very Bad') # h for horrible
# 		)

# 	pacing_rating = models.CharField(max_length=20, choices=COMMUNITY_PACING_RATINGS, default='d')
	
# 	class Meta:
# 		verbose_name='Community Pacing Ratings'
# 		verbose_name_plural='Community Pacing Ratings'
# 	def __str__(self):
# 		return "{}-{}".format(self.user.first_name, self.community)

