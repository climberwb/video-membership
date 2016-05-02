from django.shortcuts import render, Http404,HttpResponseRedirect

from .models import Comment
from django.contrib.auth.decorators import login_required
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
        parent_comment = Comment.objects.get(id=parent_id)
        video = parent_comment.video
        comment_text = form.cleaned_data['comment']
        
        
        print(parent_comment.get_origin, video, request.user)
        new_comment = Comment.objects.create_comment(
                            user=request.user, 
                            path=parent_comment.get_origin,
                            text=comment_text,
                            parent = parent_comment,
                            video = video)
            # else:
            #     new_comment = Comment.objects.create_comment(
            #                         user=request.user, 
            #                         path=parent.get_origin,
            #                         text=comment_text,
            #                         video = obj)
    
        return HttpResponseRedirect(new_comment.get_origin)#comment origin
    else:
        raise Http404