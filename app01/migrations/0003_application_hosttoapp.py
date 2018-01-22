# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-10 08:23
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app01', '0002_business_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='HostToApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aobj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Application')),
                ('hobj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Host')),
            ],
        ),
    ]
