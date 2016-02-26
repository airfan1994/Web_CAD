# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_auto_20141120_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_applyingTeam',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='work',
            field=models.CharField(default=b'', max_length=400),
        ),
    ]
