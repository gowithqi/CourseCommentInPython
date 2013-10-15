# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg

from login.models import User, RegisteringUser

def gossip(request):
	if request.method != "GET":
		raise Http404

	print "from hello"
	return HttpResponse("Here is gossip")

def recordgossip(request): 
	# pass
	return 