from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord, UserLectureCollection
from login.models import User
from login.views import checkUserLogin
from comment.models import MessageOfCommentSuper

import json
from datetime import datetime
def changeLecture(request):
	if request.method != 'GET': raise Http404

	checkUserLogin(request)
	lectures = Lecture.objects.order_by('?')[:2]
	res = ''
	ret = []
	ret.append(getALecture())
	for l in lectures:
		tmp = getLectureDict(l)
		tmp['most_popular_comment'] = ""
		comments = l.lecturecomment_set.all()
		if comments.count() > 0: 
			comment = comments[0]
			comment_tmp = getCommentDict(comment)
			tmp['most_popular_comment'] = comment_tmp

		ret.append(tmp)
		
	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))

def getALecture():
	l = Lecture.objects.get(id=10461)
	tmp = getLectureDict(l)
	tmp['most_popular_comment'] = ""
	comments = l.lecturecomment_set.all()
	if comments.count() > 0: 
		comment = comments[0]
		comment_tmp = getCommentDict(comment)
		tmp['most_popular_comment'] = comment_tmp
	return tmp

@require_http_methods(['GET'])
def collectLecture(request, collect_act, lecture_id):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	lecture = get_object_or_404(Lecture, id=int(lecture_id))

	if str(collect_act) == "collect":
		try: 
			UserLectureCollection.objects.get(user=user, lecture=lecture)
			return HttpResponse("You have collected")
		except UserLectureCollection.DoesNotExist:
			UserLectureCollection.objects.create(user=user, lecture=lecture)
	else:
		user_lecture_collection = get_object_or_404(UserLectureCollection, user=user, lecture=lecture)
		user_lecture_collection.delete()

	return HttpResponse("yes")

@require_http_methods(['GET'])
def checkSuperMessage(request, message_id):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	message_id = int(message_id)
	print message_id
	message = get_object_or_404(MessageOfCommentSuper, id=message_id)
	lecture_id = message.lecture_comment.lecture.id
	print lecture_id
	message.delete()

	return HttpResponseRedirect(reverse("lecture", args=(lecture_id, )))

@require_http_methods(['GET'])
def getAllCollectionLectures(request):
	print "getAllCollectionLecture"
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	ret = []
	for cr in user.userlecturecollection_set.all():
		l = cr.lecture
		tmp = getLectureDict(l)
		tmp['most_popular_comment'] = ""
		comments = l.lecturecomment_set.all()
		if comments.count() > 0: 
			comment = comments[0]
			comment_tmp = getCommentDict(comment)
			tmp['most_popular_comment'] = comment_tmp
		ret.append(tmp)

	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))

@require_http_methods(['GET'])
def getAllComments(request):
	print "getAllComments"
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	ret = []
	for c in user.lecturecomment_set.all():
		tmp = getCommentDict(c)
		l = c.lecture
		tmp_l = getLectureDict(l)
		tmp['lecture'] = tmp_l

		ret.append(tmp)

	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))

def getCommentDict(comment):
	comment_tmp = {}
	comment_tmp['comment_id'] = comment.id
	comment_tmp['comment_user'] = comment.user.name
	comment_tmp['comment_content'] = comment.content
	comment_tmp['comment_super_number'] = comment.super_number
	comment_tmp['comment_time'] = comment.time.strftime("%Y-%m-%d %H:%M:%S")
	return comment_tmp

def getLectureDict(l):
	tmp = {}
	tmp['id'] = l.id
	tmp['number'] = l.course.number
	tmp['course_name'] = l.course.name
	tmp['professor_name'] = l.professor.name
	tmp['level'] = l.level
	return tmp