from django.shortcuts import render, Http404
from .models import Video,Category

# Create your views here.



def video_detail(request,cat_slug,id):
    try:
        cat = Category.objects.get(slug=cat_slug)
    except:
        raise Http404
    try:
        obj  = Video.objects.get(id=id)
        context = {
            "object":obj
        }
        return render(request, "videos/video_detail.html",context)
    except:
        raise Http404 
    
    
    
def category_list(request):
    queryset = Category.objects.all()
    context = {
        "queryset":queryset
    }
    return render(request, "videos/video_single.html",context)
    
def category_detail(request,cat_slug):
   try:
        cat = Category.objects.get(slug=cat_slug)
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