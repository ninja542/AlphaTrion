from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Questions(models.Model):
	question = models.CharField(max_length=200)


class CustomSurvey(models.Model):
	title = models.CharField(max_length=150)
	date = models.DateField()
	author = models.ForeignKey(User)
	questions = models.ManyToManyField(Questions, through='SurveyQuestions')

class SurveyQuestions(models.Model):
	survey = models.ForeignKey(CustomSurvey)
	question = models.ForeignKey(Questions)




