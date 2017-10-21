from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):

	class Meta:
		model = Announcement
		fields = '__all__'
		widgets = {
			'occuring_date': forms.DateInput(attrs={'class': 'datepicker'}),
		}
