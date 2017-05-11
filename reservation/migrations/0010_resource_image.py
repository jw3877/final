# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import reservation.models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_auto_20170511_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='image',
            field=models.ImageField(default='resource.png', upload_to=reservation.models.Resource.user_directory_path),
        ),
    ]