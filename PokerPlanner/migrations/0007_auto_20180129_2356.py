# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-29 22:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('PokerPlanner', '0006_auto_20180129_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokercard',
            name='deck',
        ),
        migrations.RemoveField(
            model_name='pokergame',
            name='playerLimit',
        ),
        migrations.AddField(
            model_name='pokergame',
            name='players',
            field=models.ManyToManyField(to='PokerPlanner.PokerPlayer'),
        ),
        migrations.AddField(
            model_name='pokerplayer',
            name='isAccepted',
            field=models.BooleanField(default=False),
        ),
    ]