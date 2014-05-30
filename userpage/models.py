from django.db import models
from django.shortcuts import get_object_or_404

from lecture.models import Lecture, LectureComment
from gossip.models import Gossip
from login.models import User

# Create your models here.
class MessageTopic(models.Model):
	class Meta:
		db_table = "messageTopic"

	topic = models.CharField(max_length=50, db_column = "topic")
	user = models.ForeignKey(User, db_column = "user_id")

	def getDict(self, topic = True, user = True):
		ret = {}
		if topic: ret['topic'] = self.topic
		if user: ret['user'] = self.user.getDict(influence_factor = False)
		return ret

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
mt_reflect = {
	0: 0,
	1: 1,
	2: 2,
}
class Message(models.Model):
	class Meta:
		db_table = "message"

	user = models.ForeignKey(User, db_column = "user_id")
	message_id = models.IntegerField(db_column = "message_id")
	message_type = models.IntegerField(db_column = "message_type")

	def getDict(self):
		ret = {}
		ret['message_type'] = mt[self.message_type]
		if ret['message_type'] == 0:
			m = get_object_or_404(MessageOfCommentSupered, id = self.message_id)
		elif ret['message_type'] == 1:
			m = get_object_or_404(MessageOfGossipSupered, id = self.message_id)
		elif ret['message_type'] == 2:
			m = get_object_or_404(MessageOfMessageTopic, id = self.message_id)
		else:
			pass

		ret['data'] = m.getDict()
		return ret

#user is the message maker
class MessageOfCommentSupered(models.Model):
	class Meta:
		db_table = "messageOfCommentSupered"

	user = models.ForeignKey(User, db_column = "user_id")
	lecture_comment = models.ForeignKey(LectureComment, db_column = "lecture_comment_id")

	def getDict():
		ret = {}
		ret['lecture_comment'] = self.lecture_comment.getDict()
		ret['user'] = self.user.getDict(influence_factor = False)
		return ret

#user is the message maker
class MessageOfGossipSupered(models.Model):
	class Meta:
		db_table = "messageOfGossipSupered"

	user = models.ForeignKey(User, db_column = "user_id")
	gossip = models.ForeignKey(Gossip, db_column = "gossip_id")
	def getDict():
		ret = {}
		ret['lecture_comment'] = self.lecture_comment.getDict()
		ret['user'] = self.user.getDict(influence_factor = False)
		return ret

#user is the message maker
class MessageOfMessageTopic(models.Model):
	class Meta:
		db_table = "messageOfMessageTopic"

	user = models.ForeignKey(User, db_column = "user_id")
	message_topic = models.ForeignKey(MessageTopic, db_column = "message_topic_id")

	def getDict():
		ret = {}
		ret['message_topic'] = self.message_topic.getDict(user = False)
		ret['user'] = self.user.getDict(influence_factor = False)
		return ret

