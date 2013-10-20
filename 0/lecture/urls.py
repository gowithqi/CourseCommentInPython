from django.conf.urls import patterns, url, include

from lecture import views

urlpatterns = patterns('',
	url(r'^(?P<lecture_id>\d+)/$', views.getLecture, name='lecture'),
	url(r'^recordscore/(?P<lecture_id>\d+)/$', views.recordStudentScore),
	url(r'^recordlevel/(?P<lecture_id>\d+)/$', views.recordLevel),
)
