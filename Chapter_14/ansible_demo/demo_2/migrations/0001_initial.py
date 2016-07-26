# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ansible_Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(default=b'', max_length=50, blank=True)),
                ('name', models.CharField(default=b'', max_length=50, blank=True)),
                ('ssh_host', models.CharField(default=b'', max_length=50, blank=True)),
                ('ssh_user', models.CharField(default=b'', max_length=50, blank=True)),
                ('ssh_port', models.CharField(default=b'', max_length=50, blank=True)),
                ('server_type', models.CharField(default=b'', max_length=100, blank=True)),
                ('commit', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Demo2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]
