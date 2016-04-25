from django.shortcuts import render, Http404
from .models import Video

# Create your views here.
def video_detail(request,id):
    try:
        obj  = Video.objects.get(id=id)
        context = {
            "object":obj
        }
        return render(request, "videos/video_detail.html",context)
    except:
        raise Http404 
    
    
    
def video_list(request):
    queryset = Video.objects.all()
    context = {
        "queryset":queryset
    }
    return render(request, "videos/video_single.html",context)
    



# def video_edit(request):
#     return render(request, "videos/video_single.html",{})

# def video_create(request):
#     return render(request, "videos/video_single.html",{})