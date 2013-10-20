from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from login.views import checkUserLogin

def changeLecture(request):
	if request.method != 'GET': raise Http404

	checkUserLogin(request)
	lectures = Lecture.objects.order_by('?')[:3]
	res = ''
	for l in lectures:
		lurl = '/lecture/' + str(l.id)
		res = res + l.course.name + ':' + l.professor.name + ':' + str(l.level) + ':' + lurl + '/\n'
	res = res[:-1]

	return HttpResponse(res)


