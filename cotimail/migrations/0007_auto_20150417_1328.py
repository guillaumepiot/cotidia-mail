# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotimail', '0006_auto_20150331_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='title',
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='reply_to',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
