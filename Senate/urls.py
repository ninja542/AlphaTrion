from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^$', views.senate_home, name='senate-home'),
	url(r'^constitution/$', views.senate_constitution, name='senate-constitution')
]