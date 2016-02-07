#!/usr/bin/env python
# -*- coding: utf-8 -*-

import responses

from django.test import TestCase

from fwdform.forms import SiteForm


class TestModelForms(TestCase):

    @responses.activate
    def test_custom_clean_method(self):
        url = 'https://xxxxxx.rest.akismet.com/1.1/verify-key'
        responses.add(responses.POST, url, body='invalid', status=200)

        form_data = {
            'domain': 'http://example.com',
            'akismet_key': 'xxxxxx',
        }

        form = SiteForm(data=form_data)
        self.assertFalse(form.is_valid())
