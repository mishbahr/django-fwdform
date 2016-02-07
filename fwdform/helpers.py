# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.core.mail import send_mail as django_send_mail
from django.db.models import F
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from .exceptions import EmptyFormError, FwdFormError

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # pragma: no cover
    # Python 2.X
    from urlparse import urlparse, urlunparse

try:
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from django.utils.datastructures import SortedDict as OrderedDict


logger = logging.getLogger('fwdform')


def get_next_url(referrer='', next_url=''):
    if not next_url:
        return None

    # check if next_url is an absolute url
    if urlparse(next_url).netloc:
        return next_url

    if next_url and referrer:
        parsed = list(urlparse(referrer))  # results in [scheme, netloc, path, ...]
        parsed[2] = next_url
        return urlunparse(parsed)


def send_mail(request, instance):
    reserved_fields = ('_gotcha', '_next', '_subject')

    referrer = request.META.get('HTTP_REFERER', '')
    subject = request.POST.get(
        '_subject', _('New submission from {referrer}').format(referrer=referrer))
    from_email = request.POST.get('email', None)
    recipients = instance.get_recipients()

    form_data = OrderedDict()
    for field, value in six.iteritems(request.POST):
        if field not in reserved_fields:
            form_data[field] = value

    # prevent submitting empty form
    if not any(form_data.values()):
        raise EmptyFormError()

    context = {
        'form_data': form_data,
        'instance': instance,
        'referrer': referrer,
    }

    message = render_to_string('fwdform/submission.txt', context)

    try:
        django_send_mail(subject, message, from_email, recipients, fail_silently=False)
    except Exception as e:  # pragma: no cover
        logger.error(str(e))
        message = _('Oops! An error occurred and your message could not be sent.')
        raise FwdFormError(message)

    instance.sent_count = F('sent_count') + 1
    instance.save()
