#!/usr/bin/env  python
# -*- coding: utf-8 -*-

from django.db import models

class Demo2(models.Model):
    pass

class Ansible_Host(models.Model):
    group = models.CharField(max_length=50, blank=True, default='')         # 组名
    name = models.CharField(max_length=50, blank=True, default='')          # 主机别名
    ssh_host = models.CharField(max_length=50, blank=True, default='')      # 主机ip
    ssh_user = models.CharField(max_length=50, blank=True, default='')      # 信任的用户名
    ssh_port = models.CharField(max_length=50, blank=True, default='')      # 主机端口
    server_type = models.CharField(max_length=100, blank=True, default='')  # 主机类型
    comment = models.TextField(blank=True, null=True)                        # 备注

class Ansible_Yml_Register(models.Model):
    yml_file = models.CharField(max_length=200, blank=True, default='')         # 注册的yml文件
    yml_maintenancer = models.CharField(max_length=50, blank=True, default='')   # 注册yml的维护人
    yml_parameter = models.TextField(blank=True, null=True)                      # 可接受的参数
    accept_host_group = models.CharField(max_length=200, blank=True, default='')  # yml可接受的hosts组
    comment = models.CharField(max_length=200, blank=True, default='')           # yml的使用说明
    register_time = models.DateTimeField(auto_now_add=True)                      # 注册时间
