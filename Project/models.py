from django.db import models
from django.contrib.auth.models import User 
from s3direct.fields import S3DirectField

def get_first_name(self):
	return self.first_name

User.add_to_class("__str__", get_first_name)

class Questions(models.Model):
	"""
	Represents a single question
	"""
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
	"""
	Represents a single Survey,
	links to :model:'Project.Questions'
	links to :model:'auth.User'
	"""
	title = models.CharField(max_length=150)
	date = models.DateField()
	author = models.ForeignKey(User)
	questions = models.ManyToManyField(Questions, through='SurveyQuestions')

	def __str__(self):
		return self.title


class SurveyQuestions(models.Model):
	"""
	Represents connection between a survey and a question,
	links to :model:'Project.Questions'
	links to :model:'Project.CustomSurvey'
	"""
	survey = models.ForeignKey(CustomSurvey, null=True)
	question = models.ForeignKey(Questions)

	class Meta:
		verbose_name = 'Survey Question'
		verbose_name_plural = 'Survey Questions'
	def __str__(self):
		return ("{}-{}".format(self.survey.title, self.question.question))


class SurveyAnswers(models.Model):
	"""
	Represents connection between a survey and question and abstract for answer,
	links to :model:'Project.Questions'
	links to :model:'Project.CustomSurvey'
	"""
	survey = models.ForeignKey(CustomSurvey, null=True)
	question = models.ForeignKey(Questions)

	def __str__(self):
		return ("{}-{}".format(self.survey.title, self.question.question))


class AnswerInt(SurveyAnswers):
	"""
	Represents connection between a survey & question & user
	links to :model:'Project.Questions'
	links to :model:'Project.CustomSurvey'
	links to :model:'auth.User'
	"""
	user = models.ForeignKey(User)
	answer = models.IntegerField()

	class Meta:
		verbose_name = 'Integer Answers'
		verbose_name_plural = 'Integer Answers'
	
	def __str__(self):
		return ('{} {}-{}'.format(self.user.first_name, self.user.last_name, self.answer))


class AnswerText(SurveyAnswers):
	"""
	Represents connection between a survey & question & user
	links to :model:'Project.Questions'
	links to :model:'Project.CustomSurvey'
	links to :model:'auth.User'
	"""
	user = models.ForeignKey(User)
	answer = models.TextField()

	class Meta:
		verbose_name = 'Text Answers'
		verbose_name_plural = 'Text Answers'

	def __str__(self):
		return ('{} {}-{}'.format(self.user.first_name, self.user.last_name, self.answer))


class SenateProjects(models.Model):
	"""
	Represents a Senate project (and a connection to a survey)
	links to :model:'Project.CustomSurvey'
	links to :model:'auth.User'
	"""
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


class StudentProjects(models.Model):
	"""
	Represents a Student project (and a connection to a survey)
	links to :model:'Project.CustomSurvey'
	links to :model:'auth.User'
	"""
	title = models.CharField(max_length=200, null=True)
	author = models.ForeignKey(User, limit_choices_to={'groups__name': 'Students'})
	date = models.DateField()
	description = models.TextField(default='Insert description here')
	survey = models.ForeignKey(CustomSurvey, on_delete=models.CASCADE, blank=True, null=True)
	image = S3DirectField(dest='senateprojects', null=True)

	class Meta:
		verbose_name = 'Student Project'
		verbose_name_plural = 'Student Projects'

	def __str__(self):
		return self.title 