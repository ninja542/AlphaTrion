from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from s3direct.fields import S3DirectField

class Senator(models.Model):
	"""
	Model to store a senator
	"""
	GRADE_LEVEL_CHOICES = (
		(9, '9'),
		(10, '10'),
		(11, '11'),
		(12, '12')
	)

	POSITION = (
		('President', 'President'),
		('Vice-President', 'Vice-President'),
		('Secretary', 'Secretary'),
		('Senator', 'Senator')
	)

	name = models.CharField(max_length=140, default='AlphaTrion')
	grade = models.PositiveIntegerField(choices=GRADE_LEVEL_CHOICES)
	email = models.EmailField(max_length=254)
	position = models.CharField(max_length=14, choices=POSITION, default='Senator')
	photo = S3DirectField(dest='images')
	def __str__(self):
		return self.name
		
	class Meta:
		ordering = ["-grade", "name"]

class Minutes(models.Model):
	"""
	Model to store a minute
	"""
	date = models.DateField()
	embed_link = models.TextField(default=r'Link Goes Here!', 
		help_text='To get a embed link goto file -> publish to web -> embed -> copy the link into here')
	

	def __str__(self):
		return self.date

	class Meta:
		verbose_name = 'Minute'
		verbose_name_plural = 'Minutes'
		ordering = ["-date"]


	
