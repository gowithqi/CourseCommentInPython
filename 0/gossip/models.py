from django.db import models
from login.models import User
from lecture.models import Lecture

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

class GossipSuperRecord(models.Model):
	class Meta:
		db_table = "gossipSuperRecord"

	user = models.ForeignKey(User, db_column = "user_id")
	gossip = models.ForeignKey(Gossip, db_column = "gossip_id")
	time = models.DateTimeField("data published", db_column = "time")


