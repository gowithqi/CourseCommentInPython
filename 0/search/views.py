# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from lecture.models import Lecture, Course
from login.views import checkUserLogin

AUTO_COMPLETE_LIST_LENGTH = 15
MAX_ALTERNATE_NUMBER = 12

def autoComplete(request):
	if request.method != "POST": raise Http404

	content = request.POST['content']
	courseList = getStartsWithCourseList(content, AUTO_COMPLETE_LIST_LENGTH+10)
	
	course_name_list = getCourseNameList(courseList)
	return HttpResponse("\n".join(course_name_list))

def getCourseNameList(courseList):
	ret = []
	for c in courseList:
		if c.name in ret: pass
		else: ret.append(c.name)
		if len(ret) == AUTO_COMPLETE_LIST_LENGTH: break
	return ret

def searchLecture(request):
	if request.method != 'POST': raise Http404

	checkUserLogin(request)
	lecture_id = 0
	keyword = request.POST['content']

	courses = Course.objects.filter(name=keyword)
	print len(courses)
	if len(courses) == 1: 
		course = courses[0]
		lectures = course.lecture_set.all()
		if len(lectures) > 0: lecture_id = lectures[0].id
		else: lecture_id = -1
	elif len(courses) == 0:
		courseList = getStartsWithCourseList(keyword, MAX_ALTERNATE_NUMBER)
		return HttpResponse(getCourseListInfo(courseList))
	elif (len(courses) > 1): 
		return HttpResponse(getCourseListInfo(courses))
	else: lecture_id = -1

	return HttpResponse("/lecture/" + str(lecture_id) + "/")

@require_http_methods(['GET'])
def searchLectureUsingCourseID(request, course_id):
	checkUserLogin(request)
	course_id = int(course_id)

	lectures = Lecture.objects.filter(course_id = course_id)
	if len(lectures) > 0: lecture_id = lectures[0].id
	else: lecture_id = -1

	return HttpResponse("/lecture/" + str(lecture_id) + "/")

def getStartsWithCourseList(keyword, length):
	content = changeString(keyword)
	if isPinyin(content): courseList = Course.objects.filter(name_pinyin__startswith=content).order_by("-view_time")[:length]
	else: 				  courseList = Course.objects.filter(name_forsearch__startswith=content).order_by("-view_time")[:length]
	return courseList

def getCourseListInfo(courses):
	res = ""
	for c in courses:
		res = res + str(c.id) + ':' + c.name + ':' + c.number + ':' + str(c.credit) + ':' + c.school + '\n'
	return res

def isPinyin(keyword):
	res = True
	for k in keyword:
		res = res and (not is_chinese(k))
	return res
		
def is_alphabet(uchar):
	return (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a')

def is_chinese(uchar):
	return uchar >= u'\u4e00' and uchar<=u'\u9fa5'

def changeString(ustring):
	return "".join([changeChar(uchar) for uchar in ustring])

def changeChar(uchar):
	BIAODIAN = u"《》“”、\"（）() "
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