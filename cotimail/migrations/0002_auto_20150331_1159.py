# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotimail', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailDraft',
        ),
        migrations.AddField(
            model_name='emaillog',
            name='lastname',
            field=models.CharField(max_length=250, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emaillog',
            name='title',
            field=models.CharField(max_length=3, choices=[('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Ms.')], null=True),
            preserve_default=True,
        ),
    ]
