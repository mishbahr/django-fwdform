# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa

from appconf import AppConf


class FwdFormConf(AppConf):
    HASHIDS_SALT = settings.SECRET_KEY

    class Meta:
        prefix = 'fwdform'
