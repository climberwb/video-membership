from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
from .models import Video, Category,TaggedItem



class TaggedItemInline(GenericTabularInline):
    model = TaggedItem


class VideoAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["__unicode__","slug"]
    fields=['title','embed_code','slug',"category",
    "active",
    "featured",
    "free_preview"]
    
    # prepopulated_fields = {
    #                         "embed_code":["title"]}
    class Meta:
        model = Video
        
class CategoryAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    class Meta:
        model=Category

admin.site.register(Video,VideoAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(TaggedItem)