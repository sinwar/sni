# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-28 00:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sni', '0002_auto_20160528_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addthing',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 28, 0, 17, 42, 28206)),
        ),
    ]