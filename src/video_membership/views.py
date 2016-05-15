from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe



from accounts.forms import RegistrationForm
from accounts.models import MyUser
from videos.models import Video

from .forms import LoginForm
from accounts.forms import RegistrationForm
from .forms import LoginForm


@login_required(login_url='login/')
def home(request):
    if request.user.is_authenticated():
        context ={}
    else:
        login_form = LoginForm(request.POST or None)
        register_form =  RegistrationForm(request.POST or None)
        context = {"register_form":register_form,"login_form":login_form}
    
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