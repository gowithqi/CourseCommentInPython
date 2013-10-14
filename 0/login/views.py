# Create your views here.
from django.http import HttpResponse

def login(request):
	return HttpResponse("Hello Moto!")
	