# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0002_auto_20160316_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='forename',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, default=b'', max_length=254),
        ),
    ]
