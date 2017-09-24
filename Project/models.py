from django.db import models
from django.contrib.auth.models import User 
from s3direct.fields import S3DirectField

class Questions(models.Model):
	# Based on https://github.com/jessykate/django-survey/blob/master/survey/models.py
	TEXT = 'TEXT'
	INTEGER = 'INTEGER'
	QUESTION_TYPES = (
		(TEXT, 'text'),
		(INTEGER, 'integer') 
		
	)

	question = models.CharField(max_length=200)
	required = models.BooleanField(default=True)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=INTEGER)

	def __str__(self):
		return self.question

	class Meta:
		verbose_name = 'Question'
		verbose_name_plural = 'Questions'



class CustomSurvey(models.Model):
	title = models.CharField(max_length=150)
	date = models.DateField()
	author = models.ForeignKey(User)
	questions = models.ManyToManyField(Questions, through='SurveyQuestions')

	def __str__(self):
		return self.title


class SurveyQuestions(models.Model):
	survey = models.ForeignKey(CustomSurvey, null=True)
	question = models.ForeignKey(Questions)

	class Meta:
		verbose_name = 'Survey Question'
		verbose_name_plural = 'Survey Questions'


class SurveyAnswers(models.Model):
	survey = models.ForeignKey(CustomSurvey, null=True)
	question = models.ForeignKey(Questions)

class AnswerInt(SurveyAnswers):
	user = models.ForeignKey(User)
	answer = models.IntegerField()

	class Meta:
		verbose_name = 'Integer Answers'
		verbose_name_plural = 'Integer Answers'


class AnswerText(SurveyAnswers):
	user = models.ForeignKey(User)
	answer = models.TextField()

	class Meta:
		verbose_name = 'Text Answers'
		verbose_name_plural = 'Text Answers'


class SenateProjects(models.Model):
	title = models.CharField(max_length=200, null=True)
	author = models.ForeignKey(User, limit_choices_to={'groups__name': 'Senators'})
	date = models.DateField()
	description = models.TextField(default='insert description here!')
	survey = models.ForeignKey(CustomSurvey, on_delete=models.CASCADE, blank=True, null=True)
	image = S3DirectField(dest='senateprojects', null=True)

	class Meta:
		verbose_name = 'Senate Project'
		verbose_name_plural = 'Senate Projects'

	def __str__(self):
		return self.title