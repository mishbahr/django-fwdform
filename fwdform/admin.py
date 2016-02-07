# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from .forms import SiteForm
from .models import FwdForm, Site


class SiteAdmin(admin.ModelAdmin):
    form = SiteForm
    list_display = ('domain', 'hashid', )
    readonly_fields = ('hashid', 'created_at', 'updated_at', )


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'hashid', 'sent_count', 'spam_count', )
    readonly_fields = ('hashid', 'sent_count', 'spam_count',  'created_at', 'updated_at', )
    list_filter = ('site', )


admin.site.register(Site, SiteAdmin)
admin.site.register(FwdForm, ContactFormAdmin)
