from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.db import models
from .signals import notify
# Create your models here.


class Notification(models.Model):
    # sender = 
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notifications')
    #action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    
    sender_content_type = models.ForeignKey(ContentType,related_name='notify_sender')
    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey("sender_content_type","sender_object_id")
    
    verb = models.CharField(max_length=255)
    
    action_content_type = models.ForeignKey(ContentType,related_name='notify_action',null=True,blank=True)
    action_object_id = models.PositiveIntegerField()
    action_object = GenericForeignKey("action_content_type","action_object_id")
    
    target_content_type = models.ForeignKey(ContentType,related_name='notify_target',null=True,blank=True)
    target_object_id = models.PositiveIntegerField()
    target_content_object = GenericForeignKey("target_content_type","target_object_id")
    
    def __unicode__(self):
        return str(self.verb)
        
def new_notification(sender,recipient,action,*args,**kwargs):
    print(recipient)
    print action
    if(recipient is None):
        recipient = 0
    else:
        new_notification_create = Notification.objects.create(recipient=recipient,action=action,)
    print sender
    print args
    print kwargs

notify.connect(new_notification)
