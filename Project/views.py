from django.shortcuts import render
from django.urls import reverse
from .forms import CustomSurveyForm
from .models import SenateProjects, StudentProjects, AnswerText, AnswerInt
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

def senate_project_survey(request, projectid):
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
			if AnswerText.objects.filter(user=user, survey=survey) or AnswerInt.objects.filter(user=user, survey=survey):
				raise ValidationError("You've already submitted this survey!")
			survey.save()
			return HttpResponseRedirect(reverse('senate-projects-home', current_app='Project'))

	else:
		survey = CustomSurveyForm(user=user, survey=survey)

	return render(request, 'senate-project-survey.html', {'survey': survey})


def projects_home(request):
	return render(request, 'projects-home.html')

def student_projects(request):
	student_projects = StudentProjects.objects.all()
	return render(request, 'student-projects.html', {'student_projects': student_projects})

def senate_projects(request):
	senate_projects = SenateProjects.objects.all()
	return render(request, 'senate-projects.html', {'senate_projects': senate_projects})

def senate_project_specific(request, projectid):
	project = get_object_or_404(SenateProjects, pk=projectid)
	return render(request, 'senate-project-specific.html', {'project': project})

def student_project_specific(request):
	return render(request, 'student-project-specific.html')