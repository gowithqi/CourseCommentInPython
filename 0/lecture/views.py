# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg
from django import db

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord, LectureStudentScoreRecord, UserLectureCollection
from gossip.models import Gossip, GossipSuperRecord
from login.models import User
from login.views import checkUserLogin
from comment.views import increaseSysAchievement

import os

def getLecture(request, lecture_id):
	if request.method != 'GET': raise Http404
	print "123"
	user_id = checkUserLogin(request)				
	print lecture_id, type(lecture_id)
	lecture_id = int(lecture_id)
	user =  get_object_or_404(User, id=user_id)

	try:
		lecture = Lecture.objects.get(id=lecture_id)
	except Lecture.DoesNotExist:
		raise Http500

	lecture_collection = [r.lecture.id for r in user.userlecturecollection_set.all()]
	course = lecture.course
	course.view_time = course.view_time + 1
	course.save()
	lectures = lecture.course.lecture_set.all()

	comment_super_list = getSuperList(lectures, user, "comment")
	gossip_super_list = getSuperList(lectures, user, "gossip")
	print comment_super_list
	print gossip_super_list
	
	template = loader.get_template('lecture/course.html')
	context = RequestContext(request, {
		'course': lecture.course,
		'lectures' : lectures,
		'u': user,
		'focus_lecture_id': lecture_id,
		'comment_super_list': comment_super_list,
		'gossip_super_list': gossip_super_list,
		'lecture_collection': lecture_collection,
		})
	if lecture.lecturecomment_set.all().count() > 0: increaseSysAchievement()
	return HttpResponse(template.render(context))

def getSuperList(lectures, user, table):
	res = []
	if table == "comment": 
		for lecture in lectures:
			comments = LectureComment.objects.filter(lecture=lecture)
			for comment in comments:
				try:
					LectureCommentSuperRecord.objects.get(lecture_comment=comment, user=user)
					res.append(int(comment.id))
				except LectureCommentSuperRecord.DoesNotExist: pass
	elif table == "gossip":
		for lecture in lectures:
			gossips = Gossip.objects.filter(lecture=lecture)
			for gossip in gossips:
				try:
					GossipSuperRecord.objects.get(gossip=gossip, user=user)
					res.append(int(gossip.id))
				except GossipSuperRecord.DoesNotExist: pass

	return res
'''
def getLectureData(request, lecture_id):
	if request.method != 'GET': raise Http404
	print "getLectureData"
	user_id = checkUserLogin(request)				
	lecture_id = int(lecture_id)
	user =  get_object_or_404(User, id=user_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
'''

def recordStudentScore(request, lecture_id):
	if request.method != "POST": raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
	try:
		LectureStudentScoreRecord.objects.get(lecture=lecture, user=user)
		return HttpResponse("have recorded student score")
	except LectureStudentScoreRecord.DoesNotExist: pass
	lss = lecture.student_score         
	lssn = lecture.student_score_number
	newscore = float(lss*lssn + float(request.POST['score'])) / (lssn+1)
	lecture.student_score_number = lssn+1
	lecture.student_score = newscore

	lecture.save()

	LectureStudentScoreRecord.objects.create(lecture=lecture, user=user, score=float(request.POST['score']))

	return HttpResponse("yes")

def recordLevel(request, lecture_id):
	if request.method != "POST": raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
	try:
		LectureLevelRecord.objects.get(lecture=lecture, user=user)
		return HttpResponse("have recorded level")
	except LectureLevelRecord.DoesNotExist: pass

	level = int(request.POST['level'])
	if level == 1: lecture.level_1_number = lecture.level_1_number + 1
	elif level == 2: lecture.level_2_number = lecture.level_2_number + 1
	elif level == 3: lecture.level_3_number = lecture.level_3_number + 1
	elif level == 4: lecture.level_4_number = lecture.level_4_number + 1
	elif level == 5: lecture.level_5_number = lecture.level_5_number + 1
	else: raise Http500

	ll = lecture.level         
	lln = lecture.level_number
	newlevel = float(ll*lln + float(level)) / (lln+1)
	lecture.level_number = lln+1
	lecture.level = newlevel
	lecture.save()

	LectureLevelRecord.objects.create(lecture=lecture, user=user, level=int(request.POST['level']))

	return HttpResponse("yes")	

def test(request, mode):
	user_id = checkUserLogin(request)
	if user_id != 14: return Http404
	
	BIAODIAN = u"《》“”、\"（）()"
	count = 0
	ret = ""
	for course in Course.objects.all():
		if mode == "name": pinyin = course.name
		else: pinyin = course.name_pinyin
		res = changeString(pinyin)    
		if mode == "name": pinyin = course.name_forsearch
		if res != pinyin:
			count = count + 1
			ret += pinyin + '__' + res + '<br/>'
			if mode=="name": course.name_forsearch = res
			else: course.name_pinyin = res
			course.save()
			print res
			print pinyin
			print 		
	print count
	ret += str(count)
	return HttpResponse(ret)

def is_alphabet(uchar):
	if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
		return True
	else:
		return False

def is_chinese(uchar):
	if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
		return True
	else:
		return False

def changeString(ustring):
	return "".join([changeChar(uchar) for uchar in ustring])

def changeChar(uchar):
	BIAODIAN = u"《》“”、\"（）()"
	if uchar in BIAODIAN: return ""
	if is_alphabet(uchar): return uchar.lower()
	return Q2B(uchar)

def Q2B(uchar):
	inside_code = ord(uchar)
	if inside_code == 0x3000:
		inside_code = 0x0020
	else:
		inside_code -= 0xfee0

	if inside_code<0x0020 or inside_code >0x7e:
		return uchar

	return unichr(inside_code)
