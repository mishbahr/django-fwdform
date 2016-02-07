# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from hashids import Hashids

from .conf import settings


class HashidsManager(models.Manager):

    def get_by_hashid(self, hashid):
        hashids = Hashids(self.model.get_salt(), min_length=40)
        try:
            pk = hashids.decode(hashid)[0]
        except IndexError:  # pragma: no cover
            pk = None

        return self.get(pk=pk)


class HashidsModel(models.Model):

    objects = HashidsManager()

    class Meta:
        abstract = True

    @classmethod
    def get_salt(cls):
        return '{app_label}.{modelname}.{secret}'.format(
            app_label=cls._meta.app_label,
            modelname=cls._meta.object_name.lower(),
            secret=settings.FWDFORM_HASHIDS_SALT
        )

    @property
    def hashid(self):
        if not self.pk:  # pragma: no cover
            return None

        hashids = Hashids(self.get_salt(), min_length=40)
        return hashids.encode(self.pk)


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Site(HashidsModel, TimeStampedModel):

    domain = models.URLField(_('Site URL'), max_length=100, unique=True)
    is_active = models.BooleanField(_('Is Active?'), default=True)
    akismet_key = models.CharField(_('Akismet API key'), max_length=40, blank=True)

    def __str__(self):
        return self.domain


@python_2_unicode_compatible
class FwdForm(HashidsModel, TimeStampedModel):

    site = models.ForeignKey(Site, related_name='contact_forms')
    name = models.CharField(_('Name'), max_length=100)
    recipients = models.CharField(
        _('Recipients'), max_length=255, help_text=_('Separate several addresses with a comma.'))
    thankyou_url = models.URLField(_('Thank You URL'), blank=True)
    sent_count = models.PositiveIntegerField(_('Total Submissions'), default=0)
    spam_count = models.PositiveIntegerField(_('Spam Count'), default=0)

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def __str__(self):
        return self.name

    def get_recipients(self):
        return [email.strip() for email in re.compile('\s*[,;]+\s*').split(self.recipients)]
