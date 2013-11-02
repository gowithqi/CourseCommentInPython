from django.db import models

# Create your models here.
from login.models import User
from lecture.models import LectureComment

class MessageOfCommentSuper(models.Model):
	class Meta:
		db_table = "messageOfCommentSuper"

	user = models.ForeignKey(User, db_column="user_id")
	lecture_comment = models.ForeignKey(LectureComment, db_column="lecture_comment_id")
	super_added = models.IntegerField(default=1, db_column="super_added")

