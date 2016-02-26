# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0003_auto_20141023_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
                ('gender', models.CharField(default=b'', max_length=6, choices=[(b'\xe7\x94\xb7', b'\xe7\x94\xb7'), (b'\xe5\xa5\xb3', b'\xe5\xa5\xb3')])),
                ('studentID', models.CharField(default=b'', max_length=10)),
                ('department', models.CharField(default=b'', max_length=10, choices=[(b'\xe7\x94\xb5\xe5\xad\x90\xe5\xb7\xa5\xe7\xa8\x8b\xe7\xb3\xbb', b'\xe7\x94\xb5\xe5\xad\x90\xe5\xb7\xa5\xe7\xa8\x8b\xe7\xb3\xbb'), (b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe7\xb3\xbb', b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe7\xb3\xbb')])),
                ('studentClass', models.CharField(default=b'', max_length=6)),
                ('birth', models.DateField(null=True)),
                ('politicalBackground', models.CharField(default=b'', max_length=4, choices=[(b'\xe7\xbe\xa4\xe4\xbc\x97', b'\xe7\xbe\xa4\xe4\xbc\x97'), (b'\xe5\x85\xb1\xe9\x9d\x92\xe5\x9b\xa2\xe5\x91\x98', b'\xe5\x85\xb1\xe9\x9d\x92\xe5\x9b\xa2\xe5\x91\x98'), (b'\xe7\xa7\xaf\xe6\x9e\x81\xe5\x88\x86\xe5\xad\x90', b'\xe7\xa7\xaf\xe6\x9e\x81\xe5\x88\x86\xe5\xad\x90'), (b'\xe9\xa2\x84\xe5\xa4\x87\xe5\x85\x9a\xe5\x91\x98', b'\xe9\xa2\x84\xe5\xa4\x87\xe5\x85\x9a\xe5\x91\x98'), (b'\xe5\x85\x9a\xe5\x91\x98', b'\xe5\x85\x9a\xe5\x91\x98')])),
                ('GPA_Rank', models.CharField(default=b'', max_length=100)),
                ('phoneNum', models.CharField(default=b'', max_length=20)),
                ('address', models.CharField(default=b'', max_length=50)),
                ('work', models.CharField(default=b'', max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='athleteinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='AthleteInfo',
        ),
        migrations.RemoveField(
            model_name='basicinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='BasicInfo',
        ),
    ]
