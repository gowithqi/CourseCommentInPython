from django.conf.urls import patterns, url, include

from cadmin import views

urlpatterns = patterns('',
	url(r'^$', views.cadmin),
	url(r'^contents/$', views.getContent),
	url(r'^delete/$', views.deleteRecord),
	#url(r'^gossips/(?P<start_date>.+)/(?P<end_date>.+)/$', views.getGossips),
)
