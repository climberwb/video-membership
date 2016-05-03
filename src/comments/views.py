from django.shortcuts import render, Http404,HttpResponseRedirect

from .models import Comment
from videos.models import Video
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CommentForm

# Create your views here.
@login_required
def comment_thread(request,id):
    parent_comment = Comment.objects.get(id=id)
    child_comments = parent_comment.get_children()
    form = CommentForm( None)
    context = {
        "parent_comment":Comment.objects.get(id=id),
        "child_comments":child_comments,
        "comment_form":form
    }
    return render(request,"comments/comment_thread.html",context)
@login_required
def comment_create(request):
    form = CommentForm(request.POST)
    if form.is_valid() and request.method == "POST" and request.user.is_authenticated():
        
        # fields needed to create child comment
        parent_id = request.POST.get('parent_id')
        print(parent_id,"parent_id")
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
            video = parent_comment.video
        else:
            origin_path = request.POST.get('origin_path')
            vid_slug = origin_path.split("/")[3]
            print(vid_slug)
            video = Video.objects.get(slug=vid_slug)
            
        comment_text = form.cleaned_data['comment']
        
        
        if(parent_id is not None):
            new_comment = Comment.objects.create_comment(
                                user=request.user, 
                                path=parent_comment.get_origin,
                                text=comment_text,
                                parent = parent_comment,
                                video = video)
            if new_comment.was_saved:
                messages.success(request,"Thank you for adding your comment")
                messages.add_message(request, messages.INFO, 'Hello world.')
                
                return HttpResponseRedirect(new_comment.get_origin)
        else:
            new_comment = Comment.objects.create_comment(
                                user=request.user, 
                                path=video.get_absolute_url(),
                                text=comment_text,
                                video = video)
            return HttpResponseRedirect(video.get_absolute_url())
            
            # else:
            #     new_comment = Comment.objects.create_comment(
            #                         user=request.user, 
            #                         path=parent.get_origin,
            #                         text=comment_text,
            #                         video = obj)
    
        #comment origin
    else:
        raise Http404