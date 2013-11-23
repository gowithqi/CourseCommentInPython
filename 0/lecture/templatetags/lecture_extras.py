from django import template

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