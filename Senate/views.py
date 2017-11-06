from django.shortcuts import render
from .models import Senator, Minutes

def senate_home(request):
	senator_list = Senator.objects.all()
	return render(request, 'senate-home.html', {'senator_list': senator_list})

def senate_constitution(request):
	return render(request, 'senate-constitution.html')

def minutes(request):
	minutes_list = Minutes.objects.all()
	return render(request, 'minutes.html', {'minutes': minutes_list})
