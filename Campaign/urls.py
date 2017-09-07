from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^$', views.home_view, name='campaign-home'),
	url(r'^campaign/personalstatement/$', views.personal_statement_view, name='personal-statement'),
	url(r'^campaign/plannedpolicies/$', views.planned_policies_view, name='planned-policies'),

]