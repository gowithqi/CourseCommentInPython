from django.conf.urls import patterns, url, include

from userpage import views

urlpatterns = patterns('',
	url(r'^change/$', views.changeLecture),
	url(r'^(?P<collect_act>collect|decollect)/lecture/(?P<lecture_id>\d+)/', views.collectLecture),
)

