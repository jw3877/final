# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 12:52
from __future__ import unicode_literals

from django.db import migrations, models
import reservation.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_auto_20170512_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='capacity',
            field=models.IntegerField(default=1, validators=[reservation.validators.validate_capacity]),
        ),
    ]
