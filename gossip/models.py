from django.db import models
from login.models import User
from lecture.models import Lecture
from userpage.formatTime import formatTime

class Gossip(models.Model):
	class Meta:
		db_table = "gossip"
		ordering = ["-rank_score"]

	user = models.ForeignKey(User, db_column = "user_id")
	lecture = models.ForeignKey(Lecture, db_column="lecture_id")
	content = models.TextField(db_column = "content")
	super_number = models.IntegerField(default = 0, db_column = "super_number")
	time = models.DateTimeField(auto_now_add = True, db_column = "time")
	rank_score = models.IntegerField(default=0, db_column="rank_score")

	def getDict(self, id=True, content=True, super_number=True, time=True, user=False):
		ret = {}
		if id: 			ret['id'] = self.id
		if content:		ret['content'] = self.content
		if super_number: 		ret['super_number'] = self.super_number
		if time:		ret['time'] = formatTime(self.time)
		if user:		ret['user'] = self.user.getDict()

		return ret

class GossipSuperRecord(models.Model):
	class Meta:
		db_table = "gossipSuperRecord"

	user = models.ForeignKey(User, db_column = "user_id")
	gossip = models.ForeignKey(Gossip, db_column = "gossip_id")
	time = models.DateTimeField("data published", db_column = "time")


