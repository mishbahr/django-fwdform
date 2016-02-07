# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-07 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FwdForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('recipients', models.CharField(help_text='Separate several addresses with a comma.', max_length=255, verbose_name='Recipients')),
                ('thankyou_url', models.URLField(blank=True, verbose_name='Thank You URL')),
                ('sent_count', models.PositiveIntegerField(default=0, verbose_name='Total Submissions')),
                ('spam_count', models.PositiveIntegerField(default=0, verbose_name='Spam Count')),
            ],
            options={
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('domain', models.URLField(max_length=100, unique=True, verbose_name='Site URL')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
                ('akismet_key', models.CharField(blank=True, max_length=40, verbose_name='Akismet API key')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='fwdform',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_forms', to='fwdform.Site'),
        ),
    ]
