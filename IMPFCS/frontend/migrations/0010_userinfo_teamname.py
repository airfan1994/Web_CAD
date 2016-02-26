# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0009_auto_20141024_0453'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='teamName',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
