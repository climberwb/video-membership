
from django.core.urlresolvers import reverse
from django.shortcuts import render, Http404, get_object_or_404
from .models import Video,Category, TaggedItem
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from analytics.signals import page_view
from comments.models import Comment
from comments.forms import CommentForm
from .models import Video,Category

# Create your views here.



    
def category_list(request):
    queryset = Category.objects.all()
    context = {
        "queryset":queryset
    }
    return render(request, "videos/category_list.html",context)
   
def category_detail(request,cat_slug):
    cat = get_object_or_404(Category,slug=cat_slug)
    queryset = cat.video_set.all()
    page_view.send(request.user,
        page_path=request.get_full_path(),
        primary_obj=cat)
    context = {
        "object":cat,
        "queryset":queryset
        }
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



# Create your views here.


# @login_required 
def video_detail(request,cat_slug,vid_slug):
    
    # try:
    cat = get_object_or_404(Category,slug=cat_slug)
    # cat = Category.objects.get(slug=cat_slug)
    obj = get_object_or_404(Video, slug=vid_slug, category=cat)
    page_view.send(request.user,
        page_path=request.get_full_path(),
        primary_obj=obj, 
        secondary_obj=cat)
    
    # obj  = Video.objects.get(slug=vid_slug)
    if request.user.is_authenticated() or obj.has_preview:
        comments = Comment.objects.filter(video=obj)
        content_type = ContentType.objects.get_for_model(obj)
        tags = TaggedItem.objects.filter(content_type=content_type,object_id=obj.id)
        print(obj.tags.all())
        comment_form = CommentForm()
    
        context = {
            "object":obj,
            "comments":comments,
            "comment_form":comment_form
    
        }
        return render(request, "videos/video_detail.html",context)
    else:
        next_url = obj.get_absolute_url
        return httpResponseRediect('%s?next=%s'%(reverse('login'),nex_url))
    
    
def category_list(request):
    queryset = Category.objects.all()
    
    context = {
        "queryset":queryset
    }
    return render(request, "videos/category_list.html",context)
   



    
def video_list(request):
    queryset = Video.objects.all()
    print('queryset')
    context = {
        "queryset":queryset
    }
    return render(request, "videos/video_list.html",context)
    
    