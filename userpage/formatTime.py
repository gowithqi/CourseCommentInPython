# -*- coding: utf-8 -*-
from datetime import datetime, date

def formatTime(i_time):
	time_delta = computeTimeDelta(i_time)
	print time_delta

	if "seconds" in time_delta: return str(time_delta["seconds"]) + u"秒前"
	elif "minutes" in time_delta: return str(time_delta["minutes"]) + u"分钟前"
	else:
		today = date.today()
		delta_day = today - i_time.date()
		if delta_day.days == 0: return u"今天 " + i_time.strftime("%H:%M")
		elif delta_day.days == 1: return u"昨天 " + i_time.strftime("%H:%M")
		elif delta_day.days == 2: return u"前天 " + i_time.strftime("%H:%M")
		elif delta_day.days == 3: return u"3天前 " + i_time.strftime("%H:%M")
		else: pass
	return  i_time.strftime("%Y-%m-%d  %H:%M")

def computeTimeDelta(i_time):
	t = datetime.now() - i_time

	t = t.total_seconds()   #second
	if t < 60: return {"seconds": int(t)}
	t = t / 60		#minute
	if t < 60: return {"minutes": int(t)}
	t = t / 60		#hour
	if t < 24: return {"hours": int(t)} 
	t = t / 24		#day
	if t < 30: return {"days": int(t)}
	t = t / 30 		#month
	if t < 12: return {"month": int(t)}
	t = t / 12
	return {"year": int(t)}