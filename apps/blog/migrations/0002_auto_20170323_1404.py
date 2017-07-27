# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-23 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='title',
            new_name='tittle',
        ),
        migrations.AddField(
            model_name='post',
            name='state',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
