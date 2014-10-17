# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='metric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('sessions', models.IntegerField(max_length=999999999)),
                ('visitors', models.IntegerField(max_length=999999999)),
                ('unique_visitors', models.IntegerField(max_length=999999999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
