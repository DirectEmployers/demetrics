# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demetrics', '0002_auto_20141029_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dotjobssite',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
