# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg
from django import db
from django.views.decorators.http import require_http_methods

from lecture.models import Professor, Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord, LectureStudentScoreRecord, UserLectureCollection
from gossip.models import Gossip, GossipSuperRecord
from login.models import User
from login.views import checkUserLogin
from comment.views import increaseSysAchievement, _commentLecture
from manageDB.xpinyin import Pinyin
from search.views import changeString

import os
import json

if 'SERVER_SOFTWARE' in os.environ:
	from bae.api import logging
else: 
	import logging

@require_http_methods(["GET"])
def updateLecture(request):
	user_id = checkUserLogin(request)
	if user_id != 14: return Http404

	ret = ""
	ret += _updateLecture("1.xml")
	ret += _updateLecture("2.xml")

	return HttpResponse(ret)

def _updateLecture(file_name):
	from BeautifulSoup import BeautifulStoneSoup
	f = open(os.path.join(os.path.dirname(__file__), "../tongshike/"+file_name), "r")
	file_content = f.read()
	soup = BeautifulStoneSoup(file_content)

	p = Pinyin()
	flag = True
	ret = ""
	for l in soup.findAll("detail"):
		course_school = l.get("yxmc").strip()
		course_number = l.get("kcbm")[17:22]
		professor_name = l.get("xm").strip()
		professor_title = l.get("zcmc")
		if type(professor_title) == type(None): continue
		course_name = l.get("kcmc").strip()
		course_credit = float(l.get("xqxf").strip())

		logging.debug("after get info")
		c_flag = True
		p_flag = True
		try:
			c = Course.objects.get(school=course_school, number=course_number)
		except Course.DoesNotExist:
			c_flag = False
			name_pinyin = changeString(course_name)
			c = Course.objects.create(name=course_name, 
				number=course_number, 
				credit=course_credit, 
				school=course_school, 
				name_pinyin=p.get_pinyin((name_pinyin), '')[:50],
				name_forsearch=name_pinyin)
		logging.debug("after course")
		try:
			pro = Professor.objects.get(name=professor_name)
		except Professor.DoesNotExist:
			p_flag = False
			pro = Professor.objects.create(name=professor_name, title=professor_title)
		logging.debug("after pro")
		try:
			lecture = Lecture.objects.get(course=c, professor=pro)
		except Lecture.DoesNotExist:
			lecture = Lecture.objects.create(course=c, professor=pro)
			if not c_flag and p_flag: 
				ret += "course__"
			elif c_flag and not p_flag:
				ret += "profes__"
			else:
				ret += "lectur__"

			ret += "lecture_id:%ld__course_id:%ld__%s__%s </br>" % (lecture.id, c.id, c.name, pro.name)
			logging.debug("lecture_id:%ld__course_id:%ld__%s__%s </br>" % (lecture.id, c.id, c.name, pro.name))

	return ret

def parse(c):
	d = {"renwen": u"人文学科",
		 "sheke":  u"社会科学",
		 "shuxue": u"数学或逻辑学",
		 "ziran":  u"自然科学与工程技术"}
	from BeautifulSoup import BeautifulSoup
	f = open(os.path.join(os.path.dirname(__file__), "../tongshike/"+c+"/newsinside.html"), "r")
	file_content = f.read()
	soup = BeautifulSoup(file_content)

	i = 0
	ret = ""
	courses_html = soup.findAll("tr", {"class": ["tdcolour1", "tdcolour2"]})
	for c_html in courses_html[4:]:
		cc = c_html.findChildren("td")
		i += 1
		course_number = cc[2].string.strip()
		n = Course.objects.filter(number=course_number).count()
		if	n > 1:
			ret += "more than 1: "
			print "more than 1: ", cc[2].string, cc[1].string
		elif n == 0:
			print "does exist : ", cc[2].string, cc[1].string
		else:
			cour = Course.objects.get(number=course_number)
			cour.category = d[c]
			cour.save()
			ret += cc[2].string + "_________" + cc[1].string + "</br>"
	ret += str(i) + "</br>"
	return ret

@require_http_methods(["GET"])
def addTongShiKe(request):
	user_id = checkUserLogin(request)
	if user_id != 14: return Http404
	
	return HttpResponse(parse("renwen")+parse("sheke")+parse("ziran")+parse("shuxue"))