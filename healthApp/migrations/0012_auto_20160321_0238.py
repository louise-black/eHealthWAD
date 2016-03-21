# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0011_userprofile_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='slug',
            new_name='slugCat',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='slugUser',
            field=models.SlugField(default=b''),
            preserve_default=True,
        ),
    ]
