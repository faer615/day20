# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-09 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='code',
            field=models.CharField(default='SA', max_length=32, null=True),
        ),
    ]