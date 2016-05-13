from django.shortcuts import render, Http404,HttpResponseRedirect

from .models import Comment
from videos.models import Video
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from notifications.signals import notify
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
        origin_path = request.POST.get('origin_path')
        print(origin_path)
        # fields needed to create child comment
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
            video = parent_comment.video
        else:
            vid_slug = origin_path.split("/")[3]
            video = Video.objects.get(slug=vid_slug)
            
        comment_text = form.cleaned_data['comment']
        
       # try:
        if(parent_id is not None):
            new_comment = Comment.objects.create_comment(
                                user = request.user, 
                                path=parent_comment.get_origin,
                                text=comment_text,
                                parent = parent_comment,
                                video = video)
           
            affected_users = parent_comment.get_affected_users()
            notify.send(request.user,
                action=new_comment,
                target=parent_comment, 
                recipient=parent_comment.user, 
                affected_users = affected_users,
                verb="replied to")
            messages.success(request,"Congrats your commnet was saved ")
            return HttpResponseRedirect(new_comment.get_origin)
        else:
            new_comment = Comment.objects.create_comment(
                                user=request.user, 
                                path=video.get_absolute_url(),
                                text=comment_text,
                                video = video)
            # option to send to super user or staff users
            # notify.send(request.user, 
            #     action=new_comment,
            #     recipient=request.user,
            #     target = new_comment.video,
            #     verb="commented")
            
            messages.success(request,"Congrats your commnet was saved ")
            return HttpResponseRedirect(video.get_absolute_url())
       # except:
            messages.error(request,"Your comment did not save. Please try again. ")
            return HttpResponseRedirect(origin_path)
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