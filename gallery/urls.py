"""untitled1 URL Configuration

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
from django.conf.urls import url

from gallery.utils import gallery_utils
from  gallery.servises import database_servise
import gallery.view_old
import gallery.views
import loginer.views


urlpatterns = [
    url(r'^addpicture/$', gallery.views.add_picture),
    url(r'^remove_picture/(?P<picture_id>\d+)/$', database_servise.delete_picture),
    url(r'^resize_picture/(?P<picture_id>\d+)/$', gallery.views.picture2),
    url(r'^approve_the_picture/(?P<picture_id>\d+)/$', database_servise.admin_to_approve_the_picture),
    url(r'^add/$', gallery.views.add_picture),
    url(r'^picture/(?P<picture_id>\d+)/$', gallery.views.picture2),
    url(r'^addlike/(?P<picture_id>\d+)/(?P<user_id>\d+)/$', database_servise.add_like),
    url(r'^removelike/(?P<picture_id>\d+)/(?P<user_id>\d+)/$', database_servise.remove_like),
    url(r'^addcomment/(?P<picture_id>\d+)/(?P<user_id>\d+)/$', database_servise.add_comment),
    url(r'^profile/(?P<user_id>\d+)/$', gallery.views.profile),
    url(r'^edit_profile/(?P<user_id>\d+)/$', gallery.views.edit_profile),
    url(r'^', gallery.views.pictures),
]