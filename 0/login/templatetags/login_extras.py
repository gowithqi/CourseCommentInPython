# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timedelta
register = template.Library()

@register.filter
def computeTimeDelta(i_time):
	t = datetime.now() - i_time

	t = t.total_seconds()   #second
	if t < 60: return str(int(t)) + u"秒"
	t = t / 60		#minute
	if t < 60: return str(int(t)) + u"分"
	t = t / 60		#hour
	if t < 24: return str(int(t)) + u"小时"
	t = t / 24		#day
	if t < 30: return str(int(t)) + u"天"
	t = t / 30 		#month
	if t < 12: return str(int(t)) + u"月"
	t = t / 12
	return str(int(t)) + u"年"