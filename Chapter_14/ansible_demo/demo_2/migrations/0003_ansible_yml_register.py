# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_2', '0002_auto_20160605_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ansible_Yml_Register',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yml_file', models.CharField(default=b'', max_length=200, blank=True)),
                ('yml_maintenancer', models.CharField(default=b'', max_length=50, blank=True)),
                ('yml_parameter', models.TextField(null=True, blank=True)),
                ('accept_host_group', models.CharField(default=b'', max_length=200, blank=True)),
                ('comment', models.CharField(default=b'', max_length=200, blank=True)),
                ('register_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
