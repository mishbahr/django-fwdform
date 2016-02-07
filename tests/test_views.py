#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-fwdform
------------

Tests for `django-fwdform` models module.
"""
import json

from django.conf.urls import include, url
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import Client, TestCase, override_settings

from fwdform.models import FwdForm, Site

try:
    from unittest import mock
except ImportError:
    import mock

urlpatterns = [
    url(r'^', include('fwdform.urls', namespace='fwdform')),
]


@override_settings(ROOT_URLCONF=__name__)
class TestFwdform(TestCase):

    def setUp(self):
        self.client = Client()
        self.site = Site.objects.create(
            pk=1,
            domain='example.com',
            akismet_key='123AkismetAPIKey'
        )
        self.fwdform = FwdForm.objects.create(
            pk=1,
            site=self.site,
            name='Contact Form 1',
            recipients='hello@example.com'
        )

        self.site_hashid = self.site.hashid
        self.contact_form_hashid = self.fwdform.hashid

        self.form_action_url = reverse('fwdform:forward_form', kwargs={
            'hashid': self.contact_form_hashid
        })

        self.form_data = {
            'name': 'John Smith',
            'email': 'john@example.com',
            'message': 'Hello from FwdForm test bot.'
        }

    def test_create_or_update_form_view_raises_404_for_bad_hashid(self):
        create_or_update_url = reverse('fwdform:create_or_update', kwargs={'hashid': 'xxxxx'})
        response = self.client.post(create_or_update_url)
        self.assertEquals(response.status_code, 404)

    def test_new_form_creation(self):
        data = {
            'name': 'Contact Form 2',
            'recipients': 'hello2@example.com',
        }
        create_url = reverse('fwdform:create_or_update', kwargs={
            'hashid': self.site_hashid})

        response = self.client.post(create_url, data=data)
        self.assertEquals(response.status_code, 201)

        response_data = json.loads(response.content)
        # hashid of the newly created form should be returned.
        self.assertTrue('hashid' in response_data)

    def test_new_form_creation_bad_data(self):
        create_url = reverse('fwdform:create_or_update', kwargs={
            'hashid': self.site_hashid})

        response = self.client.post(create_url, data={})
        # missing required data (name, recipients ). Should return 400 - Bad Request
        self.assertEquals(response.status_code, 400)

    def test_form_update(self):
        data = {
            'hashid': self.contact_form_hashid,
            'recipients': 'fwdform@example.com',
        }
        update_url = reverse('fwdform:create_or_update', kwargs={
            'hashid': self.site_hashid})

        response = self.client.post(update_url, data=data)
        self.assertEquals(response.status_code, 204)

    def test_attempt_to_update_form_not_belonging_to_site_raises_404(self):
        site2 = Site.objects.create(pk=2, domain='fwdform.com')
        update_url = reverse('fwdform:create_or_update', kwargs={
            'hashid': site2.hashid})

        data = {
            'hashid': self.contact_form_hashid,
            'recipients': 'middleman@example.com',
        }

        # contact form belongs to site 1 -  attempting to update it should return 404
        response = self.client.post(update_url, data=data)
        self.assertEquals(response.status_code, 404)

    @mock.patch('fwdform.akismet.Akismet.is_spam')
    def test_forward_form_view_sends_email(self, mock_akismet):
        mock_akismet.return_value = False
        response = self.client.post(self.form_action_url, data=self.form_data)

        self.assertEquals(len(mail.outbox), 1)
        thankyou_url = 'http://testserver{path}'.format(path=reverse('fwdform:thank_you'))
        self.assertRedirects(response, thankyou_url)

        fwdform = FwdForm.objects.get(pk=self.fwdform.pk)
        self.assertTrue(fwdform.sent_count, 1)

    @mock.patch('fwdform.akismet.Akismet.is_spam')
    def test_forward_form_view_returns_400_for_empty_submissions(self, mock_akismet):
        mock_akismet.return_value = False
        response = self.client.post(self.form_action_url, data={})
        self.assertEquals(response.status_code, 400)

    @mock.patch('fwdform.akismet.Akismet.is_spam')
    def test_forward_form_view_dont_send_spam_submission(self, mock_akismet):
        mock_akismet.return_value = True
        self.client.post(self.form_action_url, data=self.form_data)

        self.assertEquals(len(mail.outbox), 0)

        fwdform = FwdForm.objects.get(pk=self.fwdform.pk)
        self.assertEquals(fwdform.spam_count, 1)
        self.assertEquals(fwdform.sent_count, 0)

    @mock.patch('fwdform.akismet.Akismet.is_spam')
    def test_forward_form_view_returns_json_response(self, mock_akismet):
        mock_akismet.return_value = False
        response = self.client.post(
            self.form_action_url,
            data=self.form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(response['Content-Type'], 'application/json')
