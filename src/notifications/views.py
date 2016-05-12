import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from .models import Notification
# Create your views here.

@login_required
def all(request):
    notifications = Notification.objects.all_for_user(request.user)
    context = {
        "notifications":notifications
    }
    return render(request,"notifications/all.html",context)
    
@login_required   
def read(request,id):
    next = request.GET.get('next',None)
    notification = Notification.objects.get(id=id)
    if notification.recipient == request.user:
        notification.read = True
        notification.save()
        if next is not None:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect(reverse("notifications_all"))
    else:
        raise Http404
        
@login_required       
def get_notifications_ajax(request):
    if request.is_ajax() and request.method == "POST":
        notifications = Notification.objects.all_for_user(request.user).recent()
        notes = [note.get_link for note in notifications]
        data ={
            "notifications":notes
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data,content_type="application/json")
    else:
        raise Http404
    
    