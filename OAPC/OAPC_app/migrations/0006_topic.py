# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-05-06 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OAPC_app', '0005_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('topic_id', models.IntegerField(primary_key=True, serialize=False)),
                ('topic_name', models.CharField(max_length=30)),
                ('subject_name', models.CharField(max_length=30)),
            ],
        ),
    ]
