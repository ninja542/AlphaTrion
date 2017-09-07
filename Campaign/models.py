from django.db import models

# Create your models here.
class campaign_section(models.Model):
	title = models.CharField(max_length=20)
	OPTIONS = (
		('home', 'Senate Website'),
		('planned-policies', 'Planned Policies'),
		('personal-statement', 'Personal Statement'),
	)
	url = models.CharField(max_length=200, choices=OPTIONS)
	photo = models.ImageField(upload_to='Campaign/static/Campaign')
