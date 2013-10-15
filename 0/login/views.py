# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg

from login.models import User, RegisteringUser

def hello(request):
	print "from hello"
	return HttpResponse("Hello Moto! lala")

def userpage(request, username):
	password = request.POST['password']
	try:
		user = User.objects.get(name=username)
	except User.DoesNotExist:
		raise Http404

	template = loader.get_template("*.html")
	context = RequestContext(request, {
		'u': user,
		})
	return HttpResponse(template.render(context))

def sign(request):
	if request.method == 'GET':
		#there is something
		pass
	elif request.method == 'POST':
		pass
	else:
		# return 404
		raise Http404

def changepassword(request):
	if request.method != 'POST':
		raise Http404

	try: 
		user = User.objects.get(name = request.POST['username'])
		# something
	except User.DoesNotExist:
		pass





	