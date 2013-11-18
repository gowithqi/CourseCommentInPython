from django.http import HttpResponse, Http404, HttpResponseRedirect

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord
from login.models import User
from comment.models import MessageOfCommentSuper
from login.views import checkUserLogin
from comment.influence import increaseSysAchievement, updateUserInfluence
from comment.views import START_TIME, SUPER_VALUE

import jieba

def updateCommentData(request):
	user_id = checkUserLogin(request)
	if user_id != 14: return Http404

	ret = ""
	for comment in LectureComment.objects.all():
		print comment.lecture.course.name, comment.content
		# get content word list
		word_list = jieba.cut(comment.content, cut_all=False)
		word_list = [w for w in word_list]
		
		# get lecture infomation
		lecture_info = getLectureInfo(comment.lecture)
		# get garbage infomation
		garbage_info = getGarbageInfo()

		# eliminate the same word
		word_list = eliminateSameWord(word_list)

		# eliminate known infomation
		res = []
		for w in word_list:
			if not(w in lecture_info or w in garbage_info) : res.append(w)

		ret = ret + "len: " + str(len(res)) + "_"
		for r in res: ret = ret + r + "_"
		ret = ret + "<br/>"

	return HttpResponse(ret)

def getGarbageInfo():
	return []

def eliminateSameWord(word_list):
	word_list.sort()

	tmpw = word_list[0]
	ret = [tmpw]
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