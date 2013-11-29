# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timedelta, date
register = template.Library()

@register.filter
def getkey(value, key):
	return value[key]

@register.filter
def div(value, key):
	value = int (value)
	key = int (key)
	if key == 0: return 0
	res = float(value)/key
	return int(res*100)

@register.filter
def formatTime(i_time):
	time_delta = computeTimeDelta(i_time)
	print time_delta

	if "seconds" in time_delta: return str(time_delta["seconds"]) + u"秒前"
	elif "minutes" in time_delta: return str(time_delta["minutes"]) + u"分钟前"
	else:
		today = date.today()
		delta_day = today - i_time.date()
		if delta_day == 0: return u"今天 " + i_time.strftime("%H:%M:%S")
		elif delta_day == 1: return u"昨天 " + i_time.strftime("%H:%M:%S")
		elif delta_day == 2: return u"前天 " + i_time.strftime("%H:%M:%S")
		elif delta_day == 3: return u"3天前 " + i_time.strftime("%H:%M:%S")
		else: pass
	return  i_time.strftime("%Y-%m-%d %H:%M:%S")

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
	# if t < 60: return str(int(t)) + "秒"
	# t = t / 60		#minute
	# if t < 60: return str(int(t)) + "分"
	# t = t / 60		#hour
	# if t < 24: return str(int(t)) + "小时"
	# t = t / 24		#day
	# if t < 30: return str(int(t)) + "天"
	# t = t / 30 		#month
	# if t < 12: return str(int(t)) + "月"
	# t = t / 12
	# return str(int(t)) + "年" 