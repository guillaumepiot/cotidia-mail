# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotimail', '0003_auto_20150331_1402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emaillog',
            old_name='context',
            new_name='context_json',
        ),
    ]
