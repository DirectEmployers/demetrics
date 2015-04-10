# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demetrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('sessions', models.IntegerField(max_length=999999999)),
                ('organic_searches', models.IntegerField(max_length=999999999)),
                ('users', models.IntegerField(max_length=999999999)),
                ('page_views', models.IntegerField(max_length=999999999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DotJobsSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='metric',
        ),
        migrations.AddField(
            model_name='datemetric',
            name='dotjobssite',
            field=models.ForeignKey(to='demetrics.DotJobsSite'),
            preserve_default=True,
        ),
    ]
