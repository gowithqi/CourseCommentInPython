# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg
from django import db
from django.views.decorators.http import require_http_methods

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord, LectureStudentScoreRecord, UserLectureCollection
from gossip.models import Gossip, GossipSuperRecord
from login.models import User
from login.views import checkUserLogin
from comment.views import increaseSysAchievement, _commentLecture

import os
import json

def getLecture(request, lecture_id):
	if request.method != 'GET': raise Http404
	user_id = checkUserLogin(request)				
	print lecture_id, type(lecture_id)
	lecture_id = int(lecture_id)
	user =  get_object_or_404(User, id=user_id)

	try:
		lecture = Lecture.objects.get(id=lecture_id)
	except Lecture.DoesNotExist:
		raise Http500

	lecture_collection = [r.lecture.id for r in user.userlecturecollection_set.all()]
	print "after lecture collection"
	course = lecture.course
	course.view_time = course.view_time + 1
	print "course view time", course.view_time
	course.save()
	print "course"
	lectures = lecture.course.lecture_set.all().order_by("-level")

	print "lectures"
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

def updateAverange(average, total_count, new, new_count = 1):
	average = float(average*total_count + new) / (total_count+new_count)
	print "average", average
	return average, total_count+new_count

def recordStudentScore(request, lecture_id):
	if request.method != "POST": raise Http404
	print "record student score"
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)

	lecture = _recordStudentScore(request, lecture, user)
	print "lecture student_score", lecture.professor.name, lecture.student_score
	lecture.save()
	print "lecture student_score", lecture.professor.name, lecture.student_score
	return HttpResponse("yes")

def _recordStudentScore(request, lecture, user):
	if request.POST['score'] == "" :return lecture
	average = lecture.student_score
	total_count = lecture.student_score_number
	new = float(request.POST['score'])
	if not (40 < new <= 101) : return lecture
	new_count = 1
	try:
		record = LectureStudentScoreRecord.objects.get(lecture=lecture, user=user)
		new, record.score = (new-record.score), new
		new_count = 0
		record.save()
		flag = False
	except LectureStudentScoreRecord.DoesNotExist: flag = True

	lecture.student_score, lecture.student_score_number = updateAverange(average, total_count, new, new_count)

	if flag: LectureStudentScoreRecord.objects.create(lecture=lecture, user=user, score=float(request.POST['score']))

	return lecture

def updateLevel(lecture, level, delta):
	if level == 1: lecture.level_1_number = lecture.level_1_number + delta
	elif level == 2: lecture.level_2_number = lecture.level_2_number + delta
	elif level == 3: lecture.level_3_number = lecture.level_3_number + delta
	elif level == 4: lecture.level_4_number = lecture.level_4_number + delta
	elif level == 5: lecture.level_5_number = lecture.level_5_number + delta
	else: pass

	return lecture

def recordLevel(request, lecture_id):
	if request.method != "POST": raise Http404
	print "record level"
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)

	lecture = _recordLevel(request, lecture, user)
	lecture.save()
	print "record level done", lecture.level
	return HttpResponse("yes")	

def _recordLevel(request, lecture, user):
	if request.POST['level'] == "" :return lecture
	average = lecture.level
	total_count = lecture.level_number
	origin = new = int(request.POST['level'])
	if not (1 <= new <= 5):  return lecture
	new_count = 1
	try:
		record = LectureLevelRecord.objects.get(lecture=lecture, user=user)
		lecture = updateLevel(lecture, record.level, -1)
		new, record.level = (new-record.level), new
		new_count = 0
		record.save()
		flag = False
	except LectureLevelRecord.DoesNotExist: flag = True

	lecture.level, lecture.level_number = updateAverange(average, total_count, new, new_count)
	lecture = updateLevel(lecture, origin, 1)

	if flag: LectureLevelRecord.objects.create(lecture=lecture, user=user, level=int(request.POST['level']))

	return lecture

@require_http_methods(['POST'])
def recordAll(request, lecture_id):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	lecture = get_object_or_404(Lecture, id=int(lecture_id))
	
	lecture = _recordLevel(request, lecture, user)
	lecture = _recordStudentScore(request, lecture, user)
	lecture.save()

	if _commentLecture(request, lecture, user):
		pass
	else:
		return HttpResponse("no")

	return HttpResponse("yes")

@require_http_methods(['GET'])
def courselist(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	template = loader.get_template('lecture/courselist.html')
	school_list = [c['school'] for c in Course.objects.values('school').distinct()]
	print school_list
	context = RequestContext(request, {
		'u': user,
		'school_list': school_list
		})
	return HttpResponse(template.render(context))

@require_http_methods(['POST'])
def getCourses(request, start, end):
	user_id = checkUserLogin(request)
	start = int(start)
	end   = int(end)

	school = request.POST['school']
	if end != 0:
		courses = Course.objects.filter(school=school).order_by("-view_time")[start-1: end]
	else:
		courses = Course.objects.filter(school=school).order_by("-view_time")[start:]
	courses = getCourseDict(courses)

	return HttpResponse(json.dumps(courses, ensure_ascii=False, indent=4))

def getCourseDict(courses):
	ret = []
	for c in courses:
		tmp = {}
		tmp['id'] = c.id
		tmp['name'] = c.name
		tmp['number'] = c.number
		tmp['credit'] = "%.1f" % c.credit
		tmp['school'] = c.school
		tmp['view_time'] = c.view_time
		ret.append(tmp)

	return ret

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
