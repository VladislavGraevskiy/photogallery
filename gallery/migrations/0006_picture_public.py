# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_picture_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='public',
            field=models.IntegerField(default=1),
        ),
    ]
