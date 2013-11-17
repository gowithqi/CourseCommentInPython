import os

from login.models import User

def increaseSysAchievement():
	if 'SERVER_SOFTWARE' in os.environ:
		from bae.api.counter import BaeCounter
		cr = BaeCounter()
		cr.increase('achievement')
	return

def updateUserInfluence(user, delta):
	user.influence_factor = user.influence_factor + delta
	user.save()
	if 'SERVER_SOFTWARE' in os.environ:
		from bae.api.rank import BaeRank
		from bae.api import logging
		r = BaeRank("UserInfluence")
		user_key = str(user.id)
		user_influence = int(user.influence_factor)
		user_dict = {user_key: user_influence}
		logging.debug(str(user_dict))
		r.set(**user_dict)

	return

def getSysAchievement():
	res = 0
	if 'SERVER_SOFTWARE' in os.environ:
		from bae.api.counter import BaeCounter
		cr = BaeCounter()
		res = cr.get('achievement')
	return	res