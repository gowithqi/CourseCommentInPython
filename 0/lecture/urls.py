from django.conf.urls import patterns, url, include

from lecture import views

urlpatterns = patterns('',
	url(r'^$', views.lecture, name='lecture'),
	# url(r'^(?P<user_id>\d+)/$', views.userpage, name='userpage'),
	# url(r'^sign/$', views.sign, name='sign'),
	# url(r'^changepassword/$', views.changepassword),
	# url(r'^login/$', views.login, name='login'),
	# url(r'^requestweightdata/(?P<user_id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.requestweightdata),
	# url(r'^submit/$', views.submit, name='submit')
)

