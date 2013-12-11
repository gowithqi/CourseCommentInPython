# -*- coding: utf-8 -*-
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
from lecture.models import Lecture, LectureCommentSuperRecord
from comment.influence import updateUserInfluence, getSysAchievement

if 'SERVER_SOFTWARE' in os.environ:
	from bae.api import logging
else: 
	import logging

LEASTCOMMITNUMBER = 3
RANKSIZE = 10
TOP_USER_NUMBER = 10

CHECK_EMAIL_CONTENT = """您好，这里SJTU Course，我们在通过交大邮箱验证您的身份信息，请您访问以下链接来确认信息。
		%s
SJTU Course感谢您一如既往的支持，谢谢您的使用！"""
CHECK_EMAIL_SUBJECT = "SJTU Course身份验证"

def login(request):
	print request.method, type(request.method)
	# logging.debug("123")
	# return HttpResponse("Hi!")
	if request.method == "GET":
		if not ('user_id' in request.session): 
			template = loader.get_template("login/login.html")      # zzq: html
			sys_achievement = getSysAchievement()
			return HttpResponse(template.render(RequestContext(request, {'sys_achievement': sys_achievement})))
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
	if 'user_id' in request.session: return request.session['user_id']
	raise Http404

def register(request):
	if request.method == "GET":
		template = loader.get_template("login/register.html")      #zzq: html
		return HttpResponse(template.render(RequestContext(request, {})))
	elif request.method == "POST":
		if not ('have_register' in request.session):									
			request.session['have_register'] = True
			print "there is /register POST"
			try:
				user = User.objects.get(Q(account=request.POST['account']) | Q(name = request.POST['name']))
				if user.formal: raise Http404
				user.delete()
			except User.DoesNotExist:
				pass
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
	updateUserInfluence(user, 0)
	template = loader.get_template("login/register_success.html")      #zzq: html
	context = RequestContext(request, {
		'u': user
		})
	request.session['user_id'] = user.id
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
		logging.debug("send mail")
		check_URL = 'http://sjtucourse.duapp.com/' + check_URL
		content = CHECK_EMAIL_CONTENT % check_URL
		from bae.core import const
		from bae.api.bcms import BaeBcms	
		bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
		logging.debug("init object")
		logging.debug("create Queue")
		real_qname = "4665ae9f84f7c7700dfbc46dc9e73d61"
		ret = bcms.mail(real_qname, content, [user_account], "support@baidu.com", CHECK_EMAIL_SUBJECT)
		logging.debug("have send mail")
		return True
	else:
		check_URL = '127.0.0.1:8000/' +  check_URL
		content = CHECK_EMAIL_CONTENT % check_URL
		try:
			send_mail(CHECK_EMAIL_SUBJECT, content, 'gowithqi@gmail.com', [user_account], fail_silently=True)
		except smtplib.SMTPException:
			return False
		return True

def checkAccountName(request, key, content):
	if request.method != 'GET':
		raise Http404

	if ('have_register' in request.session): del request.session['have_register']
	if key == "account":
		tmp = False
		for user in User.objects.filter(Q(account=content)):
			tmp = tmp or user.formal
			if not user.formal: user.delete()
		if tmp:	return HttpResponse("no")
		else: return HttpResponse("yes")
	else :
		if User.objects.filter(Q(name=content)).count() > 0: return HttpResponse("no")
		else: return HttpResponse("yes")

def setPassword(request):
	if request.method == "GET":
		template = loader.get_template("login/setpassword.html")     # zzq: html
		return HttpResponse(template.render(RequestContext(request, {})))
	elif (request.method == "POST"):
		try:
			account = request.POST['account']
			user = User.objects.get(account = account)
		except User.DoesNotExist:
			return HttpResponse("no")

		if request.POST['again'] == "False":
			if user.check_status == True: return HttpResponse("havePOST")

		sendCheckToUser(user, 'setpassword/checkuser/')
		return HttpResponse("yes")
	else: raise Http404

