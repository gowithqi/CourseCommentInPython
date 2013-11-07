from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from comment.models import MessageOfCommentSuper
from login.views import checkUserLogin


def super(request, comment_id):
	if request.method != 'GET': raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	user.influence_factor = user.influence_factor+1 			#influence factor caculation need to be discussed
	comment_id = int(comment_id)
	comment = get_object_or_404(LectureComment, id=comment_id)
	try:
		victim = LectureCommentSuperRecord.objects.get(lecture_comment=comment, user=user)
		return HttpResponse("have supered")
	except LectureCommentSuperRecord.DoesNotExist:
		pass

	LectureCommentSuperRecord.objects.create(lecture_comment=comment, user=user)
	comment.super_number = comment.super_number + 1
	comment.save()

	try:
		message = MessageOfCommentSuper.objects.get(user=comment.user, lecture_comment=comment)
		message.super_added = message.super_added+1
		message.save()
	except MessageOfCommentSuper.DoesNotExist:
		message = MessageOfCommentSuper.objects.create(user=comment.user, lecture_comment=comment)

	return HttpResponse("yes")

def deSuper(request, comment_id):
	if request.method != 'GET': raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	user.influence_factor = user.influence_factor-1				#influence factor
	comment_id = int(comment_id)
	comment = get_object_or_404(LectureComment, id=comment_id)
	try:
		victim = LectureCommentSuperRecord.objects.get(lecture_comment=comment, user=user)
		victim.delete()
	except LectureCommentSuperRecord.DoesNotExist:
		raise Http404
	comment.super_number = comment.super_number - 1
	comment.save()

	try:
		message = MessageOfCommentSuper.objects.get(user=comment.user, lecture_comment=comment)
		message.super_added = message.super_added-1
		message.save()
	except MessageOfCommentSuper.DoesNotExist:
		raise Http404

	return HttpResponse("yes")

def commentLecture(request, lecture_id):
	if request.method != "POST": raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
	lectureComment = LectureComment.objects.create(lecture=lecture, user=user, content=request.POST['content'])

	return HttpResponse("yes")



