import os
from datetime import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from comment.models import MessageOfCommentSuper
from login.views import checkUserLogin
from comment.influence import increaseSysAchievement, updateUserInfluence
from comment.views import START_TIME, SUPER_VALUE

import jieba
NUMBER_OF_WORDS = 40

def updateCommentData(request, mode):
	user_id = checkUserLogin(request)
	if user_id != 14: return Http404
	if str(mode) == "force": force_recompute = True
	elif str(mode) == "unforce": force_recompute = False
	else: raise Http500

	garbage_info = getGarbageInfo()

	ret = ""
	for comment in LectureComment.objects.all():
		if not (comment.need_recompute or force_recompute): continue

		print comment.lecture.course.name, comment.content
		# get content word list
		word_list = jieba.cut(comment.content, cut_all=False)
		word_list = [w for w in word_list]
		
		# get lecture infomation
		lecture_info = getLectureInfo(comment.lecture)

		# eliminate the same word
		word_list = eliminateSameWord(word_list)

		# eliminate known infomation
		res = []
		for w in word_list:
			if not((w in lecture_info) or (w in garbage_info)) : res.append(w)

		super_weight = getSuperWeight(len(res))
		comment_time = comment.time
		delta_t = comment_time - START_TIME
		time_factor = int(delta_t.total_seconds()/86400)

		if force_recompute: comment.super_number = comment.lecturecommentsuperrecord_set.all().count()
		comment.rank_score = time_factor+SUPER_VALUE*super_weight*(comment.super_number+1)
		comment.super_weight = comment.super_weight
		comment.need_recompute = False
		comment.save()
		ret = ret + "len: " + str(len(res)) + "_super weight: " + str(super_weight) + "_"
		for r in res: ret = ret + r + "_"
		ret = ret + "<br/>"

	return HttpResponse(ret)

def getSuperWeight(x):
	import math
	return (0.9/math.pow(NUMBER_OF_WORDS, 1.0/3))*math.pow(x, 1.0/3)

def getGarbageInfo():
	ret = []
	f = open(os.path.join(os.path.dirname(__file__), 'garbagedist.txt'), "rb")
	for line in f.read().rstrip().decode('utf-8').split('\n'):
		if len(line) > 0: ret.append(line)
	return ret

def eliminateSameWord(word_list):
	word_list.sort()

	tmpw = word_list[0]
	if tmpw != " ": ret = [tmpw]
	else: ret = []
	for w in word_list[1:]:
		if w != tmpw:
			ret.append(w)
			tmpw = w
	return ret

def getLectureInfo(lecture):
	ret = []
	# lecture course info
	tmp = jieba.cut(lecture.course.name, cut_all=False)
	tmp = [t for t in tmp]
	ret.extend(tmp)

	# leceture professor info
	tmp = jieba.cut(lecture.professor.name, cut_all=False)
	tmp = [t for t in tmp]
	ret.extend(tmp)

	return ret