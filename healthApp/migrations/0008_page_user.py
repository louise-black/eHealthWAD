# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('healthApp', '0007_auto_20160319_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='user',
            field=models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
