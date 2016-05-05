
from django.shortcuts import render, Http404
from .models import Video,Category, TaggedItem
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.



    
def category_list(request):
    queryset = Category.objects.all()
    context = {
        "queryset":queryset
    }
    return render(request, "videos/category_list.html",context)
   
@login_required 
def category_detail(request,cat_slug):
    try:
        cat = Category.objects.get(slug=cat_slug)
        queryset = cat.video_set.all()
        context = {
            "object":cat,
            "queryset":queryset
            }
        ## TODO left at 10:43 
       
    except:
        raise Http404
    return render(request, "videos/category_detail.html",context)
        
    
def video_list(request):
    queryset = Video.objects.all()
    context = {
        "queryset":queryset
    }
    return render(request, "videos/video_list.html",context)
    
    



# def video_edit(request):
#     return render(request, "videos/video_single.html",{})

# def video_create(request):
#     return render(request, "videos/video_single.html",{})from django.shortcuts import render, Http404
from .models import Video,Category
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required 
def video_detail(request,cat_slug,vid_slug):
    
    # try:
    cat = Category.objects.get(slug=cat_slug)
    obj  = Video.objects.get(slug=vid_slug)
    comments = Comment.objects.filter(video=obj)
    content_type = ContentType.objects.get_for_model(obj)
    tags = TaggedItem.objects.filter(content_type=content_type,object_id=obj.id)
    print(tags)
    comment_form = CommentForm()
    # except:
    #     raise Http404
      #  pass

    context = {
        "object":obj,
        "comments":comments,
        "comment_form":comment_form

    }
    return render(request, "videos/video_detail.html",context)
    
    
def category_list(request):
    queryset = Category.objects.all()
    print(queryset[0].title)
    context = {
        "queryset":queryset
    }
    return render(request, "videos/category_list.html",context)
   
@login_required 
def category_detail(request,cat_slug):
    try:
        cat = Category.objects.get(slug=cat_slug)
        queryset = cat.video_set.all()
        context = {
            "object":cat,
            "queryset":queryset
            }
        ## TODO left at 10:43 
       
    except:
        raise Http404
    return render(request, "videos/category_detail.html",context)
        
    
def video_list(request):
    queryset = Video.objects.all()
    print('queryset')
    context = {
        "queryset":queryset
    }
    return render(request, "videos/video_list.html",context)
    
    