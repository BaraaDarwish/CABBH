# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-14 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAC', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diabetesprediction',
            name='name',
            field=models.CharField(default='Untitled', max_length=50),
        ),
        migrations.AlterField(
            model_name='diabetesprediction',
            name='result',
            field=models.CharField(max_length=50),
        ),
    ]
