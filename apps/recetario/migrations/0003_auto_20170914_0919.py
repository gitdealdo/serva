# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-14 14:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recetario', '0002_auto_20170911_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receta',
            name='publicar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receta',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
