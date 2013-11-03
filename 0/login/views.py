# Create your views here.
import random
import os
import smtplib

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.db.models import Q

from login.models import User, RegisteringUser

def login(request):
	print request.method, type(request.method)
	# return HttpResponse("Hi!")
	if request.method == "GET":
		if not ('user_id' in request.session): 
			template = loader.get_template("login/login.html")      # zzq: html
			return HttpResponse(template.render(RequestContext(request, {})))
		else: return HttpResponseRedirect(reverse('userpage', args=(request.session['user_id'], )))
	elif request.method == "POST":
		print "login_POST"
		try:
			username = request.POST['username']
			user = User.objects.get((Q(account=username) | Q(name=username)) & (Q(formal=True)))
			if user.password != request.POST['password']:
				return HttpResponse("password")
			request.session['user_id'] = user.id
			return HttpResponse(user.id)
		except User.DoesNotExist:
			return HttpResponse("username")
	else :
		raise Http404

	# template = loader.get_template("userpage/userpage.html")      # zzq: html
	# return HttpResponse(template.render(RequestContext(request, {})))

def logout(request):
	if request.method != 'GET': raise Http404
	try:
		del request.session['user_id']
	except KeyError:
		pass

	return HttpResponseRedirect(reverse('login'))

def checkUserLogin(request):
	if 'user_id' in request.session: return True
	raise Http404

def register(request):
	if request.method == "GET":
		template = loader.get_template("login/register.html")      #zzq: html
		return HttpResponse(template.render(RequestContext(request, {})))
	elif request.method == "POST":
		if not ('have_register' in request.session):									
			request.session['have_register'] = True
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

	check_URL = resurl + str(user.id) + '/' + str(check_code)
	if 'SERVER_SOFTWARE' in os.environ:
		check_URL = 'http://sjtucourse.duapp.com/' + check_URL
		from bae.core import const
		from bae.api.bcms import BaeBcms	
		bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
		ret = bcms.createQueue("emailQ")
		real_qname = str(ret['response_params']['queue_name'])
		ret = bcms.mail(real_qname, check_URL, [user_account], "support@baidu.com", "Check Your")
		ret = bcms.dropQueue(real_qname)
		return True
	else:
		check_URL = '127.0.0.1:8000/' +  check_URL
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
		return HttpResponse(template.render(RequestContext(request, {})))
	elif (request.method == "POST"):
		account = request.POST['account']
		name = request.POST['name']
		if (account == '') and (name == ''): raise Http404
		try:
			if (account == ''): user = User.objects.get(name = name)
			else: user = User.objects.get(account = account)
			sendCheckToUser(user, 'setpassword/checkuser/')
			return HttpResponse("yes")
		except User.DoesNotExist:
			return HttpResponse("no")
	else: raise Http404

def setPwdCheckUser(request, user_id, check_code):
	if request.method != 'GET':
		raise Http404

	check_code = long(check_code)
	print check_code, type(check_code)
	user = User.objects.get(id = user_id)
	print user.check_code, type(user.check_code)
	if user.check_code != check_code :
		return HttpResponse("check code is wrong!")

	user.check_status = False
	user.save()
	template = loader.get_template("login/newpassword.html")      #zzq: html
	context = RequestContext(request, {
		'u': user
		})
	return HttpResponse(template.render(context))

def setNewPassword(request):
	if request.method != 'POST':
		raise Http404

	user = User.objects.get(id = request.POST['user_id'])
	user.password = request.POST['password']

	return HttpResponse("yes")

@require_http_methods(['GET'])
def userpage(request, user_id):
	if not ('user_id' in request.session): raise Http404
	user = get_object_or_404(User, id=user_id)
	template = loader.get_template("userpage/userpage.html")
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




	
