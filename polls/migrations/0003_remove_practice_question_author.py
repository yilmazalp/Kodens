# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-01 19:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_challenge_deneme_hacker_job_practice_practice_area_practice_question_practice_question_input_tutoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice_question',
            name='author',
        ),
    ]
