# Create your views here.
import os

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from lecture.models import Lecture, Course
from login.views import checkUserLogin

AUTO_COMPLETE_LIST_LENGTH = 5

def autoComplete(request):
	if request.method != "POST": raise Http404

	content = request.POST['content']
	if isPinyin(content): courseList = Course.objects.filter(name_pinyin__startswith=content).order_by("-view_time", "name")
	else: 				  courseList = Course.objects.filter(name__startswith=content).order_by("-view_time", "name")

	res = ''
	i = 1
	print "len: ", len(courseList)
	if len(courseList) > 0:
		tmpc = courseList[0]
		res = res + tmpc.name + '\n'
		for c in courseList[1:]: 
			if c.name != tmpc.name:	
				res = res + c.name + '\n'
				i = i + 1
			tmpc = c
			if i == AUTO_COMPLETE_LIST_LENGTH: break
		res = res[:-1]

	return HttpResponse(res)

def searchLecture(request):
	if request.method != 'POST': raise Http404

	checkUserLogin(request)
	lecture_id = 0
	keyword = request.POST['content']

	courses = Course.objects.filter(name = keyword)
	if len(courses) == 1: 
		course = courses[0]
		lectures = course.lecture_set.all()
		if len(lectures) > 0: lecture_id = lectures[0].id
		else: lecture_id = -1
	elif len(courses) > 1: 
		res = ""
		for c in courses:
			res = res + str(c.id) + ':' + c.name + ':' + c.number + ':' + str(c.credit) + ':' + c.school + '\n'
		print res
		return HttpResponse(res)
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

def isPinyin(keyword):
	res = True
	for k in keyword:
		res = res and (k.isdigit() or isLetter(k))
	return res

def isCourseNumber(keyword):
	res = True
	for k in keyword[:5]: res = res and (k.isdigit() or isLetter(k))
	return res

def isLetter(k):
	return ((k >= u'\u0041' and k<=u'\u005a') or (k >= u'\u0061' and k<=u'\u007a'))