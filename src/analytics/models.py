from __future__ import unicode_literals

from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db import models

from videos.models import Video, Category
from .signals import page_view
    

## Query Managers
class PageViewQueryset(models.query.QuerySet):
    def videos(self):
        content_type = ContentType.objects.get_for_model(Video)
        return self.filter(primary_content_type=content_type)
        
    def categories(self):
        content_type = ContentType.objects.get_for_model(Category)
        return self.filter(primary_content_type=content_type)        
        
class PageViewManager(models.Manager):
    def get_queryset(self):
        return PageViewQueryset(self.model, using=self._db)
    
    def get_videos(self):
        return self.get_queryset().videos()
        
    def get_categories(self):
        return self.get_queryset().categories
        
  
        



# Create your models here.

class PageView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    path = models.CharField(max_length=350)
    count = models.PositiveIntegerField(default=1)
    
    timestamp = models.DateTimeField(default=timezone.now())
    
    primary_content_type = models.ForeignKey(ContentType, related_name='primary_obj', null=True, blank=True)
    primary_object_id = models.PositiveIntegerField(null=True, blank=True)
    primary_object = GenericForeignKey("primary_content_type","primary_object_id")
    
    secondary_content_type = models.ForeignKey(ContentType, related_name='secondary_obj', null=True, blank=True)
    secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
    secondary_object = GenericForeignKey("secondary_content_type","secondary_object_id")
    
    objects = PageViewManager()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __unicode__(self):
        return self.path

def page_view_received(sender, **kwargs):
    page_path = kwargs.pop('page_path')
    signal = kwargs.pop('signal',None)
    primary_obj = kwargs.pop('primary_obj',None)
    secondary_obj = kwargs.pop('secondary_obj',None)
    
    user=sender
    if( not user.is_authenticated()):
        new_page_view, created = PageView.objects.get_or_create(path=page_path,timestamp=timezone.now())
    else:
        new_page_view, created = PageView.objects.get_or_create(path=page_path,user=user,timestamp=timezone.now())
    if not created:
        new_page_view.count +=1
    if primary_obj:
        new_page_view.primary_object_id = primary_obj.id
        new_page_view.primary_content_type = ContentType.objects.get_for_model(primary_obj)
    if secondary_obj:
        new_page_view.secondary_object_id = secondary_obj.id
        new_page_view.secondary_content_type = ContentType.objects.get_for_model(secondary_obj)
    
    
    new_page_view.save()
    
   
page_view.connect(page_view_received)    
    
    
    