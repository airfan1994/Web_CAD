# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='gender',
            field=models.CharField(max_length=6, choices=[(b'male', b'male'), (b'female', b'female')]),
        ),
    ]
