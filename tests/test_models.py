#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from fwdform.models import Site, FwdForm


class TestFwdformModels(TestCase):

    def setUp(self):
        self.site = Site.objects.create(pk=1, domain='example.com')
        self.form = FwdForm.objects.create(
            pk=1,
            site=self.site,
            name='Contact Form',
            recipients='hello@example.com, contact@example.com'
        )

        self.site_hashid = self.site.hashid
        self.contact_form_hashid = self.form.hashid

    def test_get_by_hashid(self):
        self.assertEquals(Site.objects.get_by_hashid(hashid=self.site_hashid), self.site)

        contact_form = FwdForm.objects.get_by_hashid(hashid=self.contact_form_hashid)
        self.assertEquals(contact_form, self.form)

    def test_get_recipients_helper(self):
        self.assertEqual(len(self.form.get_recipients()), 2)
