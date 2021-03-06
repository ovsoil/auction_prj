# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auto_20161022_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='image',
        ),
        migrations.AddField(
            model_name='good',
            name='details',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='good',
            name='image01',
            field=models.ImageField(blank=True, default='img/01.jpg', null=True, upload_to='img/'),
        ),
        migrations.AddField(
            model_name='good',
            name='image02',
            field=models.ImageField(blank=True, default='img/02.jpg', null=True, upload_to='img/'),
        ),
        migrations.AddField(
            model_name='good',
            name='image03',
            field=models.ImageField(blank=True, default='img/03.jpg', null=True, upload_to='img/'),
        ),
        migrations.AddField(
            model_name='good',
            name='image04',
            field=models.ImageField(blank=True, default='img/04.jpg', null=True, upload_to='img/'),
        ),
    ]
