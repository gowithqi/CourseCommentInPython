from django.conf.urls import patterns, url, include

from login import views

urlpatterns = patterns('',
	url(r'^$', views.login, name='login'),
	# url(r'^login/$', views.login, name='login'),
	# url(r'^requestweightdata/(?P<user_id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.requestweightdata),
	# url(r'^submit/$', views.submit, name='submit')
)

