# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-29 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170729_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_from',
            field=models.IntegerField(blank=True),
        ),
    ]
