# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demetrics', '0004_googleanalyticsaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='dotjobssite',
            name='google_analytics_account',
            field=models.ForeignKey(default=0, to='demetrics.GoogleAnalyticsAccount'),
            preserve_default=False,
        ),
    ]
