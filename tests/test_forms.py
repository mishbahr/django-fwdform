#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from fwdform.forms import SiteForm


class TestModelForms(TestCase):

    def test_custom_clean_method(self):
        form_data = {
            'domain': 'http://example.com',
            'akismet_key': 'xxxxxx',
        }

        form = SiteForm(data=form_data)
        self.assertFalse(form.is_valid())
