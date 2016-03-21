# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0013_userprofile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='pubOrPriv',
            field=models.CharField(default=b'PRIV', max_length=4, choices=[(b'PUB', b'public'), (b'PRIV', b'private')]),
            preserve_default=True,
        ),
    ]
