# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_auto_20141120_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='applyTeamTime',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
