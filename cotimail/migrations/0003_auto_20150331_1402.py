# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotimail', '0002_auto_20150331_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='title',
        ),
        migrations.AddField(
            model_name='emaillog',
            name='context',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
