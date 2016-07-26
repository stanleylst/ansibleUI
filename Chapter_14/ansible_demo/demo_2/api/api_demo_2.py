#!/usr/bin/env  python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.decorators import list_route

from .models import *
from .serializers import *
import os
import commands
import json
import itertools
from demo_2.tools.parse_hosts import Generate_ansible_hosts
from demo_2.tasks import *
from celery.task.control import revoke
from celery.result import AsyncResult
from time import sleep
from tempfile import NamedTemporaryFile

home_dir = os.path.abspath('.') + '/'

class Ansible_HostViewSet(viewsets.ModelViewSet):
    serializer_class = Ansible_HostSerializer
    queryset = Ansible_Host.objects.all()

class Ansible_Yml_RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = Ansible_Yml_RegisterSerializer
    queryset = Ansible_Yml_Register.objects.all()

class Demo2ViewSet(viewsets.ModelViewSet):
    serializer_class = Demo2Serializer
    queryset = Demo2.objects.all()

    def generate_hosts(self):
        data = Ansible_Host.objects.all().values()
        s_data = [{'group': group, 'items': list(items)} for group, items in itertools.groupby(data, lambda x: x['group'])]
        generate_hosts = Generate_ansible_hosts('/tmp/hosts')
        try:
            generate_hosts.create_all_servers(s_data)
            msg = 'hosts has been create'
            flag = True
        except:
            msg = 'hosts has not been create'
            flag = False
        return msg, flag

    @list_route(methods=['get', 'post'])                      
    def create_ansible_hosts(self, request):
        msg, flag = self.generate_hosts()
        return Response({'msg': msg, 'flag': flag})

    @list_route(methods=['get', 'post'])
    def create_ansible_hosts_add(self, request):
        data = request.data
        Ansible_Host.objects.create(**data).save()
        msg, flag = self.generate_hosts()
        return Response({'msg': msg, 'flag': flag})

    @list_route(methods=['get', 'post'])
    def create_ansible_hosts_delete(self, request):
        data = request.data
        Ansible_Host.objects.filter(id=data['remove_id']).delete()
        msg, flag = self.generate_hosts()
        return Response({'msg': msg, 'flag': flag})

    @list_route(methods=['get', 'post'])
    def create_ansible_hosts_modify(self, request):
        data = request.data
        Ansible_Host.objects.filter(id=data['id']).update(**data)
        msg, flag = self.generate_hosts()
        return Response({'msg': msg, 'flag': flag})

    @list_route(methods=['get', 'post'])
    def long_ansible_background_cmd(self, request):
        data = request.data
        s1 = long_ansible_bg.s(data)
        res = s1.delay()
        return Response({'task_id': res.task_id})

    @list_route(methods=['get', 'post'])
    def long_ansible_revoke(self, request):
        data = request.data
        task_id = data['task_id']
        res = AsyncResult(task_id)
        revoke(task_id, terminate=True, signal='SIGKILL')
        return Response({'msg': task_id + ' has been revoked'})

    def check_task_end(self, task_id):
        res = AsyncResult(task_id)
        return res.state

    @list_route(methods=['get', 'post'])
    def read_long_ansible(self, request):
        data = request.data
        if not data.has_key('log_file'):
            log_file = '/tmp/ansible_long.log'
        else:
            log_file = data['log_file']
        if not os.path.exists(log_file):
            data['read_flag'] = True
            data['logs'] = ''
            return Response(data)
        with open(log_file, 'r') as f:
            f.seek(data['seek'])
            data['logs'] = f.read()
            data['seek'] = f.tell()
        data['state'] = self.check_task_end(data['task_id'])
        if data['state'] in ['SUCCESS', 'FAILURE', 'REVOKED']:
            data['read_flag'] = False
        else:
            data['read_flag'] = True
        return Response(data)

    @list_route(methods=['get', 'post'])
    def execute_long_ansible(self, request):
        data = request.data
        f = NamedTemporaryFile(delete=False)
        data['log_file'] = f.name
        res = long_ansible_read_log.delay(data)
        return Response({'task_id': res.task_id, 'log_file': f.name})

    @list_route(methods=['get', 'post'])
    def file_upload(self, request):
        all_str = request.data['para']
        all_data = json.loads(all_str)
        saved_file_name = all_data['saved_file_name']    # 保存的文件名
        saved_file_dir = os.path.dirname(saved_file_name)
        filename = request.data['file']
        file_name = str(filename)
        if not os.path.exists(saved_file_dir):               # 目录不存在时，为其创建
            os.makedirs(saved_file_dir)
        try:
            destination = open(saved_file_name, 'wb+')
            for chunk in filename.chunks():
                destination.write(chunk)
            destination.close()
            return Response({'flag': True})
        except:
            return Response({'flag': False})

    @list_route(methods=['get', 'post'])
    def create_yml_file_define(self, request):
        data = request.data
        Ansible_Yml_Register.objects.create(**data)
        return Response({'flag': True})

    @list_route(methods=['get', 'post'])
    def delete_yml_file_define(self, request):
        data = request.data
        Ansible_Yml_Register.objects.filter(id=data['remove_id']).delete()
        return Response({'flag': True})

    @list_route(methods=['get', 'post'])
    def update_yml_file_define(self, request):
        data = request.data
        Ansible_Yml_Register.objects.filter(id=data['id']).update(**data)
        return Response({'flag': True})


    @list_route(methods=['get', 'post'])
    def execute_yml_ansible(self, request):
        data = request.data
        f = NamedTemporaryFile(delete=False)
        data['log_file'] = f.name
        res = common_ansible_bg.delay(data)
        return Response({'task_id': res.task_id, 'log_file': f.name})