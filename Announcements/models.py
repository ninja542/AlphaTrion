from django.db import models
from django.contrib.auth.models import User 


class Announcement(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(User, limit_choices_to={'groups__name': 'Senators'})
	short_description = models.CharField(max_length=3000)
	occuring_date = models.DateField(blank=True)

	class Meta:
		ordering=['occuring_date']
