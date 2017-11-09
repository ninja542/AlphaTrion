from django.shortcuts import render
from django.urls import reverse
from .forms import CustomSurveyForm
from .models import SenateProjects, StudentProjects, AnswerText, AnswerInt
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

def senate_project_survey(request, projectid):
	"""
	Generalized view for a custom senate project survey

	**Context**
	''survey''
		CustomSurvey form that is related to the project
	
	**Template:**
	:template:'senate-project-survey.html'
	
	"""
	user = None
	if request.user.is_authenticated():
		user = request.user 
	
	if not user:
		return request(request, 'not_logged_in.html')

	project = get_object_or_404(SenateProjects, pk=projectid)
	survey = project.survey

	if request.method == "POST":
		survey = CustomSurveyForm(request.POST, user=user, survey=survey)
		if survey.is_valid():
			survey.save()
			return HttpResponseRedirect(reverse('senate-projects-home', current_app='Project'))

	else:
		survey = CustomSurveyForm(user=user, survey=survey)

	return render(request, 'senate-project-survey.html', {'survey': survey})


def projects_home(request):
	"""
	Home view for all projects (Depreciated, soon to be made into drop down)
	
	**Template:**
	:template:'projects-home.html'
	
	"""
	return render(request, 'projects-home.html')

def student_projects(request):
	"""
	Home view for all student projects

	**Context**
	''student_projects''
		All projects from the studentprojects model
	
	**Template:**
	:template:'student-projects.html'
	
	"""
	student_projects = StudentProjects.objects.all()
	return render(request, 'student-projects.html', {'student_projects': student_projects})

def senate_projects(request):
	"""
	Home view for all senate projects

	**Context**
	''student_projects''
		All projects from the senateprojects model 
	
	**Template:**
	:template:'senate-projects.html'
	
	"""
	senate_projects = SenateProjects.objects.all()
	return render(request, 'senate-projects.html', {'senate_projects': senate_projects})

def senate_project_specific(request, projectid):
	"""
	Generalized view for a senate project

	**Context**
	''project''
		A specific senate project object
	
	**Template:**
	:template:'senate-project-specific.html'
	
	"""
	project = get_object_or_404(SenateProjects, pk=projectid)
	return render(request, 'senate-project-specific.html', {'project': project})

def student_project_specific(request):
	"""
	Generalized view for a senate project

	**Context**
	''project''
		A specific senate project object
	
	**Template:**
	:template:'senate-project-specific.html'
	
	"""
	return render(request, 'student-project-specific.html')