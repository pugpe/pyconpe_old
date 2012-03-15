# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('landpage.views',
    url(r'^$', 'home', name='home'),
)
