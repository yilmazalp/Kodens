# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-22 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='slug',
            field=models.SlugField(default='', max_length=40, unique=True),
        ),
    ]
