#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase, RequestFactory

from fwdform.akismet import Akismet


class TestAsikmet(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.akismet = Akismet(
            api_key=settings.AKISMET_API_KEY,
            site_url='https://akismet.com/',
            debug=True)

    def test_ham_submission(self):
        data = {
            'name': 'John Smith',
            'email': 'fwdform@akismet.com',
            'message': 'Hello Akismet! Nice to meet you!',
        }
        request = self.factory.post(path='/contact-form/', data=data)
        self.assertFalse(self.akismet.is_spam(request))

    def test_spam_submission(self):
        data = {
            'name': 'viagra-test-123',
        }
        request = self.factory.post(path='/contact-form/', data=data)
        self.assertTrue(self.akismet.is_spam(request))

    def test_verify_key_with_valid_key(self):
        self.assertTrue(self.akismet.verify_key())

    def test_verify_key_with_invalid_key(self):
        akismet = Akismet(
            api_key='xxx',
            site_url='https://akismet.com/',
            debug=True)
        self.assertFalse(akismet.verify_key())
