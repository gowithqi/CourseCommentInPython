from django.db import models
from login.models import User


class Gossip(models.Model):
	class Meta:
		db_table = "gossip"

	user = models.ForeignKey(User, db_column = "user_id")
	content = models.TextField(db_column = "content")
	super_number = models.IntegerField(db_column = "super_number")
	time = models.DateTimeField("data published", db_column = "time")

class GossipSuperRecord(models.Model):
	class Meta:
		db_table = "gossipSuperRecord"

	user = models.ForeignKey(User, db_column = "user_id")
	gossip = models.ForeignKey(Gossip, db_column = "gossip_id")
	time = models.DateTimeField("data published", db_column = "time")


