# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-27 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20180927_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice_question',
            name='level',
            field=models.CharField(choices=[('kolay', 'KOLAY'), ('orta', 'ORTA'), ('zor', 'ZOR'), ('çok zor', 'ÇOK ZOR')], default='kolay', max_length=10),
        ),
    ]
