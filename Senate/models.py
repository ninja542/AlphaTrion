from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Senator(models.Model):
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

	name = models.CharField(max_length=140, default='OmegaSupreme')
	grade = models.PositiveIntegerField(choices=GRADE_LEVEL_CHOICES)
	email = models.EmailField(max_length=254)
	photo = models.ImageField(upload_to='Senate/static/Senate/', default='static/Senate/Senate.jpg')