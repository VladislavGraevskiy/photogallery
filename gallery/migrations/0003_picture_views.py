# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20160906_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='views',
            field=models.IntegerField(null=True),
        ),
    ]
