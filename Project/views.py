from django.shortcuts import render
from .models import 

def projects_home(request):
	return render(request, 'projects-home.html')

def senate_projects(request):
	return render(request, 'senate-projects.html', {'senate-projects': })