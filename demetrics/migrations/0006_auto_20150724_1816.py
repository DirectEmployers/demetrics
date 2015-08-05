# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demetrics', '0005_dotjobssite_google_analytics_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='datemetric',
            name='campaigns',
            field=models.IntegerField(default=0, max_length=999999999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datemetric',
            name='direct',
            field=models.IntegerField(default=0, max_length=999999999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datemetric',
            name='feeds',
            field=models.IntegerField(default=0, max_length=999999999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datemetric',
            name='referrals',
            field=models.IntegerField(default=0, max_length=999999999),
            preserve_default=False,
        ),
    ]
