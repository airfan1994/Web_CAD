# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_auto_20141022_0254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athleteinfo',
            name='GPA',
        ),
        migrations.AddField(
            model_name='athleteinfo',
            name='GPA_Rank',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athleteinfo',
            name='address',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athleteinfo',
            name='birth',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athleteinfo',
            name='phoneNum',
            field=models.CharField(default=b'', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athleteinfo',
            name='politicalBackground',
            field=models.CharField(default=b'', max_length=4, choices=[(b'\xe7\xbe\xa4\xe4\xbc\x97', b'\xe7\xbe\xa4\xe4\xbc\x97'), (b'\xe5\x85\xb1\xe9\x9d\x92\xe5\x9b\xa2\xe5\x91\x98', b'\xe5\x85\xb1\xe9\x9d\x92\xe5\x9b\xa2\xe5\x91\x98'), (b'\xe7\xa7\xaf\xe6\x9e\x81\xe5\x88\x86\xe5\xad\x90', b'\xe7\xa7\xaf\xe6\x9e\x81\xe5\x88\x86\xe5\xad\x90'), (b'\xe9\xa2\x84\xe5\xa4\x87\xe5\x85\x9a\xe5\x91\x98', b'\xe9\xa2\x84\xe5\xa4\x87\xe5\x85\x9a\xe5\x91\x98'), (b'\xe5\x85\x9a\xe5\x91\x98', b'\xe5\x85\x9a\xe5\x91\x98')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athleteinfo',
            name='work',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='department',
            field=models.CharField(default=b'', max_length=10, choices=[(b'\xe7\x94\xb5\xe5\xad\x90\xe5\xb7\xa5\xe7\xa8\x8b\xe7\xb3\xbb', b'\xe7\x94\xb5\xe5\xad\x90\xe5\xb7\xa5\xe7\xa8\x8b\xe7\xb3\xbb'), (b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe7\xb3\xbb', b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe7\xb3\xbb')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='studentClass',
            field=models.CharField(default=b'', max_length=6),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='studentID',
            field=models.CharField(default=b'', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='gender',
            field=models.CharField(default=b'', max_length=6, choices=[(b'male', b'male'), (b'female', b'female')]),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='name',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
