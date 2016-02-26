# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0006_auto_20141024_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='COACH',
            field=models.CharField(default=b'', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='is_teamMember',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='teamCategory',
            field=models.CharField(default=b'', max_length=1, choices=[(b'', b''), (b'A', b'A'), (b'B', b'B'), (b'C', b'C')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='teamRole',
            field=models.CharField(default=b'\xe9\x98\x9f\xe5\x91\x98', max_length=5, choices=[(b'\xe9\x98\x9f\xe9\x95\xbf', b'\xe9\x98\x9f\xe9\x95\xbf'), (b'\xe5\x9b\xa2\xe6\x94\xaf\xe4\xb9\xa6', b'\xe5\x9b\xa2\xe6\x94\xaf\xe4\xb9\xa6'), (b'\xe9\x98\x9f\xe5\x91\x98', b'\xe9\x98\x9f\xe5\x91\x98')]),
            preserve_default=True,
        ),
    ]
