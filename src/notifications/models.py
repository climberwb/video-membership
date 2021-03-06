from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from .signals import notify
# Create your models here.


class NotificationQuerySet(models.query.QuerySet):
    def get_user(self,user):
        return self.filter(recipient=user)
    
    def mark_targetless(self,recipient):
        qs = self.unread().get_user(recipient)
        qs_no_target = qs.filter(target_object_id = None)
        if qs_no_target:
            qs_no_target.update(read=True)
    
    def mark_all_read(self,recipient):
        qs = self.unread().get_user(recipient)
        qs.update(read=True)
        
    def mark_all_unread(self,recipient):
        qs = self.read().get_user(recipient)
        qs.update(read=False)
    
    def unread(self):
        return self.filter(read=False)
        
    def read(self):
        return self.filter(read=True)
    
    def recent(self):
        return self.unread()[:5]

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)
        
    def all_unread(self,user):   
        return self.get_queryset().get_user(user).unread()
    
    def all_read(self,user):   
        return self.get_queryset().get_user(user).read()
    
    def all_for_user(self, user):
        self.get_queryset().mark_targetless(user)
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

    
    objects = NotificationManager()
    @property
    def get_link(self):
        try:
            target_url = self.target_content_object.get_absolute_url()
        except:
            target_url = reverse("notifications_all")
        context = {
            "sender": self.sender_object,
            "verb": self.verb,
            "action":self.action_object,
            "target": self.target_content_object,
            "target_url": target_url,
            "verify_read":reverse("notifications_read",kwargs={"id":self.id})
        }
        if self.target_content_object:
            return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s  %(target)s with %(action)s </a> "%context
        else:
            return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s</a> "%context
            
            
    def __unicode__(self):
        try:
            target_url = self.target_content_object.get_absolute_url()
        except:
            target_url = reverse("notifications_all")
        print("inside unicode", self.id)
        context = {
            "sender": self.sender_object,
            "verb": self.verb,
            "action":self.action_object,
            "target": self.target_content_object,
            "target_url": target_url,
            "verify_read":reverse("notifications_read",kwargs={"id":self.id})
        }
        if self.target_content_object:
            return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s  %(target)s with %(action)s </a> "%context
        else:
            return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s</a> "%context
            
            
        
        
def new_notification(sender,**kwargs):
    # if(recipient is None):
    #     recipient = 0
    # else:
    #     new_notification_create = Notification.objects.create(recipient=recipient,action=action,)
   
    kwargs.pop('signal',None)
    recipient = kwargs.pop("recipient")
    verb = kwargs.pop("verb")
    try:
        affected_users = kwargs.pop('affected_users')
    except:
        affected_users = None
    if affected_users is not None:
        for u in affected_users:
            print("affected_users: ",affected_users, u==sender)
            if u == sender:
                pass
            else:
                print("u: ", u)
                print("sender",sender == u,sender.id)
                new_note = Notification(
                        recipient=u,
                        verb = verb,
                        sender_content_type = ContentType.objects.get_for_model(sender),
                        sender_object_id = sender.id
                    )
                print("before option loop")
                # print("before option looop", new_note)
                print("kwargs ", kwargs)
                for option in ("target","action"):
                    # obj = kwargs.pop(option,None )
                    try:
                        obj = kwargs[option] 
                    except:
                        obj = None
                    if obj is not None:
                        setattr(new_note,"%s_content_type"%option, ContentType.objects.get_for_model(obj))
                        setattr(new_note,"%s_object_id"%option, obj.id)
                print("before new note")
                # print(new_note)
                print("passed new_)note")
                new_note.save()
                
    else:
        print("affected_users is none")
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
