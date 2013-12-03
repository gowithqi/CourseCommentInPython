# -*- coding: utf-8 -*-
from datetime import datetime
import os

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from comment.models import MessageOfCommentSuper
from login.views import checkUserLogin
from comment.influence import increaseSysAchievement, updateUserInfluence

START_TIME = datetime(year=2013, month=11, day=1)
SUPER_VALUE = 10		# One SUPER equal how many days
MAX_COMMENTS_PER_USER = 3		# One user can comment a lecture at most ** times.
NUMBER_OF_WORDS = 100
COMMENT_SUPER_VALUE_INFLUENCE = 5
COMMENT_VALUE_INFLUENCE = 2

def super(request, comment_id):
	if request.method != 'GET': raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	comment_id = int(comment_id)
	comment = get_object_or_404(LectureComment, id=comment_id)
	try:
		victim = LectureCommentSuperRecord.objects.get(lecture_comment=comment, user=user)
		res = {"result": "您已经点过赞了", "comment": [1,2,3]}
		import json
		return HttpResponse(json.dumps(res, ensure_ascii=False))
	except LectureCommentSuperRecord.DoesNotExist:
		pass
	
	updateUserInfluence(comment.user, COMMENT_SUPER_VALUE_INFLUENCE)
	LectureCommentSuperRecord.objects.create(lecture_comment=comment, user=user)
	comment.super_number = comment.super_number + 1
	comment.rank_score = comment.rank_score + SUPER_VALUE*comment.super_weight
	comment.save()

	try:
		message = MessageOfCommentSuper.objects.get(user=comment.user, lecture_comment=comment)
		message.super_added = message.super_added+1
		message.save()
	except MessageOfCommentSuper.DoesNotExist:
		message = MessageOfCommentSuper.objects.create(user=comment.user, lecture_comment=comment)

	increaseSysAchievement()
	return HttpResponse("yes")

def deSuper(request, comment_id):
	if request.method != 'GET': raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	comment_id = int(comment_id)
	comment = get_object_or_404(LectureComment, id=comment_id)
	try:
		victim = LectureCommentSuperRecord.objects.get(lecture_comment=comment, user=user)
		victim.delete()
	except LectureCommentSuperRecord.DoesNotExist:
		raise Http404

	updateUserInfluence(comment.user, -1* COMMENT_SUPER_VALUE_INFLUENCE)
	comment.super_number = comment.super_number - 1
	comment.rank_score = comment.rank_score - SUPER_VALUE*comment.super_weight
	comment.save()

	try:
		message = MessageOfCommentSuper.objects.get(user=comment.user, lecture_comment=comment)
		if message.super_added == 1: message.delete()
		else: 
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

	if LectureComment.objects.filter(user=user, lecture=lecture).count() >= MAX_COMMENTS_PER_USER:
		return HttpResponse("You have comment too mant times")

	super_weight = getSuperWeight(request.POST['content'])

	lectureComment = LectureComment.objects.create(lecture=lecture, 
		user=user, 
		content=request.POST['content'], 
		rank_score=getRankScore(super_weight),
		super_weight=super_weight)
	updateUserInfluence(user, COMMENT_VALUE_INFLUENCE)
	return HttpResponse("yes")

def getRankScore(super_weight):
	now = datetime.now()
	delta_t = now - START_TIME
	time_factor = int(delta_t.total_seconds()/86400)

	return time_factor+SUPER_VALUE*super_weight

def getSuperWeight(content):
	if len(content) == 0: return 0
	import math
	return (0.9/math.pow(NUMBER_OF_WORDS, 1.0/3))*math.pow(getLength(content), 1.0/3)

# compute the number of effective word in the content
# eliminate the sucessive same word
def getLength(content):
	ret = 1
	tmpc = content[0]
	for c in content[1:]:
		if c != tmpc: 
			ret = ret + 1
			tmpc = c
	print "ret: ", ret
	return ret

def getTodayComments(request, check_code):
	print check_code
	from datetime import date
	today = date.today()
	safe_code = today.strftime("%Y%m%d") +"sjtucourse"
	print safe_code
	if (str(check_code) != safe_code) or not(request.session['user_id'] in [6, 14, 15]): raise Http404

	today = datetime(year=today.year, month=today.month, day=today.day)
	comments = LectureComment.objects.filter(time__gte=today)

	template = loader.get_template("comment/todaycomments.html")
	context = RequestContext(request, {
		'comments': comments,
		})

	return HttpResponse(template.render(context))

