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
from analytics.signals import page_view 
from comments.models import Comment


from analytics.models import PageView
from videos.models import Video
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

# @login_required(login_url='login/')
def home(request):
    # print request.user.pageview_set.get_videos()
    page_view.send(
        request.user,
        page_path=request.get_full_path())
    if request.user.is_authenticated():
        page_view_objects = request.user.pageview_set.get_videos()[:6]

        recent_videos=[]
        for  obj in page_view_objects:
            if not obj.primary_object in recent_videos:
                recent_videos.append(obj.primary_object)
        recent_comments = Comment.objects.recent()
        


        #top itmes
        video_type = ContentType.objects.get_for_model(Video)
        popular_videos = PageView.objects.filter(primary_content_type=video_type).values("primary_object_id")\
                                .annotate(the_count=Count("primary_object_id"))\
                                .order_by("-the_count")[:10]
        
        
        
        # one item
        # pageView.objects.filter(primary_content_type=video_type,primary_object_id=6).count()
        
        popular_videos_list=[]
        for item in popular_videos:
            try:
                new_video = Video.objects.get(id=item['primary_object_id'])
                popular_videos_list.append(new_video)
            except:
                pass
        
        context ={"recent_videos":recent_videos,
                  "recent_comments": recent_comments,
                  "popular_videos": popular_videos_list
                    
        }
        template = "home_logged_in.html"
        
    else:
        login_form = LoginForm(request.POST or None)
        register_form =  RegistrationForm(request.POST or None)
        template = "home_visitor.html"
        context = {"register_form":register_form,"login_form":login_form}
    
    return render(request,template,context)
    

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