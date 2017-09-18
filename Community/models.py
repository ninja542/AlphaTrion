from django.db import models
from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone
from s3direct.fields import S3DirectField
import uuid

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

# Games
class Game(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, default="No decription")
    estimated_length = models.PositiveIntegerField(help_text="Minutes", blank=False, default=10)
    number_of_participants = models.PositiveIntegerField(blank=False, default=1)
    
    def __str__(self):
        return "{}".format(self.name)

# Community
class CommunityInst(models.Model):
    date = models.DateField(default=timezone.now)
    spectrum_id = models.PositiveIntegerField(default=0)
    occuring_games = models.ManyToManyField(Game, through='CommunityGames')
    minutes_ended_early = models.PositiveIntegerField(blank=False, default=5)
    photo = S3DirectField(dest='community')


    def __str__(self):
        return"{}".format(self.date)
   
    class Meta:
        verbose_name = 'Community Instance'
        verbose_name_plural = 'Community Instances'
        ordering = ["-date"]


class CommunityGames(models.Model):
    communityinst = models.ForeignKey(CommunityInst, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Community Games'

    def __str__(self):
        return "{}".format(self.game)


# Review 
class CommunityGameRatings(models.Model):
    user = models.ForeignKey(User)
    games = models.ForeignKey(CommunityGames)

    game_rating = models.PositiveIntegerField(blank=False, choices=RATING_CHOICES, default=5)
    
    LIKE_TO_SEE_AGAIN = (
        ('y', 'Yes'),
        ('n', 'No')
    )

    like_to_see_again = models.CharField(max_length=1, choices=LIKE_TO_SEE_AGAIN, blank=False, default='n')
    game_comments = models.TextField(blank=True, null=True,)

    class Meta:
        verbose_name = 'Community Game Rating'
        verbose_name_plural = 'Community Game Ratings'

    def __str__(self):
        return "{}-{}".format(self.user, self.games)

class CommunityExtraRatings(models.Model):
    user = models.ForeignKey(User)
    community = models.ForeignKey(CommunityInst)
    overall_rating = models.PositiveIntegerField(blank=False, default=5, choices=RATING_CHOICES)
    extra_comments = models.TextField(blank=True)
    how_can_we_improve_survey = models.TextField(blank=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.community)

class CommunityPacingRatings(models.Model):
    user = models.ForeignKey(User)
    community = models.ForeignKey(CommunityInst)
    COMMUNITY_PACING_RATINGS = (
            ('v', 'Very Good'),
            ('g', 'Good'),
            ('d', 'Decent'),
            ('b', 'Bad'),
            ('h', 'Very Bad') # h for horrible
        )

    pacing_rating = models.CharField(max_length=20, choices=COMMUNITY_PACING_RATINGS, default='d')
    
    class Meta:
        verbose_name='Community Pacing Ratings'
        verbose_name_plural='Community Pacing Ratings'
    def __str__(self):
        return "{}-{}".format(self.user, self.community)

