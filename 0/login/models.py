from django.db import models

# Create your models here.
class User(models.Model):
	class Meta:
		db_table = "user"

	name = models.CharField(max_length = 50, db_column = "name")
	password = models.CharField(max_length = 50, db_column = "password")
	join_time = models.DateField('data published', db_column = "join_time")
	account = models.CharField(max_length = 50, db_column = "account")
	check_code = models.BigIntegerField(default = 0, db_column = "check_code")
	check_status =  models.BooleanField(default=True, db_column = "check_status")
	formal = models.BooleanField(default = False, db_column = "formal")
	influence_factor = models.IntegerField(default = 0, db_column = "influence_factor")

	def __unicode__(self):
		return self.account

class RegisteringUser(models.Model):
	class Meta:
		db_table = "registeringUser"
		
	name = models.CharField(max_length = 50, db_column = "name")
	password = models.CharField(max_length = 50, db_column = "password")
	status = models.CharField(max_length = 10, db_column = "status")
	account = models.CharField(max_length = 50, db_column = "account")