def setPwdCheckUser(request, user_id, check_code):
	if request.method != 'GET':
		raise Http404

	check_code = long(check_code)
	print check_code, type(check_code)
	user = User.objects.get(id = user_id)
	print user.check_code, type(user.check_code)
	if (user.check_code != check_code) or (not user.check_status):
		return HttpResponse("check code is wrong or not in a right check_status!")
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
	user.check_status = False
	user.password = request.POST['password']
	user.save()

	if 'user_id' in request.session: del request.session['user_id']

	return HttpResponse("yes")

@require_http_methods(['GET'])
def userpage(request, user_id):
	if not ('user_id' in request.session): return HttpResponseRedirect(reverse('login'))

	user = get_object_or_404(User, id=user_id)
	# lecture_rank_level = Lecture.objects.filter(level_number__gte=LEASTCOMMITNUMBER).order_by("-level")[:RANKSIZE]
	# lecture_rank_student_score = Lecture.objects.filter(student_score_number__gte=LEASTCOMMITNUMBER).order_by("-student_score")[:RANKSIZE]
	(user_influence_factor, user_rank) = getUserInfluenceInfo(user)
	sys_achievement = getSysAchievement()
	lectures = Lecture.objects.order_by('?')[:3]

	if int(request.session['user_id']) == int(user_id):
		top_users = User.objects.order_by("-influence_factor")[:TOP_USER_NUMBER]
		me = user
		comment_super_records = []
		template = loader.get_template("userpage/userpage.html")
	else:
		top_users = ""
		me = get_object_or_404(User, id = int(request.session['user_id']))
		comment_super_records = [ t.lecture_comment.id for t in me.lecturecommentsuperrecord_set.all()]
		template = loader.get_template("userpage/hisuserpage.html")

	context = RequestContext(request, {
		'comment_super_records': comment_super_records,
		'me': me,
		'top_users': top_users,
		'u': user,
		# 'llevel': lecture_rank_level,
		# 'lstudentscore': lecture_rank_student_score,
		'user_influence_factor': user_influence_factor,
		'user_rank': user_rank,
		'sys_achievement': sys_achievement,
		'lectures': lectures,
		})
	return HttpResponse(template.render(context))

def getUserInfluenceInfo(user):
	res = (10, 1)
	if 'SERVER_SOFTWARE' in os.environ:
		# from bae.api.rank import BaeRank
		# from bae.api import logging
		# r = BaeRank("UserInfluence")
		# keyword = str(user.id)
		# info = r.get(keyword)
		# tmp =  float(User.objects.all().count() - info['response_params']['rank'] - 1) / User.objects.all().count()
		# res = (info['response_params']['value'], int(tmp*100))
		tmp =  float(User.objects.filter(influence_factor__lt=user.influence_factor).count()) / User.objects.all().count()
		res = (user.influence_factor, int(tmp*100))
	else:
		tmp =  float(User.objects.filter(influence_factor__lt=user.influence_factor).count()) / User.objects.all().count()
		res = (user.influence_factor, int(tmp*100))
	return res

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

def test(request):
	if not ('user_id' in request.session): raise Http404

	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)
	(user_influence_factor, user_rank) = getUserInfluenceInfo(user)
	sys_achievement = getSysAchievement()
	lectures = Lecture.objects.order_by('?')[:3]

	template = loader.get_template("lecture/test.html")
	context = RequestContext(request, {
		'u': user,
		'user_influence_factor': user_influence_factor,
		'user_rank': user_rank,
		'sys_achievement': sys_achievement,
		'lectures': lectures,
		})
	return HttpResponse(template.render(context))
	# if 'SERVER_SOFTWARE' in os.environ:
	# 	from bae.api.rank import BaeRank
	# 	from bae.api import logging
	# 	r = BaeRank("UserInfluence")
	# 	logging.debug(str(r.get("14")))

	# 	rlist = r.getList()
	# 	res = []
	# 	for u in rlist:
	# 		user = get_object_or_404(User, id=long(u[0]))
	# 		tmp = (user.name, u[1])
	# 		res.append(tmp)
	# 	template = loader.get_template("lecture/test.html")
	# 	context = RequestContext(request, {
	# 		'res': res,
	# 		})
	# 	return HttpResponse(template.render(context))

	# return HttpResponse("")

	
