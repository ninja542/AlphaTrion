from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^$', views.senate_home, name='senate-home'),
	url(r'^constitution/$', views.senate_constitution, name='senate-constitution'),
	url(r'^minutes/$', views.minutes, name='senate-minutes-home'),
	url(r'^minutes/(?P<minutesid>\d+)/$', views.minutes_specific, name='senate-minutes-specific')
] 