# Create your views here.
import os

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
from django.db.models import Q

from lecture.models import Lecture, Course
from login.views import checkUserLogin

def autoComplete(request):
	if request.method != "POST": raise Http404

	content = request.POST['content']
	courseList = Course.objects.filter(name__startswith=content).order_by("name").distinct("name")[:5]
	res = ''
	for c in courseList: 
		res = res + c.name + '\n'
	res = res[:-1]

	return HttpResponse(res)

def searchLecture(request):
	if request.method != 'POST': raise Http404

	checkUserLogin(request)
	lecture_id = 0
	try:
		course = Course.objects.get(name=request.POST['content'])
		lectures = course.lecture_set.all()
		if len(lectures) > 0: lecture_id = lectures[0].id
		else : lecture_id = -1
	except Course.DoesNotExist:
		lecture_id = -1
	
	return HttpResponse("/lecture/" + str(lecture_id) + "/")
