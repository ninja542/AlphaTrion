from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^$', views.projects_home, name='projects-home'),
	url(r'^senateprojects/$', views.senate_projects, name='senate-projects-home'),
	url(r'^senateprojects/(?P<projectid>\d+)/$', views.senate_project_specific, name='senate-project-specific'),
	url(r'^studentprojects/$', views.student_projects, name='student-projects-home'),
	url(r'^studentprojects/(?P<projectid>\d+)/$', views.student_project_specific, name='student-project-specific'),
	url(r'^senateprojects/survey/(?P<projectid>\d+)/$', views.senate_project_survey, name='senate-project-survey'),
]