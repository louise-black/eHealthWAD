# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('healthApp', '0010_page_summary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='slug',
            new_name='slugCat',
        ),
        migrations.RemoveField(
            model_name='page',
            name='summary',
        ),
        migrations.AddField(
            model_name='category',
            name='pubOrPriv',
            field=models.CharField(default=b'PRIV', max_length=4, choices=[(b'PUB', b'public'), (b'PRIV', b'private')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='slugUser',
            field=models.SlugField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
