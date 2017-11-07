from .models import Minutes
from django import forms

class MinutesForm(forms.ModelForm):
    class Meta:
        model = Minutes
        fields = '__all__'
        widgets = {
			'date': forms.DateInput(attrs={'class': 'datepicker'}),
		}
    