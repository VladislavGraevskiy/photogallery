from django.conf.urls import url, include
from django.contrib import admin

import loginer.views

urlpatterns = [

    url(r'^registration/$', loginer.views.registration),
    url(r'^out/$', loginer.views.logout),
    url(r'^', loginer.views.login),

]
