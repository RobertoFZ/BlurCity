# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-11 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Routes', '0003_route_create_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='create_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]