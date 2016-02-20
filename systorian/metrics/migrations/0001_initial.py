# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 23:27
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('command', models.CharField(max_length=255)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]