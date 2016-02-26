# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_auto_20141024_0443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='GPA_Rank',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='teamRole',
            field=models.CharField(default=b'', max_length=5, choices=[(b'', b''), (b'\xe9\x98\x9f\xe9\x95\xbf', b'\xe9\x98\x9f\xe9\x95\xbf'), (b'\xe5\x9b\xa2\xe6\x94\xaf\xe4\xb9\xa6', b'\xe5\x9b\xa2\xe6\x94\xaf\xe4\xb9\xa6'), (b'\xe9\x98\x9f\xe5\x91\x98', b'\xe9\x98\x9f\xe5\x91\x98')]),
        ),
    ]
