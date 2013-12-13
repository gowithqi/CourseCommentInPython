from django.conf.urls import patterns, url, include

from manageDB import views

urlpatterns = patterns('',
	url(r'^updatelecture/$', views.updateLecture),
	url(r'^addtongshike/$', views.addTongShiKe),
	#url(r'^getlecturedata/(?P<lecture_id>\d+)/$', views.getLectureData),
)
