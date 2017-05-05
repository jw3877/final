# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField(verbose_name='available start time')),
                ('end_time', models.DateTimeField(verbose_name='availabile end time')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('resources', models.ManyToManyField(to='reservation.Resource')),
            ],
        ),
    ]
