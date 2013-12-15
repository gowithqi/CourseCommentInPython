from django.conf.urls import patterns, url, include

from manageDB import views

urlpatterns = patterns('',
	url(r'^updatelecture/(?P<f>.+)/(?P<start>\d+)/(?P<end>\d+)/$', views.updateLecture),
	url(r'^addtongshike/$', views.addTongShiKe),
	#url(r'^getlecturedata/(?P<lecture_id>\d+)/$', views.getLectureData),
)
