# -*- coding: utf-8 -*-
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
import random
from datetime import datetime
MIN_LECTURE_ID = 6338
MAX_LECTURE_ID = 10479

def changeLecture(request):
	if request.method != 'GET': raise Http404

	checkUserLogin(request)
	random_id = [random.randrange(MIN_LECTURE_ID, MAX_LECTURE_ID) for i in range(2)]
	lectures = [Lecture.objects.get(id=id) for id in random_id]
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
	for c in user.lecturecomment_set.all().order_by('-time'):
		tmp = getCommentDict(c)
		l = c.lecture
		tmp_l = getLectureDict(l)
		tmp['lecture'] = tmp_l

		ret.append(tmp)

	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))

@require_http_methods(['GET'])
def getCollectionLectures(request, start, end):
	start = int(start)
	if start<1: raise Http500
	end = int(end)
	print "getCollectionLecture, start:%d, end:%d" % (start, end)
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	if end < start: collections = user.userlecturecollection_set.all()[start-1:]
	else: collections = user.userlecturecollection_set.all()[start-1: end]

	ret = []
	for cr in collections:
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
def getComments(request, start, end):
	start = int(start)
	if start<1: raise Http500	
	end = int(end)
	print "getCollectionLecture, start:%d, end:%d" % (start, end)
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	if end < start: comments = user.lecturecomment_set.all().order_by('-time')[start-1:]
	else: comments = user.lecturecomment_set.all().order_by('-time')[start-1: end]

	ret = []
	for c in comments:
		tmp = getCommentDict(c)
		l = c.lecture
		tmp_l = getLectureDict(l)
		tmp['lecture'] = tmp_l
		ret.append(tmp)

	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))

@require_http_methods(['GET'])
def getGossips(request, start, end):
	start = int(start)
	if start<1: raise Http500	
	end = int(end)
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	if end < start: gossips = user.gossip_set.all().order_by('-time')[start-1:]
	else: gossips = user.gossip_set.all().order_by('-time')[start-1: end]

	ret = []
	for g in gossips:
		tmp = getGossipDict(g)
		l = g.lecture
		tmp_l = getLectureDict(l)
		tmp['lecture'] = tmp_l
		ret.append(tmp)
	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))


@require_http_methods(['GET'])
def getRandomComment(request):
	c = LectureComment.objects.order_by('?')[0]
	tmp = getCommentDict(c)
	tmp_l = getLectureDict(c.lecture)
	tmp['lecture'] = tmp_l

	return HttpResponse(json.dumps(tmp, ensure_ascii=False, indent=4))

def getGossipDict(gossip):
	gossip_tmp = {}
	gossip_tmp['gossip_id'] = gossip.id
	gossip_tmp['gossip_user'] = gossip.user.name
	gossip_tmp['gossip_content'] = gossip.content
	gossip_tmp['gossip_super_number'] = gossip.super_number
	gossip_tmp['gossip_time'] = gossip.time.strftime("%Y-%m-%d %H:%M:%S")
	gossip_tmp['gossip_time_delta'] = computeTimeDelta(gossip.time)
	return gossip_tmp

def getCommentDict(comment):
	comment_tmp = {}
	comment_tmp['comment_id'] = comment.id
	comment_tmp['comment_user'] = comment.user.name
	comment_tmp['comment_content'] = comment.content
	comment_tmp['comment_super_number'] = comment.super_number
	comment_tmp['comment_time'] = comment.time.strftime("%Y-%m-%d %H:%M:%S")
	comment_tmp['comment_time_delta'] = computeTimeDelta(comment.time)
	return comment_tmp

def getLectureDict(l):
	tmp = {}
	tmp['id'] = l.id
	tmp['number'] = l.course.number
	tmp['course_name'] = l.course.name
	tmp['professor_name'] = l.professor.name
	tmp['level'] = l.level
	return tmp

def computeTimeDelta(i_time):
	t = datetime.now() - i_time

	t = t.total_seconds()   #second
	if t < 60: return str(int(t)) + u"秒"
	t = t / 60		#minute
	if t < 60: return str(int(t)) + u"分"
	t = t / 60		#hour
	if t < 24: return str(int(t)) + u"小时"
	t = t / 24		#day
	if t < 30: return str(int(t)) + u"天"
	t = t / 30 		#month
	if t < 12: return str(int(t)) + u"月"
	t = t / 12
	return str(int(t)) + u"年"