# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-18 23:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('PokerPlanner', '0003_remove_pokerplayer_is_currently_in_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokertable',
            name='playerLimit',
        ),
        migrations.AddField(
            model_name='pokergame',
            name='playerLimit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='scrumstory',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='scrumstory',
            name='dateCreated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='scrumstory',
            name='name',
            field=models.CharField(default='No name', max_length=200),
        ),
    ]
