# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-10 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app01', '0004_auto_20180110_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='r',
            field=models.ManyToManyField(to='app01.Host'),
        ),
    ]
