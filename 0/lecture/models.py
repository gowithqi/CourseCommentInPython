from django.db import models
from login.models import User
from userpage.formatTime import formatTime

class Course(models.Model):
	class Meta:
		db_table = "course"

	name = models.CharField(max_length = 50, db_column = "name")
	number = models.CharField(max_length = 10, db_column = "number")
	credit = models.FloatField(default = 0, db_column = "credit")
	school = models.CharField(max_length = 50, db_column = "school")
	view_time = models.IntegerField(default = 0, db_column = "view_time")
	name_pinyin = models.CharField(max_length = 50, db_column = "name_pinyin")
	name_forsearch = models.CharField(max_length = 50, db_column = "name_forsearch")
	category = models.CharField(max_length = 50, db_column = "category")

	def getDict(self, id=True, name=True, number=True, credit=True, school=True, category=True):
		ret = {}
		if id: 			ret['id'] = self.id
		if name: 		ret['name'] = self.name
		if number: 		ret['number'] = self.number
		if credit:		ret['credit'] = self.credit
		if school: 		ret['school'] = self.school
		if category: 	ret['category'] = self.category

		return ret

class Professor(models.Model):
	class Meta:
		db_table = "professor"

	name = models.CharField(max_length = 50, db_column = "name")
	number = models.CharField(max_length = 20, db_column = "number")
	title = models.CharField(max_length = 50, db_column = "title")

	def getDict(self, id=True, name=True, number=False, title=False):
		ret = {}
		if id: 			ret['id'] = self.id
		if name: 		ret['name'] = self.name
		if number: 		ret['number'] = self.number
		if title:		ret['title'] = self.title

		return ret

class Lecture(models.Model):
	class Meta:
		db_table = "lecture"

	course = models.ForeignKey(Course, db_column = "course_id")
	professor = models.ForeignKey(Professor, db_column = "professor_id")
	student_score = models.FloatField(default = 0, db_column = "student_score")
	level = models.FloatField(default = 0, db_column = "level")
	student_score_number = models.IntegerField(default = 0, db_column = "student_score_number")
	level_number = models.IntegerField(default = 0, db_column = "level_number")
	level_1_number = models.IntegerField(default = 0, db_column = "level_1_number")
	level_2_number = models.IntegerField(default = 0, db_column = "level_2_number")
	level_3_number = models.IntegerField(default = 0, db_column = "level_3_number")
	level_4_number = models.IntegerField(default = 0, db_column = "level_4_number")
	level_5_number = models.IntegerField(default = 0, db_column = "level_5_number")

	def getDict(self, id=True, student_score=True, level=True, student_score_number=True, level_number=True):
		ret = {}
		if id: 						ret['id'] = self.id
		if student_score: 			ret['student_score'] = self.student_score
		if level: 					ret['level'] = self.level
		if student_score_number: 	ret['student_score_number'] = self.student_score_number
		if level_number:
			ret['level_number'] = self.level_number
			ret['level_1_number'] = self.level_1_number
			ret['level_2_number'] = self.level_2_number
			ret['level_3_number'] = self.level_3_number
			ret['level_4_number'] = self.level_4_number
			ret['level_5_number'] = self.level_5_number

		return ret

class LectureComment(models.Model):
	class Meta:
		db_table = "lectureComment"
		ordering = ["-rank_score"]

	lecture = models.ForeignKey(Lecture, db_column = "lecture_id")
	user = models.ForeignKey(User, db_column = "user_id")
	content = models.TextField(db_column = "content")
	super_weight = models.FloatField(default = 0.0, db_column = "super_weight")
	super_number = models.IntegerField(default = 0, db_column = "super_number")
	rank_score = models.FloatField(default = 0.0, db_column = "rank_score")
	need_recompute = models.BooleanField(default=True, db_column = "need_recompute")
	time = models.DateTimeField(auto_now_add = True, db_column = "time")

	def getDict(self, id=True, content=True, super_number=True, time=True, user=False):
		ret = {}
		if id: 			ret['id'] = self.id
		if content:		ret['content'] = self.content
		if super_number:ret['super_number'] = self.super_number
		if time:		ret['time'] = formatTime(self.time)
		if user:		ret['user'] = self.user.getDict()

		return ret

class LectureCommentSuperRecord(models.Model):
	class Meta:
		db_table = "lectureCommentSuperRecord"

	lecture_comment = models.ForeignKey(LectureComment, db_column = "lectureComment_id")
	user = models.ForeignKey(User, db_column = "user_id")
	time = models.DateTimeField("data published", db_column = "time")

class LectureLevelRecord(models.Model):
	class Meta:
		db_table = "lectureLevelRecord"

	lecture = models.ForeignKey(Lecture, db_column = "lecture_id")
	user = models.ForeignKey(User, db_column = "user_id")
	level = models.SmallIntegerField(db_column = "level")
	time = models.DateTimeField("data published", db_column = "time")

class LectureStudentScoreRecord(models.Model):
	class Meta:
		db_table = "lectureStudentScoreRecord"

	lecture = models.ForeignKey(Lecture, db_column = "lecture_id")
	user = models.ForeignKey(User, db_column = "user_id")
	score = models.SmallIntegerField(db_column = "score")
	time = models.DateTimeField("data published", db_column = "time")

class UserLectureCollection(models.Model):
	class Meta:
		db_table = "userLectureCollection"
		ordering = ["-time"]

	user = models.ForeignKey(User, db_column = "user_id")
	lecture = models.ForeignKey(Lecture, db_column = "lecture_id")
	time = models.DateTimeField("data published", db_column = "time")


