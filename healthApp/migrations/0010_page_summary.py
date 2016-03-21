# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0009_auto_20160320_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='summary',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
    ]
