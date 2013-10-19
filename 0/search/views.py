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
	courseList = Course.objects.filter(name__startswith=content)[:5]
	res = ''
	for c in courseList: res = c.name + '\n'
	res = res[:-1]

	return HttpResponse(res)

def searchLecture(request):
	if request.method != 'POST': raise Http404

	checkUserLogin(request)
	course = Course.objects.filter(name=request.POST['content'])[0]
	lectures = course.lecture_set.all()

	template = loader.get_template("lecture/lecture.html")
	context = RequestContext(request, {
		'l': lectures,
		})
	return HttpResponse(template.render(context))
