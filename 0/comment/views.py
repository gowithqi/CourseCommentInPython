from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from login.views import checkUserLogin

def super(request, comment_id):
	if request.method != 'GET': raise Http404

	checkUserLogin(request)
	user = get_object_or_404(User, id=request.session['user_id'])
	comment_id = int(comment_id)
	comment = get_object_or_404(LectureComment, id=comment_id)
	LectureCommentSuperRecord.objects.create(lectureComment=comment, user=user)
	comment.super_number = comment.super_number + 1
	comment.save()

	return HttpResponse()

def deSuper(request, comment_id):
	if request.method != 'GET': raise Http404

	checkUserLogin(request)
	user = get_object_or_404(User, id=request.session['user_id'])
	comment_id = int(comment_id)
	comment = get_object_or_404(LectureComment, id=comment_id)
	try:
		victim = LectureCommentSuperRecord(lectureComment=comment, user=user)
		victim.delete()
	except LectureCommentSuperRecord.DoesNotExist:
		raise Http404

	return HttpResponse()

def commentLecture(request, lecture_id):
	if request.method != "POST": raise Http404

	checkUserLogin(request)
	user = get_object_or_404(User, id=request.session['user_id'])
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
	lectureComment = LectureComment.objects.create(lecture=lecture, user=user, content=request.POST['content'])

	return HttpResponse("yes")



