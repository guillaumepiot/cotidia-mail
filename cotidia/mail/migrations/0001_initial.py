# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField()),
                ('pickled_data', models.TextField()),
                ('notice', models.CharField(null=True, max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('identifier', models.CharField(max_length=250)),
                ('status', models.CharField(max_length=10, choices=[('QUEUED', 'Queued'), ('SENT', 'Sent'), ('FAILED', 'Failed'), ('SAVED', 'Saved')])),
                ('context_json', models.TextField(null=True)),
                ('recipients', models.TextField(help_text='A comma separated list of recipients')),
                ('sender', models.EmailField(max_length=250)),
                ('reply_to', models.EmailField(blank=True, max_length=254)),
                ('object_pk', models.TextField(null=True, blank=True, verbose_name='object ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_sent', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', verbose_name='content type', null=True, blank=True, related_name='content_type_set_for_emaillog', on_delete=models.SET_NULL)),
            ],
            options={
                'verbose_name_plural': 'Email logs',
                'ordering': ('-date_created',),
                'verbose_name': 'Email log',
            },
        ),
    ]
