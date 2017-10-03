# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 19:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Project', '0002_senateprojects'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerInt',
            fields=[
                ('surveyquestions_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Project.SurveyQuestions')),
                ('answer', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('Project.surveyquestions',),
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('surveyquestions_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Project.SurveyQuestions')),
                ('answer', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('Project.surveyquestions',),
        ),
        migrations.AddField(
            model_name='questions',
            name='question_type',
            field=models.CharField(choices=[('TEXT', 'text'), ('INTEGER', 'integer')], default='INTEGER', max_length=200),
        ),
        migrations.AddField(
            model_name='questions',
            name='required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='senateprojects',
            name='description',
            field=models.TextField(default='insert description here!'),
        ),
        migrations.AddField(
            model_name='senateprojects',
            name='image',
            field=s3direct.fields.S3DirectField(null=True),
        ),
        migrations.AddField(
            model_name='senateprojects',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Project.CustomSurvey'),
        ),
        migrations.AddField(
            model_name='senateprojects',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='surveyquestions',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Project.CustomSurvey'),
        ),
    ]