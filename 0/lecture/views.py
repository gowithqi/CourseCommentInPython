# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from django.db.models import Avg

from lecture.models import Course, Lecture, LectureComment, LectureCommentSuperRecord, LectureLevelRecord, LectureStudentScoreRecord
from login.models import User
from login.views import checkUserLogin

def getLecture(request, lecture_id):
	if request.method != 'GET': raise Http404
	print "123"
	checkUserLogin(request)
	print lecture_id, type(lecture_id)
	lecture_id = int(lecture_id)

	try:
		lecture = Lecture.objects.get(id=lecture_id)
	except Lecture.DoesNotExist:
		raise Http500

	lectures = lecture.course.lecture_set.all()

	template = loader.get_template('lecture/lecture.html')
	context = RequestContext(request, {
		'l' : lectures,
		})
	return HttpResponse(template.render(context))

def recordStudentScore(request, lecture_id):
	if request.method != "POST": raise Http404

	checkUserLogin(request)
	user = get_object_or_404(User, id=request.session['user_id'])
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
	lss = lecture.student_score         
	lssn = lecture.student_score_number
	newscore = float(lss*lssn + float(request.POST['score'])) / (lssn+1)
	lecture.student_score_number = lssn+1
	lecture.student_score = newscore
	lecture.save()

	LectureStudentScoreRecord.objects.create(lecture=lecture, user=user, score=float(request.POST['score']))

	return HttpResponse("yes")

def recordLevel(request, lecture_id):
	if request.method != "POST": raise Http404

	checkUserLogin(request)
	user = get_object_or_404(User, id=request.session['user_id'])
	lecture_id = int(lecture_id)
	lecture = get_object_or_404(Lecture, id=lecture_id)
	ll = lecture.level         
	lln = lecture.level_number
	newlevel = float(ll*lln + float(request.POST['level'])) / (lln+1)
	lecture.level_number = lln+1
	lecture.level = newlevel
	lecture.save()

	LectureLevelRecord.objects.create(lecture=lecture, user=user, level=int(request.POST['level']))

	return HttpResponse("yes")	

def commentLecture(request):
	# get a user
	# get a lecture
	# get a comment
	lecture_comment = LectureComment.objects.create()

def test(request, lecture_id):
	lecture = get_object_or_404(Lecture, id=lecture_id)

	lectures = lecture.course.lecture_set.all()
	for lecture in lectures:
		print lecture.course.name, lecture.professor.name

	return HttpResponse()