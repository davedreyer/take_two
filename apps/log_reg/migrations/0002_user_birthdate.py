# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]