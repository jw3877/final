# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_auto_20170509_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.BigIntegerField(default=0)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.Resource')),
            ],
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
