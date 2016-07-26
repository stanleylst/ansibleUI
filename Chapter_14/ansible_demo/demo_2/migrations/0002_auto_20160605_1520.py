# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_2', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ansible_host',
            old_name='commit',
            new_name='comment',
        ),
    ]
