# -*- coding: utf-8 -*-
from datetime import datetime, date
import os

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from gossip.models import Gossip, GossipSuperRecord
from login.models import User
from comment.models import MessageOfCommentSuper
from login.views import checkUserLogin
from comment.influence import increaseSysAchievement, updateUserInfluence
from comment.settings import COMMENT_VALUE_INFLUENCE, COMMENT_SUPER_VALUE_INFLUENCE
from gossip.settings import GOSSIP_SUPER_VALUE_INFLUENCE

ADMINS = [6, 14, 15, 16]
START_DATE = datetime.strptime("20131101", "%Y%m%d")
TODAY = date.today()
TODAY = datetime(year=TODAY.year, month=TODAY.month, day=TODAY.day)

@require_http_methods(['GET'])
def cadmin(request):
	if not (request.session['user_id'] in ADMINS): raise Http404
	template = loader.get_template("cadmin/cadmin.html")
	context = RequestContext(request, {
		"user_number": User.objects.all().count(),
		"formal_user_number": User.objects.filter(formal=True).count(),
		"comment_number": LectureComment.objects.all().count(),
		"gossip_number": Gossip.objects.all().count()
		})

	return HttpResponse(template.render(context))

@require_http_methods(['GET'])
def getContent(request):
	if not (request.session['user_id'] in ADMINS): raise Http404
	start_date = str(request.GET['start_date'])
	end_date = str(request.GET['end_date'])
	if start_date == "": start_date = TODAY
	else: start_date = datetime.strptime(start_date, "%Y%m%d")
	if end_date == "": end_date = datetime.now()
	else: end_date = datetime.strptime(end_date, "%Y%m%d")

	print "start: ", start_date
	print "end  : ", end_date
	if request.GET['group'] == "comment": 
		l = LectureComment.objects.filter(time__range=(start_date, end_date)).order_by('-time')
	elif request.GET['group'] == "gossip": 
		l = Gossip.objects.filter(time__range=(start_date, end_date)).order_by('-time')
	else: pass


	template = loader.get_template("cadmin/content.html")
	context = RequestContext(request, {
		"user_number": User.objects.all().count(),
		"comment_number": LectureComment.objects.all().count(),
		"gossip_number": Gossip.objects.all().count(),
		'contents': l,
		'title': request.GET['group'],
		})

	return HttpResponse(template.render(context))

@require_http_methods(['POST'])
def deleteRecord(request):
	if not (request.session['user_id'] in ADMINS): raise Http404

	if request.POST['type'] == "comment":
		deleteComment(int(request.POST['id']))
	elif request.POST['type'] == 'gossip':
		deleteGossip(int(request.POST['id']))

	return HttpResponse(request.POST['id'])

def deleteComment(id):
	c = get_object_or_404(LectureComment, id=id)
	updateUserInfluence(c.user, LectureCommentSuperRecord.objects.filter(lecture_comment=c).count()*COMMENT_SUPER_VALUE_INFLUENCE*(-1))
	# delete super record
	LectureCommentSuperRecord.objects.filter(lecture_comment=c).delete()
	# delete message
	MessageOfCommentSuper.objects.filter(lecture_comment=c).delete()
	updateUserInfluence(c.user, COMMENT_VALUE_INFLUENCE*(-1))
	c.delete()
	return

def deleteGossip(id):
	g = get_object_or_404(Gossip, id=id)
	updateUserInfluence(g.user, GOSSIP_SUPER_VALUE_INFLUENCE*(-1)*GossipSuperRecord.objects.filter(gossip=g).count())
	GossipSuperRecord.objects.filter(gossip=g).delete()
	g.delete()
	return 