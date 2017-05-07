# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 00:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_resource_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
