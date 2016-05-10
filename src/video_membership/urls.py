"""video_membership URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin

urlpatterns = patterns('',
        url(r'^$','video_membership.views.home', name='home'),
        url(r'^admin/', admin.site.urls),
        url(r'^videos/$', 'videos.views.category_list',name='category_list'),
        url(r'^videos/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail',name='category_detail'),
        url(r'^videos/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail',name='video_detail'),
        
)

urlpatterns +=patterns('accounts.views',
    url(r'^accounts/login/$', 'auth_login', name='login'),
    url(r'^accounts/logout/$', 'auth_logout', name='logout'),
)

#Comment Thread
urlpatterns +=patterns('comments.views',
    url(r'^comments/(?P<id>\d+)$','comment_thread', name='comment_thread'),
    url(r'^comments/create/$','comment_create', name='comment_create')
)

#Notifications Thread
urlpatterns +=patterns('notifications.views',
    url(r'^notifications/$','all', name='notifications_all'),
    url(r'^notifications/unread/$','all', name='notifications_all'),
    url(r'^notifications/read/$','all', name='notifications_all'),
)
