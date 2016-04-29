from __future__ import unicode_literals

from django.db import models
from accounts.models import MyUser
from videos.models import Video

class CommentManager(models.Manager):
    def create_comment(self,user=None,path=None,text=None,video=None):
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
            text=text
        )
        
        if video is not None:
            comment.video = video
        
        comment.save(using=self._db)
        
        return comment

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    text = models.TextField()
    video = models.ForeignKey(Video)
    path = models.CharField(max_length=350)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    active = models.BooleanField(default=True)
    
    objects = CommentManager()
    def __unicode__(self):
        return self.user.username
        
    def __str__(self):
        return self.user.username
