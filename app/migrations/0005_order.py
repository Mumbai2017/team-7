# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-29 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170729_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_by', models.IntegerField()),
                ('placed_from', models.IntegerField()),
                ('nachni', models.IntegerField(default=0)),
                ('mari', models.IntegerField(default=0)),
                ('oat', models.IntegerField(default=0)),
            ],
        ),
    ]
