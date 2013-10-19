# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from login.views import checkUserLogin

def getLecture(request, lecture_id):
	if request.method != 'GET': raise Http404

	checkUserLogin(request)
	lecture_id = int(lecture_id)

	try:
		lecture = Lecture.objects.get(id=lecture_id)
	except Lecture.DoesNotExist:
		raise Http500

	lectures = lecture.course.lecture_set.all()

	template = loader.get_template('lecture/lecture.html')
	context = RequestContext(request, {
		'l' : lectures,
		})
	return HttpResponse(template.render(context))
	
def commentLecture(request):
	# get a user
	# get a lecture
	# get a comment
	lecture_comment = LectureComment.objects.create()



