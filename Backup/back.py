from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _ 
import uuid


class Game(models.Model):
	name = models.CharField(max_length=200, default='None', blank=False, null=True)
	description = models.TextField(default='Describe the Game Here!', blank=False, null=True)
	number_of_participants = models.PositiveIntegerField(verbose_name='Number Of Participants', blank=False, null=True)
	estimated_length = models.PositiveIntegerField(verbose_name='Estimated Length', default=10, blank=False, help_text='Minutes')
	communities = models.ManyToManyField(CommunityInstance )

	def __str__(self):
		return '{}'.format(self.name)


class Talent(models.Model):
	name = models.CharField(primary_key=True, max_length=200, help_text='Use what was done, Piano, Story, Violion, Etc', blank=False)
	description = models.TextField(default='Describe the talent here!', blank=True, null=True)
	author = models.CharField(max_length=200, help_text='Name the Preformer (optional)', blank=True, null=True)
	
	def __str__(self):
		return '{}'.format(self.name)

class CommunityInstance(models.Model):
	id = models.SlugField(primary_key=True, default=uuid.uuid4, unique=True)
	date = models.DateField(blank=False)

	number_of_games = models.PositiveIntegerField(blank=False, default=1)
	games = models.ManyToManyField(Game, help_text='Select the games that appeard this community!', blank=True)
	
	number_of_announcements = models.PositiveIntegerField(default=3, blank=False)
	length_of_announcements = models.PositiveIntegerField(default=10, help_text='minutes') 
	announcements_made = models.TextField()
	
	host = models.CharField(max_length=20) 
	
	number_of_talent = models.PositiveIntegerField(blank=False, verbose_name="Number of Student Preformances")
	talent = models.ManyToManyField(Talent, blank=True, help_text='Enter all the talent that was preformed, if there was no talent preformed, don\'t select anything. If the talent that was preformed is not listed, use the + button to add it to the list.')

	number_of_it_awards = models.PositiveIntegerField(blank=False, default=0, verbose_name='Independent Thinker Awards')
	number_of_pc_awards = models.PositiveIntegerField(blank=False, default=0, verbose_name='Profiles in Courage Awards')
	number_of_ds_awards = models.PositiveIntegerField(blank=False, default=0, verbose_name='Durkheim Scholar Awards')
	number_of_gp_awards = models.PositiveIntegerField(blank=False, default=0, verbose_name='Gary Phillips Awards')

	minutes_end_early = models.PositiveIntegerField(default=15, help_text='in minutes', verbose_name="Minutes Left When Community Ended")

	class Meta:
		verbose_name = 'Community Instance'
		verbose_name_plural = 'Community Instances'

	def __str__(self):
		return '{}'.format(self.date)


class CommunityInstanceReview(models.Model):
	user = models.ForeignKey(User, blank=False)
	community = models.ForeignKey(CommunityInstance, blank=False)