from django.shortcuts import render, Http404
from .models import Video,Category
from django.contrib.auth.decorators import login_required
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
    
    try:
        cat = Category.objects.get(slug=cat_slug)
    except:
        raise Http404
    try:
        obj  = Video.objects.get(slug=vid_slug)
        comments = Comment.objects.filter(video=obj)
        # comment_form = CommentForm(request.POST or None)
        # if comment_form.is_valid():
        #     obj_instance = comment_form.save(commit=False)
        #     obj_instance.path = request.get_full_path()
        #     obj_instance.user = request.user
        #     obj_instance.text = request.text
        #     obj_instance.video = obj
        #     obj_instance.save()
        
        #     # print('poop',comments)
        # context = {
        #     "object":obj,
        #     "comments":comments,
        #     "comment_form":comment_form
        # }
        # return render(request, "videos/video_detail.html",context)
    except:
        raise Http404 
    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
            obj_instance = comment_form.save(commit=False)
            obj_instance.path = request.get_full_path()
            obj_instance.user = request.user
            # obj_instance.text = request.text
            obj_instance.video = obj
            obj_instance.save()
        
            # print('poop',comments)
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
    
    



# def video_edit(request):
#     return render(request, "videos/video_single.html",{})

# def video_create(request):
#     return render(request, "videos/video_single.html",{})