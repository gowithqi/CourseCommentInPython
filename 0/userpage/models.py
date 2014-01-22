from django.db import models
from lecture.models import Lecture, LectureComment
from gossip.models import Gossip
from login.models import User

# Create your models here.
class MessageTopic(models.Model):
	class Meta:
		db_table = "messageTopic"

	topic = models.CharField(max_length=50, db_column = "topic")
	user = models.ForeignKey(User, db_column = "user_id")

class MessageWords(models.Model):
	class Meta:
		db_table = "messageWords"

	message_topic = models.ForeignKey(MessageTopic, db_column = "message_topic_id")
	content = models.TextField(db_column = "content")
	user = models.ForeignKey(User, db_column = "user_id")


# the new message system
# message_id is the id of the table determined by message_type
# message_type = 0, refer to messageOfCommentSupered
# 			   = 1, refer to messageOfGossipSupered
#			   = 2, refer to messageOfDMessageTopic
# user is the message reader 
class Message(models.Model):
	class Meta:
		db_table = "message"

	user = models.ForeignKey(User, db_column = "user_id")
	message_id = models.IntegerField(db_column = "message_id")
	message_type = models.IntegerField(db_column = "message_type")

#user is the message maker
class MessageOfCommentSupered(models.Model):
	class Meta:
		db_table = "messageOfCommentSupered"

	user = models.ForeignKey(User, db_column = "user_id")
	lecture_comment = models.ForeignKey(LectureComment, db_column = "lecture_comment_id")

#user is the message maker
class MessageOfGossipSupered(models.Model):
	class Meta:
		db_table = "messageOfGossipSupered"

	user = models.ForeignKey(User, db_column = "user_id")
	gossip = models.ForeignKey(Gossip, db_column = "gossip_id")

#user is the message maker
class MessageOfMessageTopic(models.Model):
	class Meta:
		db_table = "messageOfMessageTopic"

	user = models.ForeignKey(User, db_column = "user_id")
	message_topic = models.ForeignKey(MessageTopic, db_column = "message_topic_id")


