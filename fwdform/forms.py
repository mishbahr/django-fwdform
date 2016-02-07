# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .akismet import Akismet
from .models import FwdForm, Site


class FwdFormModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        super(FwdFormModelForm, self).__init__(*args, **kwargs)
        if partial:
            for name in list(self.fields):
                if name not in self.data:
                    del self.fields[name]

    class Meta:
        model = FwdForm
        fields = ('site', 'name', 'recipients', 'thankyou_url', )


class SiteForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(SiteForm, self).clean()
        site_url = cleaned_data.get('domain')
        akismet_key = cleaned_data.get('akismet_key')

        if site_url and akismet_key:
            akismet = Akismet(api_key=akismet_key, site_url=site_url)
            if not akismet.verify_key():
                msg = _('Invalid API Key for Akismet')
                self.add_error('akismet_key', msg)

    class Meta:
        model = Site
        fields = '__all__'
