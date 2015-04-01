# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotimail', '0005_emaillog_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='first_name',
            field=models.CharField(null=True, max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emaillog',
            name='last_name',
            field=models.CharField(null=True, max_length=3),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emaillog',
            name='title',
            field=models.CharField(null=True, max_length=3, choices=[('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Ms.')]),
            preserve_default=True,
        ),
    ]
