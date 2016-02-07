# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import create_or_update_form, forward_form, thank_you

urlpatterns = [
    url(r'^(?P<hashid>\w+)/$', create_or_update_form, name='create_or_update'),
    url(r'^send/(?P<hashid>\w+)/$', forward_form, name='forward_form'),
    url(r'^thank-you/$', thank_you, name='thank_you'),
]
