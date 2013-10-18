# Create your views here.
import random
import os
import smtplib

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
# from django.core.urlresolvers import reverse
from django.db.models import Q

from login.models import User, RegisteringUser

def login(request):
	print request.method, type(request.method)
	# return HttpResponse("Hi!")
	if request.method == "GET":
		# print "from hello"
		# return HttpResponse("Hello Moto! lala")
		template = loader.get_template("login/login.html")      # zzq: html
		context = RequestContext(request, {
			'u': '123'
		})
		return HttpResponse(template.render(context))
	elif request.method == "POST":
		print "login_POST"
		try:
			username = request.POST['username']
			user = User.objects.get((Q(account=username) | Q(name=username)) & (Q(formal=True)))
			if user.password != request.POST['password']:
				return HttpResponse("password")
			template = loader.get_template("lecture/index.html")      # zzq: html
			return HttpResponse(template.render(RequestContext(request, {})))
		except User.DoesNotExist:
			return HttpResponse("username")
	else :
		raise Http404

def register(request):
	if request.method == "GET":
		template = loader.get_template("login/register.html")      #zzq: html
		return HttpResponse(template.render(RequestContext(request, {})))
	elif request.method == "POST":
		print "there is /register POST"
		registering_user = User.objects.create(account=request.POST['account'],
										name = request.POST['name'],
										password = request.POST['password'])
		sendCheckToUser(registering_user, 'register/checkuser/')
		return HttpResponse()
	else:
		raise Http404


def regCheckUser(request, user_id, check_code):
	if request.method != 'GET':
		raise Http404

	user = User.objects.get(id = user_id)
	check_code = long(check_code)
	print "user.check_code", type(user.check_code), "check_code", type(check_code)
	if user.check_code != check_code :
		return HttpResponse("check code is wrong!")

	user.check_status = False
	user.formal = True
	user.save()
	template = loader.get_template("login/register_success.html")      #zzq: html
	context = RequestContext(request, {
		'u': user
		})
	return HttpResponse(template.render(context))

def sendCheckToUser(user, resurl):
	#check user
	check_code = random.getrandbits(60)	
	print "check_code is " + str(check_code)
	user_account = user.account
	user.check_code = check_code
	user.check_status = True
	user.save()

	check_URL = 'http://sjtucourse.duapp.com/'+ resurl + str(user.id) + '/' + str(check_code)
	if 'SERVER_SOFTWARE' in os.environ:
		from bae.core import const
		from bae.api.bcms import BaeBcms	
		bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
		ret = bcms.createQueue("emailQ")
		real_qname = str(ret['response_params']['queue_name'])
		ret = bcms.mail(real_qname, check_URL, [user_account], "support@baidu.com", "Check Your")
		ret = bcms.dropQueue(real_qname)
		return True
	else:
		try:
			send_mail('Check You', check_URL, 'gowithqi@gmail.com', [user_account], fail_silently=True)
		except smtplib.SMTPException:
			return False
		return True

def checkAccountName(request, key, content):
	if request.method != 'GET':
		raise Http404

	try:
		if key == "account":
			user = User.objects.get(Q(account=content))
		else :
			user = User.objects.get(Q(name=content))
	except User.DoesNotExist:
		return HttpResponse("yes")
	return HttpResponse("no")

def setPassword(request):
	if request.method == "GET":
		template = loader.get_template("login/setpassword.html")     # zzq: html
		return HttpResponse(template)
	elif (request.method == "POST"):
		account = request.POST['account']
		name = request.POST['name']
		if (account == '') and (name == ''): raise Http404
		try:
			if (account == ''): user = User.objects.get(name = name)
			else: user = User.objects.get(account = account)
			sendCheckToUser(user, 'setpassword/chechuser/')
			return HttpResponse("yes")
		except User.DoesNotExist:
			return HttpResponse("no")
	else: raise Http404

def setPwdCheckUser(request, user_id, check_code):
	if request.method != 'GET':
		raise Http404

	user = User.objects.get(id = user_id)
	if user.check_code != check_code :
		return HttpResponse("check code is wrong!")

	user.check_status = False
	user.save()
	template = loader.get_template("login/setnewpassword.html")      #zzq: html
	context = RequestContext(requset, {
		'u': user
		})
	return HttpResponse(template.render(context))

def setNewPassword(request):
	if request.method != 'POST':
		raise Http404

	user = User.objects.get(id = request.POST['user_id'])
	user.password = request.POST['password']

	return HttpResponse("yes")

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
	if 'SERVER_SOFTWARE' in os.environ:
		from bae.core import const
		from bae.api.bcms import BaeBcms	
		bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
		ret = bcms.createQueue("emailQ")
		real_qname = str(ret['response_params']['queue_name'])
		ret = bcms.mail(real_qname, "lalala", ['gowithqi@126.com'], "sjtucourse@duapp.com", "Check You")
		ret = bcms.dropQueue(real_qname)
		return HttpResponse('success in BAE')
	else :
		try:
			send_mail('Check You', "lalal", 'gowithqi@gmail.com', ['gowithqi@126.com'], fail_silently=True)
		except smtplib.SMTPSenderRefused:
			return HttpResponse('there is a exception')
		return HttpResponse('success')

def changepassword(request):
	if request.method != 'POST':
		raise Http404

	try: 
		user = User.objects.get(name = request.POST['username'])
		# something
	except User.DoesNotExist:
		# pass
		return 




	