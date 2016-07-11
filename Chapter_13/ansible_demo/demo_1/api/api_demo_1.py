#!/usr/bin/env  python
# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.decorators import detail_route, list_route

from .models import *
from .serializers import *
import os
import commands
import json

home_dir = os.path.abspath('.') + '/'

class DemoViewSet(viewsets.ModelViewSet):
    serializer_class = DemoSerializer
    queryset = Demo.objects.all()

    @list_route(methods=['get', 'post'])                      
    def touch(self, request):
        os.system('touch /tmp/abc')
        return Response({'msg': '/tmp/abc has been touched'})

    @list_route(methods=['get', 'post'])                      
    def touch_2(self, request):
        os.system('ansible localhost -a "touch /tmp/bcf"')
        return Response({'msg': '/tmp/bcf has been touched'})

    @list_route(methods=['get', 'post'])                   
    def touch_3(self, request):
        bits = 'ansible localhost -a "touch /tmp1/eee"'
        (status, output) = commands.getstatusoutput(bits)
        if status != 0:
            return Response({'msg': '/tmp1/eee has not been touched', 'output': output})
        return Response({'msg': '/tmp/eee has been touched', 'output': output})


    @list_route(methods=['get', 'post'])                      
    def touch_4(self, request):
        bits = 'ansible localhost -a "touch /tmp1/eee"|tee -a /tmp/ansible.log'
        (status, output) = commands.getstatusoutput(bits)
        if status != 0:
            return Response({'msg': '/tmp1/eee has not been touched', 'output': output})
        return Response({'msg': '/tmp/eee has been touched', 'output': output})

    @list_route(methods=['get', 'post'])
    def touch_5(self, request):
        bits = 'set -o pipefail;ansible localhost -a "touch /tmp1/eee"|tee -a /tmp/ansible.log'
        (status, output) = commands.getstatusoutput('bash -c "{0}"'.format(bits))
        if status != 0:
            return Response({'msg': '/tmp1/eee has not been touched', 'output': output})
        return Response({'msg': '/tmp/eee has been touched', 'output': output})

    @list_route(methods=['get', 'post'])
    def touch_6(self, request):
        data = request.data
        filename = data['filename']
        bits = 'set -o pipefail;ansible localhost -a "touch {0}"|tee -a /tmp/ansible.log'.format(filename)
        (status, output) = commands.getstatusoutput('bash -c "{0}"'.format(bits))
        if status != 0:
            return Response({'msg': '{0} has not been touched'.format(filename), 'output': output})
        return Response({'msg': '{0} has been touched'.format(filename), 'output': output})

    @list_route(methods=['get', 'post'])
    def touch_7(self, request):
        ansible_playbook = home_dir + '../ansible_file/touch_7.yml'
        print ansible_playbook
        bits = 'set -o pipefail;ansible-playbook {0}|tee -a /tmp/ansible.log'.format(ansible_playbook)
        (status, output) = commands.getstatusoutput('bash -c "{0}"'.format(bits))
        if status != 0:
            return Response({'msg': '{0} has not been touched'.format('ggg'), 'output': output})
        return Response({'msg': '{0} has beentouched'.format('ggg'), 'output': output})

    @list_route(methods=['get', 'post'])
    def touch_8(self, request):
        data = str(request.data).replace("u'", '\\"').replace("'", '\\"')
        ansible_playbook = home_dir + "../ansible_file/touch_8.yml"
        bits =  'ansible-playbook {0} -e'.format(ansible_playbook) + " '{0}' ".format(data) + '|tee -a /tmp/ansible.log'
        comm = 'bash -c "' + 'set -o pipefail;{0}"'.format(bits)
        (status, output) = commands.getstatusoutput(comm)
        if status != 0:
            return Response({'msg': '{0} has not been touched'.format(request.data['filename']), 'output': output})
        return Response({'msg': '{0} has been touched'.format(request.data['filename']), 'output': output})



