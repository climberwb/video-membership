
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
        
        comment_form = CommentForm(request.POST or None)
        
        if comment_form.is_valid():
            # print('try3')
            comment_text = comment_form.cleaned_data['comment']
            parent_id = request.POST.get('parent_id')
            # print(comment_text, parent_id)
            # print(parent_id)
    #         if(parent_id is not None):
    #             try: 
    #                 print('try')
    #                 print(parent_id)
    #                 parent_comment = Comment.objects.get(id=parent_id)
    #                 print(parent_comment)
    #                 new_comment = Comment.objects.create_comment(
    #                             user=request.user, 
    #                             path=request.get_full_path(),
    #                             text=comment_text,
    #                             video = obj,
    #                             parent=parent_comment)
    #                 print(new_comment)
    #             except:
    #                 parent_comment = None
    #         else:
    #             new_comment = Comment.objects.create_comment(
    #                             user=request.user, 
    #                             path=request.get_full_path(),
    #                             text=comment_text,
    #                             video = obj)
               
    #     ## TODO Render comment thread
    except:
        # raise Http404 
        pass
    
    
       
   
    
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
    
    