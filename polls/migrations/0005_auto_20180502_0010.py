# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-01 21:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_practice_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice_question',
            name='author',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.UserProfile'),
        ),
    ]