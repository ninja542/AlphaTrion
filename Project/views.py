from django.shortcuts import render
from .forms import CustomSurveyForm
from .models import SenateProjects
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

def senate_project_survey(request, projectid):
	user = None
	if request.user.is_authenticated():
		user = request.user 
	if user:
		project = get_object_or_404(SenateProjects, pk=projectid)
		survey = project.survey

		if request.method == "POST":
			survey = CustomSurveyForm(request.POST, user=user, survey=survey)
			if survey.is_valid():
				survey.save()
				HttpResponseRedirect('/home/')
		else:
			survey = CustomSurveyForm(user=user, survey=survey)

	return render(request, 'senate-project-survey.html', {'survey': survey})


def projects_home(request):
	return render(request, 'projects-home.html')

def student_projects(request):
	return render(request, 'student-projects.html')

def senate_projects(request):
	senate_projects = SenateProjects.objects.all()
	return render(request, 'senate-projects.html', {'senate_projects': senate_projects})

def senate_project_specific(request, projectid):
	project = get_object_or_404(SenateProjects, pk=projectid)
	return render(request, 'senate-project-specific.html', {'project': project})

def student_project_specific(request):
	return render(request, 'student-project-specific.html')