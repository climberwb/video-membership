from django.shortcuts import render
from videos.models import Video

def home(request):
    videos = Video.objects.all()
    context={
        "videos":videos,
       "numbers": videos.count()
    }
    return render(request,"home.html",context)