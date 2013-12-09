from datetime import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from login.models import User
from gossip.models import Gossip, GossipSuperRecord
from comment.influence import increaseSysAchievement, updateUserInfluence

GOSSIPS_NUMBER = 50
GOSSIP_MAX_LENGTH = 300
START_TIME = datetime(year=2013, month=11, day=11)
SUPER_VALUE = 10

GOSSIP_SUPER_VALUE_INFLUENCE = 1

@require_http_methods(['GET'])
def gossip(request):
	user_id = checkUserLogin(request)
	user = get_object_or_404(User, id=user_id)

	gossips = Gossip.objects.all()[:GOSSIPS_NUMBER]
	template = loader.get_template("gossip/gossip.html")
	context = RequestContext(request, {
		'gossips': gossips,
		'u': user,
		})
	
	return HttpResponse(template.render(context))

# a gossip with its author hidden, the user id will be 0.
# a gossip that isn't for a specific lecture, the lecture id will 0
@require_http_methods(['POST'])
def recordGossip(request):
	user_id = 0
	if 'user_id' in request.session: user_id = request.session['user_id']
	if not checkGossipContent(request.POST['content']): return HttpResponse("wrong")

	if 'lecture_id' in request.POST: lecture_id = int(request.POST['lecture_id'])
	else: lecture_id = 0
	if 'user_id' in request.POST: user_id = 0
	
	now = datetime.now()
	delta_t = now - START_TIME
	Gossip.objects.create(user_id=user_id, 
		lecture_id=lecture_id,
		content=request.POST['content'],
		rank_score=int(delta_t.total_seconds()/1800))

	return HttpResponse("yes")

def checkGossipContent(content):
	# length
	if len(content) > GOSSIP_MAX_LENGTH: return False
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
		updateUserInfluence(gossip.user, GOSSIP_SUPER_VALUE_INFLUENCE)
		gossip.save()
	else:
		gossip_super_record = get_object_or_404(GossipSuperRecord, user_id=user_id, gossip = gossip)
		gossip_super_record.delete()
		gossip.rank_score = gossip.rank_score - SUPER_VALUE
		if gossip.super_number > 0: gossip.super_number = gossip.super_number - 1
		updateUserInfluence(gossip.user, -1 * GOSSIP_SUPER_VALUE_INFLUENCE)
		gossip.save()
		
	return HttpResponse("yes")
