from datetime import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from login.models import User
from gossip.models import Gossip, GossipSuperRecord

GOSSIPS_NUMBER = 50
START_TIME = datetime(year=2013, month=11, day=11)
SUPER_VALUE = 10

@require_http_methods(['GET'])
def gossip(request):
	gossips = Gossip.objects.all()[:GOSSIPS_NUMBER]
	template = loader.get_template("gossip/gossip.html")
	context = RequestContext(request, {
		'gossips': gossips,
		})
	
	return HttpResponse(template.render(context))

@require_http_methods(['POST'])
def recordGossip(request): 
	user_id = 0 
	if 'user_id' in request.session: user_id = request.session['user_id']
	if not checkGossipContent(request.POST['content']): return HttpResponse("wrong")

	now = datetime.now()
	delta_t = now - START_TIME
	Gossip.objects.create(user_id=user_id, 
		content=request.POST['content'],
		rank_score=int(delta_t.total_seconds()/60))

	return HttpResponse("yes")

def checkGossipContent(content):
	# length
	if len(content) > 300: return False
	return True
	
@require_http_methods(['GET'])
def superGossip(request, super_action, gossip_id): 
	user_id = 0 
	if 'user_id' in request.session: user_id = request.session['user_id']
	gossip_id = int(gossip_id)
	gossip = get_object_or_404(Gossip, id=gossip_id)

	if str(super_action) == "super":
		GossipSuperRecord.objects.create(user_id=user_id, gossip = gossip)
		gossip.rank_score = gossip.rank_score + SUPER_VALUE
		gossip.super_number = gossip.super_number + 1
		gossip.save()
	else:
		gossip_super_record = get_object_or_404(GossipSuperRecord, user_id=user_id, gossip = gossip)
		gossip_super_record.delete()
		gossip.rank_score = gossip.rank_score - SUPER_VALUE
		if gossip.super_number > 1: gossip.super_number = gossip.super_number - 1
		gossip.save()
		
	return HttpResponse("yes")
