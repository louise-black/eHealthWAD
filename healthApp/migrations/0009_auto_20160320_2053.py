# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0008_page_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='user',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name=b'profile', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
