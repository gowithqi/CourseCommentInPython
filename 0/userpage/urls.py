from django.conf.urls import patterns, url, include

from userpage import views

urlpatterns = patterns('',
	url(r'^change/$', views.changeLecture),
	url(r'^(?P<collect_act>collect|decollect)/lecture/(?P<lecture_id>\d+)/$', views.collectLecture),
	url(r'^checksupermessage/(?P<message_id>\d+)/$', views.checkSuperMessage),
	url(r'^getallcollectionlectures/$', views.getAllCollectionLectures),
	url(r'^getallcomments/$', views.getAllComments),
	url(r'^getcollectionlectures/(?P<start>\d+)/(?P<end>\d+)/$', views.getCollectionLectures),
	url(r'^getcomments/(?P<start>\d+)/(?P<end>\d+)/$', views.getComments),
	url(r'^getgossips/(?P<start>\d+)/(?P<end>\d+)/$', views.getGossips),
	url(r'^getrandomcomment/$', views.getRandomComment),
	url(r'^setnickname/$', views.setNickname),
)

