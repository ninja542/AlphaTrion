# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Community', '0022_auto_20170827_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityinst',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
