from django.shortcuts import render
from .models import SenateProjects

def projects_home(request):
	return render(request, 'projects-home.html')

def student_projects(request):
	return render(request, 'student-projects.html')

def senate_projects(request):
	senate_projects = SenateProjects.objects.all()
	return render(request, 'senate-projects.html', {'senate-projects': senate_projects})

def senate_project_specific(request):
	return render(request, 'senate-project-specific.html')

def student_project_specific(request):
	return render(request, 'student-project-specific.html')