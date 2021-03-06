# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-18 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0006_person_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.CharField(default='default', max_length=20),
        ),
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(default='persons/user.png', upload_to='persons'),
        ),
    ]
