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
from comment.influence import updateUserInfluence
from cadmin.views import deleteComment, deleteGossip
from gossip.models import Gossip
from userpage.formatTime import formatTime
from userpage.models import MessageTopic, MessageWords
from userpage.models import Message, MessageOfCommentSupered, MessageOfGossipSupered, MessageOfMessageTopic

import json
import random
from datetime import datetime, date
MIN_LECTURE_ID = 6338
MAX_LECTURE_ID = 10479
COMMENT_CUT_LENGTH = 80

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
def getRandomComment(request, length):
	length = int(length)
	if length > COMMENT_CUT_LENGTH: raise Http404
	c = LectureComment.objects.order_by('?')[0]
	# c = LectureComment.objects.get(id=57)
	tmp = getCommentDict(c)
	if len(tmp['comment_content']) > length:
		tmp['comment_content'] = tmp['comment_content'][:length] + "..."
	tmp_l = getLectureDict(c.lecture)
	tmp['lecture'] = tmp_l

	return HttpResponse(json.dumps(tmp, ensure_ascii=False, indent=4))

@require_http_methods(['POST'])
def setNickname(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	user.name = request.POST['new_nickname']
	user.save()
	return HttpResponse("yes")

@require_http_methods(['POST'])
def setStyle(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	if not (str(request.POST['style']) in ['zzq', 'lyw']): raise Http404
	user.style = str(request.POST['new_nickname'])
	user.save()
	return HttpResponse("yes")

@require_http_methods(['GET'])
def freshUserInfluence(request):
	user_id = checkUserLogin(request)
	if int(user_id) != 14: raise Http404

	from comment.settings import COMMENT_SUPER_VALUE_INFLUENCE, COMMENT_VALUE_INFLUENCE
	from gossip.settings import GOSSIP_SUPER_VALUE_INFLUENCE
	for u in User.objects.all():
		t = u.influence_factor
		updateUserInfluence(u, (-1*t))
		tmp = 0
		for c in u.lecturecomment_set.all():
			tmp += COMMENT_VALUE_INFLUENCE
			tmp += c.lecturecommentsuperrecord_set.all().count() * COMMENT_SUPER_VALUE_INFLUENCE
		for g in u.gossip_set.all():
			tmp += g.gossipsuperrecord_set.all().count() * GOSSIP_SUPER_VALUE_INFLUENCE
		updateUserInfluence(u, tmp)
	return HttpResponse("yes")

@require_http_methods(['GET'])
def deleteRecord(request, record_type, id):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	record_type = str(record_type)
	if record_type == "comment":
		record = get_object_or_404(LectureComment, id=int(id))
		if record.user.id == user.id:
			deleteComment(int(id))
		else:
			raise Http404
	elif record_type == "gossip":
		record = get_object_or_404(Gossip, id=int(id))
		if record.user.id == user.id:
			deleteGossip(int(id))
		else:
			raise Http404
	else:
		raise Http404

	return HttpResponse("yes")

def getGossipDict(gossip):
	gossip_tmp = {}
	gossip_tmp['gossip_id'] = gossip.id
	gossip_tmp['gossip_user'] = gossip.user.name
	gossip_tmp['gossip_user_id'] = gossip.user.id
	gossip_tmp['gossip_content'] = gossip.content
	gossip_tmp['gossip_super_number'] = gossip.super_number
	gossip_tmp['gossip_time'] = formatTime(gossip.time)
	return gossip_tmp

def getCommentDict(comment):
	comment_tmp = {}
	comment_tmp['comment_id'] = comment.id
	comment_tmp['comment_user'] = comment.user.name
	comment_tmp['comment_user_id'] = comment.user.id
	comment_tmp['comment_content'] = comment.content
	comment_tmp['comment_super_number'] = comment.super_number
	comment_tmp['comment_time'] = formatTime(comment.time)
	return comment_tmp

def getLectureDict(l):
	tmp = {}
	tmp['id'] = l.id
	tmp['number'] = l.course.number
	tmp['course_name'] = l.course.name
	tmp['professor_name'] = l.professor.name
	tmp['level'] = "%.2f" % l.level
	return tmp

# return JSON message data 
@require_http_methods(['GET'])
def getMessages(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	messages = user.message_set.all()

	#get JSON data
	ret = [m.getDict() for m in messages]

	return HttpResponse(json.dumps(ret, ensure_ascii=False, indent=4))

@require_http_methods(['GET'])
def checkMessage(request, message_id):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	message = get_object_or_404(Message, id = message_id)	
	if message.message_type == 0:
		m = get_object_or_404(MessageOfCommentSupered, id = message.message_id)
		lecture_id = m.lecture_comment.lecture.id
		MessageOfCommentSupered.objects.delete(lecture_comment = m.lecture_comment)

		return HttpResponseRedirect(reverse("lecture", args=(lecture_id, )))
	elif message.message_type == 1:
		m = get_object_or_404(MessageOfGossipSupered, id = message.message_id)
		lecture_id = m.gossip.lecture.id
		MessageOfGossipSupered.objects.delete(gossip = m.gossip)

		return HttpResponseRedirect(reverse("lecture", args=(lecture_id, )))
	elif message.message_type == 2:
		m = get_object_or_404(MessageOfMessageTopic, id = message.message_id)
		m.delete()
		return HttpResponse("yes")
	else:
		pass

	return HttpResponse()

def sendMessageOfMessageTopic(message_topic, writer):
	users_id = [message_topic.user.id]
	users_id.extend([m.user.id for m in message_topic.messagewords_set.all()])
	readers = list(set(users_id))

	messages = [(user_id, MessageOfMessageTopic.objects.create(user = writer, message_topic = message_topic).id) for user_id in readers]
	Message.objects.bulk_create([Message(user=s[0], message_id=s[1]) for s in messages])
	return True
	
def sendMessageOfCommentSupered(lecture_comment, writer):
	m = MessageOfCommentSupered.objects.create(user = writer, lecture_comment = lecture_comment)
	Message.objects.create(user = lecture_comment.user, message_id = m.id)
	return True

def sendMessageOfGossipSupered(gossip, writer):
	m = MessageOfGossipSupered.objects.create(user = writer, gossip = gossip)
	Message.objects.create(user = gossip.user, message_id = m.id)
	return True

@require_http_methods(["POST"])
def newMessageTopic(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	mt = MessageTopic.objects.create(topic = request.POST['topic'], 
		user = user)
	return HttpResponse("yes")

@require_http_methods(["POST"])
def newMessageWords(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	message_topic = get_object_or_404(message_topic, id = request.POST['message_topic_id'])
	MessageWords.objects.create(message_topic=message_topic,
		content = request.POST['content'],
		user = user)

	sendMessage()
	return HttpResponse("yes")	