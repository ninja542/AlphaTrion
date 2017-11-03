from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
	"""
	Form to create an announcement object from :model:'Announcements.Announcement'
	"""
	
	class Meta:
		model = Announcement
		fields = '__all__'
		widgets = {
			'occuring_date': forms.DateInput(attrs={'class': 'datepicker'}),
		}
