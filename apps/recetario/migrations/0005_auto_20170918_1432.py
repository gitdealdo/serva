# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-18 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetario', '0004_auto_20170914_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='recetas', verbose_name='Imágen'),
        ),
        migrations.AlterField(
            model_name='receta',
            name='preparacion',
            field=models.TextField(blank=True, null=True, verbose_name='Preparación'),
        ),
    ]