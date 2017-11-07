from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^$', views.senate_home, name='senate-home'),
	url(r'^constitution/$', views.senate_constitution, name='senate-constitution'),
	url(r'^minutes/$', views.minutes, name='senate-minutes-home'),
	url(r'^addminutes/$', views.add_minutes, name='add-minutes'),
	url(r'^deleteminutes/(?P<minuteid>\d+)/$', views.delete_minutes, name='delete-minutes')
]