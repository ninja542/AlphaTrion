from django.db import models
from django.contrib.auth.models import User 


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

class SenateProjects(models.Model):
	date = models.DateField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_senators': True})



