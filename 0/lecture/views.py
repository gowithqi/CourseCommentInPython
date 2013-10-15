# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg

from lecture.models import *

def lecture(request):
	print "from hello"
	return HttpResponse("Hello! this is lecture")


