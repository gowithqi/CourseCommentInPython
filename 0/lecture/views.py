# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User

def lecture(request):
	print "from hello"
	return HttpResponse("Hello! this is lecture")

def commentLecture(request):
	# get a user
	# get a lecture
	# get a comment
	lecture_comment = LectureComment.objects.create()



