# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0005_auto_20171023_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Reportada'), (2, 'Consolidada'), (3, 'Verificada'), (4, 'Cerrada'), (5, 'Desechada')]),
        ),
    ]
