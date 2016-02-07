#!/usr/bin/env python
# -*- coding: utf-8 -*-

import responses

from django.conf import settings
from django.test import RequestFactory, TestCase

from fwdform.akismet import Akismet


class TestAsikmet(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.akismet = Akismet(
            api_key=settings.AKISMET_API_KEY,
            site_url='akismet.com',
            debug=True)

    @responses.activate
    def test_ham_submission(self):
        url = '{base_url}/comment-check'.format(base_url=self.akismet.get_api_url())
        responses.add(responses.POST, url, body='false', status=200)

        data = {
            'name': 'John Smith',
            'email': 'fwdform@akismet.com',
            'message': 'Hello Akismet! Nice to meet you!',
        }
        request = self.factory.post(path='/contact-form/', data=data)
        self.assertFalse(self.akismet.is_spam(request))

    @responses.activate
    def test_spam_submission(self):
        url = '{base_url}/comment-check'.format(base_url=self.akismet.get_api_url())
        responses.add(responses.POST, url, body='true', status=200)

        data = {
            'name': 'viagra-test-123',
        }
        request = self.factory.post(path='/contact-form/', data=data)
        self.assertTrue(self.akismet.is_spam(request))

    @responses.activate
    def test_verify_key_with_valid_key(self):
        url = '{base_url}/verify-key'.format(base_url=self.akismet.get_api_url())
        responses.add(responses.POST, url, body='valid', status=200)

        self.assertTrue(self.akismet.verify_key())

    @responses.activate
    def test_verify_key_with_invalid_key(self):
        akismet = Akismet(
            api_key='xxx',
            site_url='https://akismet.com/',
            debug=True)

        url = '{base_url}/verify-key'.format(base_url=akismet.get_api_url())
        responses.add(responses.POST, url, body='invalid', status=200)
        self.assertFalse(akismet.verify_key())
