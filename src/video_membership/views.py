from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from videos.models import Video
from django.utils.safestring import mark_safe
from .forms import LoginForm

@login_required(login_url='/login')
def home(request):
    videos = Video.objects.all()
    
    embeds = ["%s" %(mark_safe(vid.embed_code))for vid in videos]
        
    context={
        "videos":videos,
       "numbers": videos.count(),
       "embeds":embeds
    }
    return render(request,"home.html",context)
    

# @login_required(login_url='/enroll/login')
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def auth_login(request):
    form = LoginForm(request.POST  or None)
    next_url = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url)
    context={"form":form}
    return render(request,"login.html",context)
# def home(request):
#     if request.user.is_authenticated():

#         videos = Video.objects.all()
        
#         embeds = ["%s" %(mark_safe(vid.embed_code))for vid in videos]
            
#         context={
#             "videos":videos,
#           "numbers": videos.count(),
#           "embeds":embeds
#         }
#         return render(request,"home.html",context)
#     else:
#         return HttpResponseRedirect('/login/')