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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.TextField()),
                ('pickled_data', models.TextField()),
                ('notice', models.CharField(max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
                ('identifier', models.CharField(max_length=250)),
                ('status', models.CharField(max_length=10, choices=[(b'QUEUED', b'Queued'), (b'SENT', b'Sent'), (b'FAILED', b'Failed'), (b'SAVED', b'Saved')])),
                ('context_json', models.TextField(null=True)),
                ('recipients', models.TextField(help_text=b'A comma separated list of recipients')),
                ('sender', models.EmailField(max_length=250)),
                ('reply_to', models.EmailField(max_length=254, blank=True)),
                ('object_pk', models.TextField(null=True, verbose_name='object ID', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_sent', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_emaillog', verbose_name='content type', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Email log',
                'verbose_name_plural': 'Email logs',
            },
        ),
    ]
