from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.db import models
from .signals import notify
# Create your models here.


class NotificationQuerySet(models.query.QuerySet):
    def get_user(self,user):
        return self.filter(recipient=user)
    def unread(self):
        return self.filter(unread=True)
        
    def read(self):
        return self.filter(read=True)
        

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)
        
    def all_unread(self,user):   
        return self.get_queryset().get_user(user).unread()
    
    def all_read(self,user):   
        return self.get_queryset().get_user(user).read()
    
    def all_for_user(self, user):
        return self.get_queryset().get_user(user)
        
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
    action_object_id = models.PositiveIntegerField(null=True)
    action_object = GenericForeignKey("action_content_type","action_object_id")
    
    target_content_type = models.ForeignKey(ContentType,related_name='notify_target',null=True,blank=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target_content_object = GenericForeignKey("target_content_type","target_object_id")
    
    read = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)
    
    objects = NotificationManager()
    
    def __unicode__(self):
        context = {
            "sender": self.sender_object,
            "verb": self.verb,
            "action":self.action_object,
            "target": self.target_content_object
        }
        if self.target_content_object:
            if self.action_object:
                return "%(sender)s %(verb)s with %(action)s"%context
            return "%(sender)s %(verb)s %(target)s"%context
        return "%(sender)s %(verb)s "%context
            
        
        
def new_notification(sender,**kwargs):
    # if(recipient is None):
    #     recipient = 0
    # else:
    #     new_notification_create = Notification.objects.create(recipient=recipient,action=action,)
    print sender
    kwargs.pop('signal',None)
    recipient = kwargs.pop("recipient")
    verb = kwargs.pop("verb")
    new_note = Notification(
            recipient=recipient,
            verb = verb,
            sender_content_type = ContentType.objects.get_for_model(sender),
            sender_object_id = sender.id
        )
    for option in ("target","action"):
        obj = kwargs.pop(option,None )
        print('out loop',obj)
        if obj is not None:
            setattr(new_note,"%s_content_type"%option, ContentType.objects.get_for_model(obj))
            setattr(new_note,"%s_object_id"%option, obj.id)
    new_note.save()
    print(new_note)


notify.connect(new_notification)
