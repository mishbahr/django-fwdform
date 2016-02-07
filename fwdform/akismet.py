# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import six
from django.utils.version import get_version as django_get_version
from requests.api import request
from requests.exceptions import RequestException

from . import __version__ as fwdform_version
from .exceptions import AkismetError


class Akismet(object):
    api_key = ''
    site_url = ''
    api_url = 'rest.akismet.com'
    version = '1.1'
    # http://blog.akismet.com/2012/06/19/pro-tip-tell-us-your-comment_type/
    comment_type = 'contact-form'
    debug = False

    def __init__(self, *args, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

        self.debug = True

    def get_api_url(self):
        return 'https://{api_key}.{api_url}/{version}'.format(
            api_key=self.api_key,
            api_url=self.api_url,
            version=self.version,
        )

    def get_akismet_ua(self):
        return 'Django/{django_version} | Fwdform/{fwdform_version}'.format(
            django_version=django_get_version(),
            fwdform_version=fwdform_version
        )

    def request(self, url,  method='post', **kwargs):
        headers = {'User-Agent': self.get_akismet_ua()}
        return request(method, url, headers=headers, **kwargs)

    def verify_key(self):
        endpoint = '{base_url}/verify-key'.format(base_url=self.get_api_url())
        payload = {
            'key': self.api_key,
            'blog': self.site_url
        }

        try:
            response = self.request(endpoint, data=payload)
            response.raise_for_status()
        except RequestException as e:  # pragma: no cover
            raise AkismetError(str(e))
        else:
            bool_dict = {
                'valid': True,
                'invalid': False,
            }
            try:
                return bool_dict[response.text.lower()]
            except KeyError:  # pragma: no cover
                raise AkismetError(response.text)

    def is_spam(self, http_request):
        meta = http_request.META
        data = http_request.POST

        payload = {
            'blog': self.site_url,
            'user_ip': meta.get('REMOTE_ADDR', ''),
            'user_agent': meta.get('HTTP_USER_AGENT', ''),
            'referrer': meta.get('HTTP_REFERER', ''),
            'permalink': data.get('permalink', ''),
            'comment_type': self.comment_type,
            'comment_author': data.get('name', ''),
            'comment_author_email': data.get('email', ''),
            'comment_author_url': data.get('url', ''),
            'comment_content': data.get('message', ''),
            'is_test': self.debug,
        }

        if self.debug:
            payload['user_role'] = 'administrator'

        endpoint = '{base_url}/comment-check'.format(base_url=self.get_api_url())

        try:
            response = self.request(endpoint, data=payload)
            response.raise_for_status()
        except RequestException as e:  # pragma: no cover
            raise AkismetError(str(e))
        else:
            bool_dict = {
                'true': True,
                'false': False,
            }
            try:
                return bool_dict[response.text.lower()]
            except KeyError:  # pragma: no cover
                raise AkismetError(response.text)
