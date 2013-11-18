from django.conf.urls import patterns, url, include

from comment import views, updateCommentData

urlpatterns = patterns('',
	url(r'^super/(?P<comment_id>\d+)/$', views.super),
	url(r'^desuper/(?P<comment_id>\d+)/$', views.deSuper),
	url(r'^lecture/(?P<lecture_id>\d+)/$', views.commentLecture),
	url(r'^gettoday/(?P<check_code>.*)/$', views.getTodayComments),
	url(r'^update/$', updateCommentData.updateCommentData),
)
