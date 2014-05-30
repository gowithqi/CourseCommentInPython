from django.conf.urls import patterns, url, include

from search import views

urlpatterns = patterns('',
	url(r'^lecture/autocomplete/$', views.autoComplete),
	url(r'^lecture/$', views.searchLecture),
	url(r'^lecture/courseid/(?P<course_id>\d+)/$', views.searchLectureUsingCourseID),
)

