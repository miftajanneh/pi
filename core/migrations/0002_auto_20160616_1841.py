# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 11:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alatkb',
            options={'verbose_name_plural': 'Alat KB'},
        ),
        migrations.AlterModelOptions(
            name='kb',
            options={'verbose_name_plural': 'KB'},
        ),
        migrations.AlterModelOptions(
            name='kunjungan',
            options={'verbose_name_plural': 'Kunjungan'},
        ),
        migrations.AlterModelOptions(
            name='obat',
            options={'verbose_name_plural': 'Obat'},
        ),
        migrations.RemoveField(
            model_name='kunjungan',
            name='bidan',
        ),
    ]
