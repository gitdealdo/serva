# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_auto_20170418_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='persona',
            new_name='person',
        ),
    ]
