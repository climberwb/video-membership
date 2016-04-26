from django.contrib import admin

# Register your models here.
from .models import Video, Category

class VideoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__","slug"]
    fields=['title','embed_code',"slug",
    "active",
    "featured",
    "free_preview"]
    
    prepopulated_fields = {"slug":["title"],
                            "embed_code":["title"]}
    class Meta:
        model = Video
        
    

admin.site.register(Video,VideoAdmin)
admin.site.register(Category)