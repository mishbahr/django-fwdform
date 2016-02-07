#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from fwdform.helpers import get_next_url


class TestModelForms(TestCase):

    def setUp(self):
        self.referrer = 'http://example.com/contact-form/'
        self.absolute_url = 'http://example.com/thank-you/'
        self.relative_url = '/thank-you/'

    def test_get_next_url_with_absolute_url(self):
        next_url = get_next_url(referrer=self.referrer, next_url=self.absolute_url)
        self.assertEquals(next_url, self.absolute_url)

    def test_get_next_url_with_relative_url(self):
        next_url = get_next_url(referrer=self.referrer, next_url=self.relative_url)
        self.assertEquals(next_url, self.absolute_url)

    def test_get_next_url_with_relative_url_and_no_referrer(self):
        self.assertIsNone(get_next_url(referrer='', next_url=self.relative_url))

    def test_get_next_url_with_empty_url(self):
        self.assertIsNone(get_next_url(referrer=self.referrer, next_url=None))
