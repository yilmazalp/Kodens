# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-22 14:53
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge_name', models.CharField(max_length=250)),
                ('challenge_id', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=20)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Deneme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deneme_isim', models.CharField(max_length=250)),
                ('deneme_id', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hacker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('school', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='', max_length=250, verbose_name='firma ismi')),
                ('job_name', models.TextField(default='', max_length=100, verbose_name='iş ismi')),
                ('job_description', ckeditor.fields.RichTextField(default='', max_length=750, verbose_name='iş tanımı')),
            ],
        ),
        migrations.CreateModel(
            name='practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('practice_name', models.CharField(max_length=250)),
                ('practice_id', models.CharField(max_length=250)),
                ('practice_logo', models.CharField(default='', max_length=250)),
                ('slug', models.SlugField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='practice_area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.CharField(max_length=250)),
                ('area_name', models.CharField(max_length=250)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.practice')),
            ],
        ),
        migrations.CreateModel(
            name='practice_question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_area_id', models.CharField(default='1', max_length=5, null=True)),
                ('question_area_name', models.CharField(default='', max_length=100, verbose_name='soru adı')),
                ('question_area_text', ckeditor.fields.RichTextField(default='', max_length=750, verbose_name='soru')),
                ('question_input_text', models.TextField(default='', max_length=150, verbose_name='girdi formatı')),
                ('question_answer_text', models.TextField(default='', max_length=150, verbose_name='çıktı formatı')),
                ('question_language_field', multiselectfield.db.fields.MultiSelectField(choices=[('c', 'C'), ('c++', 'C++'), ('c#', 'C#'), ('python', 'Python'), ('java', 'Java')], default='', max_length=20, verbose_name='kullanılacak diller')),
            ],
        ),
        migrations.CreateModel(
            name='practice_question_input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_id', models.CharField(default='', max_length=5)),
                ('input_text', models.TextField(default='', max_length=150)),
                ('output_text', models.TextField(default='', max_length=150)),
                ('input_belong_practice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.practice_question')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='SolvedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved_question_id', models.CharField(default='', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutorial_name', models.CharField(max_length=250)),
                ('tutorial_id', models.CharField(max_length=250)),
                ('tutorial_logo', models.CharField(default='', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='tutorial_language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.CharField(max_length=250)),
                ('language_name', models.CharField(max_length=250)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.tutorial')),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial_Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_area_name', models.CharField(default='', max_length=100)),
                ('lecture_area_text', ckeditor.fields.RichTextField(default='', max_length=7500)),
                ('lecture_area_input', models.TextField(default='', max_length=150)),
                ('lecture_area_output', models.TextField(default='', max_length=150)),
                ('lecture_discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.tutorial')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('school', models.CharField(default='', max_length=100)),
                ('point', models.FloatField(default=0)),
                ('website', models.URLField(default='')),
                ('phone', models.IntegerField(default=0)),
                ('face', models.FileField(default='', upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='solvedquestion',
            name='solved_by_user',
            field=models.ManyToManyField(to='polls.UserProfile'),
        ),
        migrations.AddField(
            model_name='solvedquestion',
            name='solved_question_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.practice_question'),
        ),
        migrations.AddField(
            model_name='practice_question',
            name='author',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.UserProfile'),
        ),
        migrations.AddField(
            model_name='practice_question',
            name='practice_discipline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.practice_area', verbose_name='konu adı'),
        ),
        migrations.AddField(
            model_name='practice_question',
            name='solved_by_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friend',
            name='current_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='polls.UserProfile'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_user',
            field=models.ManyToManyField(to='polls.UserProfile'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question'),
        ),
    ]
