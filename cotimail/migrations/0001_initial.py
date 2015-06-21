# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('subject', models.TextField()),
                ('pickled_data', models.TextField()),
                ('name', models.CharField(max_length=250)),
                ('identifier', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('QUEUED', 'Queued'), ('SENT', 'Sent'), ('FAILED', 'Failed'), ('SAVED', 'Saved')], max_length=10)),
                ('recipients', models.TextField(help_text='A comma separated list of recipients')),
                ('sender', models.EmailField(max_length=250)),
                ('reply_to', models.EmailField(max_length=75, blank=True)),
                ('object_pk', models.TextField(blank=True, null=True, verbose_name='object ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_sent', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(null=True, blank=True, verbose_name='content type', related_name='content_type_set_for_emaillog', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name_plural': 'Email logs',
                'verbose_name': 'Email log',
            },
            bases=(models.Model,),
        ),
    ]
