from __future__ import unicode_literals
import urllib2
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType



class MasterVideoQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
        
    def featured(self):
        return self.filter(featured=True)
    
   

class MasterVideoManager(models.Manager):
    def get_queryset(self):
        return MasterVideoQueryset(self.model, using=self._db)
    
    def get_featured(self):
        return self.get_queryset().active().featured()
 
 
   
class VideoQueryset(MasterVideoQueryset):
    def has_embed(self):
        return self.filter(embed_code__isnull=False).exclude(embed_code__exact="")
        
class VideoManager(MasterVideoManager):
    def get_queryset(self):
        return VideoQueryset(self.model, using=self._db)
        
    def all(self):
        return self.get_queryset().active().has_embed()
        


DEFAULT_MESSAGE = """
Check out this awesome video. 
"""

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=120)
    embed_code = models.CharField(max_length=500, null=True, blank=True)
    share_message = models.TextField(default=DEFAULT_MESSAGE)
    tags = GenericRelation("TaggedItem", null=True,blank=True)
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
    
    def get_share_message(self):
        full_url = "%s%s" %(settings.FULL_DOMAIN_NAME_LOCAL, self.get_absolute_url())
        print(full_url)
        # url_with_message = "%s%s" %( self.share_message(), full_url)
        return urllib2.quote("%s %s" %( self.share_message, full_url))


def video_signal_post_save_receiver(sender,instance,created, *args,**kwargs):
    print("signal sent")
    if created:
        slug_title = slugify(instance.title)
        new_slug = "%s %s %s"%(instance.title, instance.category.slug, instance.id)
        try: 
            obj_exists = Video.objects.get(slug=slug_title, category=instance.category)
            
            instance.slug = slugify(new_slug)
            instance.save()
            print("model exists, new slug generated")
        except Video.DoesNotExist:
            instance.slug = slug_title
            instance.save()
            print("slug and model created")
        except Video.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            insance.save()
            print("Multple models exists, new slug generated")
        except:
            pass

post_save.connect(video_signal_post_save_receiver,sender=Video)


# class CategoryQueryset(MasterVideoQueryset):
#     pass
        
class CategoryManager(MasterVideoManager):
    def get_queryset(self):
        return MasterVideoQueryset(self.model, using=self._db)
        
    def all(self):
        return self.get_queryset().active()

class Category(models.Model):
    title = models.CharField(max_length=120)
    # videos = models.ManyToManyField(Video, null=True, blank=True)
    tags = GenericRelation("TaggedItem", null=True,blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(default="abc",unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    objects = CategoryManager()
    def get_image_url(self):
        return "%s%s" % (settings.MEDIA_URL,self.image)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'cat_slug':self.slug})

   
TAG_CHOICES = (
        ("python","python"),
        ("django","django"),
        ("css","css"),
        ("bootsrap","bootstrap")
    )



class TaggedItem(models.Model):
    tag = models.SlugField(choices=TAG_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    def __unicode__(self):
        return self.tag
        
    def __str__(self):
        return self.tag
    ## TODO go back to https://www.codingforentrepreneurs.com/projects/srvup-membership/models-videos-app/?play=true
    ## 7:05
