from django.conf.urls import patterns, url, include

from lecture import views

urlpatterns = patterns('',
	url(r'^(?P<lecture_id>\d+)/$', views.getLecture, name='lecture'),
	url(r'^recordscore/(?P<lecture_id>\d+)/$', views.recordStudentScore),
	url(r'^recordlevel/(?P<lecture_id>\d+)/$', views.recordLevel),
	url(r'^recordall/(?P<lecture_id>\d+)/$', views.recordAll),
	url(r'^getcourses/(?P<start>\d+)/(?P<end>\d+)/$', views.getCourses),
	url(r'^courselist/$', views.courselist),
	url(r'^test/(?P<mode>.+)/$', views.test),
	#url(r'^getlecturedata/(?P<lecture_id>\d+)/$', views.getLectureData),
)
