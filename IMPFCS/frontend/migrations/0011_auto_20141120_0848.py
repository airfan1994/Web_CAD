# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0010_userinfo_teamname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='COACH',
            new_name='coach',
        ),
    ]
