from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse


class VideoQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
        
    def featured(self):
        return self.filter(featured=True)
        
class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQueryset(self.model, using=self._db)
    
    def get_featured(self):
        return self.get_queryset().active().featured()
        
    def all(self):
        return self.get_queryset().active()

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=120)
    embed_code = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    free_preview = models.BooleanField(default=False)
    category = models.ForeignKey("Category", default=1)
    slug = models.SlugField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    
    objects = VideoManager()
    
    class Meta:
        unique_together=('slug','category')
        
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'cat_slug':self.category.slug,'vid_slug':self.slug})

class Category(models.Model):
    title = models.CharField(max_length=120)
    # videos = models.ManyToManyField(Video, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to="/images", null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(default="abc",unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'cat_slug':self.slug})

   
        
        
    ## TODO go back to https://www.codingforentrepreneurs.com/projects/srvup-membership/models-videos-app/?play=true
    ## 7:05
