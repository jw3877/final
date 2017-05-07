# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20170507_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='reservation start time')),
                ('end_time', models.DateTimeField(verbose_name='reservation end time')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.Resource')),
            ],
        ),
    ]