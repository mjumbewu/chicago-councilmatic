# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from phillyleg.models import Subscription,KeywordSubscription,LegFile,CouncilMember,CouncilMemberSubscription
from django.template import Context, loader
from django.views.generic.list_detail import object_list

def index(request):
    return object_list(request, Subscription.objects.all())

def subscribe(request):
    t = loader.get_template('subscribe.html')
    c = Context({
    	'council_members': CouncilMember.objects.all()
    })
    return HttpResponse(t.render(c))

def create(request):
    emailvar = request.POST['email']
    s = Subscription(email = emailvar)
    s.save()
    keywords = request.POST['keywords']
    keylist = keywords.split(",") 
    for word in keylist:
        k = KeywordSubscription(keyword = word, subscription = s)
        k.save()
    members = request.POST.getlist('council')
    ret_members = []
    for mem in members:
    	cmember = CouncilMember.objects.get(id=mem)
    	ret_members.append(cmember)
        cm = CouncilMemberSubscription(councilmember = cmember, subscription = s)
        cm.save()
    t = loader.get_template('received.html')
    c = Context({
        'emailvar': emailvar,
        'keylist': keylist,
        'members': ret_members
    })
    return HttpResponse(t.render(c))

def unsubscribe(request):
    t = loader.get_template('editsubscribe.html')
    c = Context()
    return HttpResponse(t.render(c))

def delete(request):
    t = loader.get_template('unsubscribed.html')
    emailvar = request.POST['email']
    s = Subscription.objects.filter(email = emailvar)
    for item in s:
        item.delete()
    c = Context({
        'email': emailvar
    })
    return HttpResponse(t.render(c))

def dashboard(request, subscription_id):
    subscription = Subscription(pk=subscription_id)
    t = loader.get_template('dashboard.html')
    c = Context({
        'user':subscription
    })
    return HttpResponse(t.render(c))

# ==============================================================================

from django.contrib.auth.decorators import login_required

@login_required
def add_bookmark(request, pk):
    legfile = LegFile.objects.get(pk=pk)
    if request.user not in legfile.bookmarks.all():
        legfile.bookmarks.add(request.user)
    return HttpResponseRedirect(request.GET.get('next', '/'))
