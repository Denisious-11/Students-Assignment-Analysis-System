# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-03-10 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OAPC_app', '0003_plagiarism_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('m_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=40)),
                ('file', models.CharField(max_length=100)),
                ('matching_content', models.TextField()),
            ],
        ),
    ]
