from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from videos.models import Video
from django.utils.safestring import mark_safe

# @login_required(login_url='/enroll/login')
@login_required
def home(request):
    videos = Video.objects.all()
    
    embeds = ["%s" %(mark_safe(vid.embed_code))for vid in videos]
        
    context={
        "videos":videos,
       "numbers": videos.count(),
       "embeds":embeds
    }
    return render(request,"home.html",context)
    

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