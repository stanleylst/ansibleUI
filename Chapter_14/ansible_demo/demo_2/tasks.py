#!/usr/bin/env  python
# -*- coding: utf-8 -*-
from celery import task
from billiard.exceptions import Terminated
import commands
import os

home_dir = os.path.abspath('.') + '/'

def long_ansible_common(yml_file, log_file=''):
    ansible_playbook = home_dir + '../ansible_file/{0}'.format(yml_file)
    print ansible_playbook
    if not log_file:
    	bits = "set -o pipefail;ansible-playbook {0}|tee -a /tmp/ansible_long.log".format(ansible_playbook)
    else:
        bits = "set -o pipefail;ansible-playbook {0}|tee -a {1}".format(ansible_playbook, log_file)
    (status, output) = commands.getstatusoutput('bash -c "{0}"'.format(bits))


@task(throws=(Terminated,))
def long_ansible_bg(data):
    long_ansible_common('long_cmd_1.yml')
    long_ansible_common('long_cmd_2.yml')
    return {'msg': 'long ansible cmd has been executed'}
 

@task(throws=(Terminated,))
def long_ansible_read_log(data):
    print 'start job'
    for i in xrange(10):
        print str(i) + ': {0}'.format(data['yml_file'])
        long_ansible_common(data['yml_file'], data['log_file'])
    return {'msg': 'long ansible cmd has been executed'}


@task(throws=(Terminated,))
def common_ansible_bg(data):
    extra_vars = str(data['operate']).replace("u'", '\\"').replace("'", '\\"')
    ansible_playbook = home_dir + "../ansible_file/{0}".format(data['yml_file'])
    bits =  "ansible-playbook {0} -e '{1}'|tee -a {2}".format(ansible_playbook, extra_vars, data['log_file'])
    print bits
    comm = 'bash -c "' + 'set -o pipefail;{0}"'.format(bits)
    (status, output) = commands.getstatusoutput(comm)
    if status != 0:
        return {'flag': False}
    return {'flag': True}

