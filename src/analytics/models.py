from __future__ import unicode_literals

from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db import models
from .signals import page_view

# Create your models here.

class PageView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    path = models.CharField(max_length=350)
    count = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now())
    
    
    
    def __unicode__(self):
        return self.path

def page_view_received(sender,page_path, *args,**kwargs):
    user=sender
    if( not user.is_authenticated()):
        new_page_view, created = PageView.objects.get_or_create(path=page_path,timestamp=timezone.now())
    else:
        new_page_view, created = PageView.objects.get_or_create(path=page_path,user=user,timestamp=timezone.now())
    if not created:
        new_page_view.count +=1
    new_page_view.save()
    
   
page_view.connect(page_view_received)    
    
    
    