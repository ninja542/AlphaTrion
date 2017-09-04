from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^$', views.CommunityInstView.as_view(), name='community-home'),
	url(r'^communitysurvey/(?P<communityid>\d+)/(?P<userid>\d+)/$', views.review_community_instance, name='community-review'),
	url(r'^communitysurveyresults/(?P<communityid>\d+)/$', views.survey_results, name='community-results-specific'),
	url(r'^communitysurveyresults/$', views.communityinstviewresults, name='community-results'),
]