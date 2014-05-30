from django.conf.urls import patterns, url, include

from login import views

urlpatterns = patterns('',
	url(r'^$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register/(?P<key>account|name)/(?P<content>.+)/$', views.checkAccountName),
	url(r'^register/checkuser/(?P<user_id>\d+)/(?P<check_code>\d+)/$', views.regCheckUser),
	url(r'^setpassword/$', views.setPassword),
	url(r'^setpassword/checkuser/(?P<user_id>\d+)/(?P<check_code>\d+)/$', views.setPwdCheckUser),
	url(r'^setpassword/newpassword/$', views.setNewPassword),
	url(r'^(?P<user_id>\d+)/$', views.userpage, name='userpage'),
	url(r'^sign/$', views.sign, name='sign'),
	url(r'^changepassword/$', views.changepassword),
	url(r'^test/$', views.test),
	# url(r'^login/$', views.login, name='login'),
	# url(r'^requestweightdata/(?P<user_id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.requestweightdata),
	# url(r'^submit/$', views.submit, name='submit')
)

