from __future__ import unicode_literals

from django.db import models
from accounts.models import MyUser
from videos.models import Video

class CommentManager(models.Manager):
    def all(self):
        return super(CommentManager,self).filter(active=True).filter(parent=None)
        
        

    def create_comment(self,user=None, path=None,text=None,video=None,parent=None):
        """
        Creates and saves a comment to a video
        """
        if not path:
            raise ValueError('Must include path when adding comment')
            
        if not user:
            raise ValueError('Must include user when adding comment')
        
            
        comment = self.model(
            user=user,
            path=path,
            text=text,
            parent=parent
        )
        
        if video is not None:
            comment.video = video
        
        comment.save(using=self._db)
        
        return comment

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    parent = models.ForeignKey("self",null=True, blank=True)
    text = models.TextField()
    video = models.ForeignKey(Video)
    path = models.CharField(max_length=350)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    active = models.BooleanField(default=True)
    
    objects = CommentManager()
    
    class Meta:
        ordering=['-timestamp']
    
    def __unicode__(self):
        return self.user.username
        
    def __str__(self):
        return self.user.username
    
    @property
    def is_child(self):
        if self.parent is not None:
            return True
        else:
            return False
    
    def get_children(self):
        if self.is_child:
            return None
        else:
            return Comment.objects.filter(parent=self)