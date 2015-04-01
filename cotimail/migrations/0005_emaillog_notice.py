# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotimail', '0004_auto_20150331_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='notice',
            field=models.CharField(null=True, max_length=250),
            preserve_default=True,
        ),
    ]
