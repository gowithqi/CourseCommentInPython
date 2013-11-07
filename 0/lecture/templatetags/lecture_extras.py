from django import template

register = template.Library()

@register.filter
def getkey(value, key):
	return value[key]