#!/usr/bin/env python

import os
import sys
import re
import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
try:
    from ansible.utils.display import log_file, log_add
except:
    print('after modifying ansible.utils.display, you can use Ansi_play2.run()')
from ansible.plugins.callback import CallbackBase
from ansible.errors import AnsibleParserError

from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from copy import copy

class ResultCallback(CallbackBase):
    ''' if needed, you can modify it yourself'''    
    def __init__(self, *args):
        super(ResultCallback, self).__init__(*args)
        self.ok = {}
        self.fail = {}
        self.unreachable = {}
        self.playbook = ''
        self.no_hosts = False
        self.msg_list = {}

    def deal_result(self, res, host, status):
        result = copy(res)
        del_keys = [key for key in result.keys() if key.startswith('_')]
        del_keys += ['invocation']
        for key in del_keys:
            if key in result:
                del result[key]
        if host not in self.msg_list:
            self.msg_list[host] = {'msg': [], 'status': status}
        if self.msg_list[host]['status'] in ['ok']:
            self.msg_list[host]['status'] = status
        msg = ''
        if 'stdout' in result:
            msg += result['stdout'] + '\n'
        if 'stderr' in result:
            msg += result['stderr'] + '\n'
        if 'msg' in result:
            msg += result['msg']
        self.msg_list[host]['msg'].append(msg)
        return result
   
    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        self.runner_on_ok(host, result._result)
        if host not in self.ok:
            self.ok[host] = []
        self.ok[host].append(self.deal_result(result._result, host, 'ok'))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, ignore_errors)
        if host not in self.fail:
            self.fail[host] = []
        self.fail[host].append(self.deal_result(result._result, host, 'failed'))

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        if host not in self.unreachable:
            self.unreachable[host] = []
        print(self.unreachable)
        self.unreachable[host].append(self.deal_result(result._result, host, 'unreachable'))


    def v2_playbook_on_play_start(self, play):
        self.playbook_on_play_start(play.name)
        self.playbook = play.name

    def v2_playbook_on_no_hosts_matched(self):
        self.playbook_on_no_hosts_matched()
        self.no_hosts = True

class Ansi_Play2(object):

    def __init__(self, playbook='', extra_vars={},
                        host_list='/etc/ansible/hosts', 
                        connection='ssh',
                        become=False,
                        become_user=None,
                        module_path=None,
                        fork=50,
                        ansible_cfg=None,   #os.environ["ANSIBLE_CONFIG"] = None
                        passwords={},
                        check=False):
        self.playbook = playbook
        self.passwords = passwords
        Options = namedtuple('Options',
                   ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path',
                   'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                      'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        self.options = Options(listtags=False, listtasks=False, 
                              listhosts=False, syntax=False, 
                              connection=connection, module_path=module_path, 
                              forks=fork, private_key_file=None, 
                              ssh_common_args=None, ssh_extra_args=None, 
                              sftp_extra_args=None, scp_extra_args=None, 
                              become=become, become_method=None, 
                              become_user=become_user, 
                              verbosity=None, check=check)
        if ansible_cfg != None:
            os.environ["ANSIBLE_CONFIG"] = ansible_cfg
        self.variable_manager = VariableManager()
        self.variable_manager.extra_vars = extra_vars
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,  host_list=host_list)
    
    def run(self, log):
        if not self.playbook:
            code = 999
            simple = 'playbook must exist'
            return code, simple, None
        if log:
            log_file.append(log)
        if not os.path.exists(self.playbook):
            code = 1000
            results = 'not exists playbook: ' + self.playbook
            return code, results, None
        pbex = PlaybookExecutor(playbooks=[self.playbook],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords=self.passwords)
        try:
            code = pbex.run()
        except AnsibleParserError:
            code = 1001
            results = 'syntax problems in ' + self.playbook
            return  code, results, None
        stats = pbex._tqm._stats
        hosts = sorted(stats.processed.keys())
        results = [{h: stats.summarize(h)} for h in hosts]
        if not results:
            code = 1002
            results = 'no host executed in ' + self.playbook
            return  code, results, None
        complex = '\n'.join(log_add)
        return code, results, complex

    def run_module(self, hosts='localhost', rules=[{'module': 'setup'}]):
        '''
        rules=[
              {'module': 'shell', 'args': 'echo "ok"', 'register': 'echo_ok'},
              {'module': 'debug', 'args': {'msg': '{{echo_ok.stdout}}'}}
        ]
        '''
        tasks = []
        for rule in rules:
            if 'register' in rule:
                register = rule.pop('register')
            tasks.append(dict(dict(action=rule), register=register))
        play_source =  dict(
            name = "Ansible Play",
            hosts = 'localhost',
            gather_facts = 'no',
            tasks = tasks
        )
        results_callback = ResultCallback()
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        qm = None
        try:
            tqm = TaskQueueManager(
                  inventory=self.inventory,
                  variable_manager=self.variable_manager,
                  loader=self.loader,
                  options=self.options,
                  passwords=self.passwords,
                  stdout_callback=results_callback,
             )
            tqm.run(play)
            return results_callback
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_need_data(self):
        if not self.playbook:
            code = 999
            simple = 'playbook must exist'
            return code, simple, None
        if not os.path.exists(self.playbook):
            code = 1000
            complex = {'playbook': self.playbook, 
           'msg': self.playbook + ' playbook does not exist', 'flag': False}
            simple = 'playbook does not exist about ' + self.playbook
            return code, simple, complex
        pbex = PlaybookExecutor(playbooks=[self.playbook], 
                                inventory=self.inventory, 
                                variable_manager=self.variable_manager, 
                                loader=self.loader, 
                                options=self.options, 
                                passwords=self.passwords)
        results_callback = ResultCallback()
        pbex._tqm._stdout_callback = results_callback
        try:
            code = pbex.run()
        except AnsibleParserError:
            code = 1001
            simple = {'playbook': self.playbook,
                      'msg': 'syntax problems in ' + self.playbook, 'flag': False,
                      'msg_list': {'status': 'unknown', 'msg': 'syntax problems'}}
            complex = 'syntax problems in ' + self.playbook
            return code, simple, complex
        if results_callback.no_hosts:
            code = 1002
            complex = 'no hosts matched in ' + self.playbook
            simple = {'executed': False, 'flag': False, 'playbook': self.playbook,
                      'msg': 'no_hosts', 'msg_list': {'status': 'unknown', 'msg': 'no_hosts'}}
            return code, simple, complex
        else:
            msg_list = results_callback.msg_list
            ok = results_callback.ok
            fail = results_callback.fail
            unreachable = results_callback.unreachable
            ok_all = list(ok.keys())
            fail_all = list(fail.keys())
            unreachable_hosts = list(unreachable.keys())
            fail_hosts = list(set(fail_all) - set(unreachable_hosts))
            ok_hosts = list(set(ok_all) - set(unreachable_hosts) - set(fail_hosts))
            if code != 0:
                complex = {'playbook': results_callback.playbook, 'ok': ok,
                 'fail': fail, 'unreachable': unreachable, 'flag': False}
                simple = {'executed': True, 'flag': False, 'playbook': self.playbook, 'msg_list': msg_list,
                         'msg': {'playbook': self.playbook, 'ok_hosts': ok_hosts, 'fail': fail_hosts, 'unreachable': unreachable_hosts}}
                return code, simple, complex
            else:
                complex = {'playbook': results_callback.playbook, 'ok': ok,
                 'fail': fail, 'unreachable': unreachable, 'flag': True}
                simple = {'executed': True, 'flag': True, 'playbook': self.playbook, 'msg_list': msg_list,
                         'msg': {'playbook': self.playbook, 'ok_hosts': ok_hosts, 'fail': fail_hosts, 'unreachable': unreachable_hosts}}
                return code, simple, complex

if __name__ == '__main__':
    book2 = Ansi_Play2('test.yml')
    # User can choose one of followings.
    # if you need data of detail to combine with your program, choose first. 
    # if not care about detail and want to add to log, choose second.
    code, simple, complex = book2.run_need_data()   # get more details about playbook 
    print(code, simple, complex)
    print(simple['msg_list'])
    # simple: {'msg': {'fail': [], 'unreachable': [], 'ok_hosts': [u'localhost'], 'playbook': 'test.yml'}, 'flag': True, 'executed': True, 'playbook': 'test.yml'} 
    # complex: {'code': 0, 'ok': {u'localhost': {u'invocation': {u'module_name': u'debug', u'module_args': {u'var': u'res'}}, u'res': {u'changed': True, u'end': u'2016-07-16 00:29:42.936217', u'stdout': u'123', u'cmd': u'bash -c "echo 123; sleep 10"', u'rc': 0, u'start': u'2016-07-16 00:29:32.932963', u'stderr': u'', u'delta': u'0:00:10.003254', u'stdout_lines': [u'123'], u'warnings': []}, u'changed': False, u'_ansible_verbose_always': True, u'_ansible_no_log': False}}, 'flag': True, 'playbook': u'test', 'fail': {}, 'unreachable': {}}
    #code, simple, complex = book2.run('/tmp/aa.log')   #  get simple result about playbook, and log detail in log_file
    #print(code, simple, complex)
    # simple: 0
    # complex: [{u'localhost': {'unreachable': 0, 'skipped': 0, 'ok': 2, 'changed': 1, 'failures': 0}}]
    # log_file: '/tmp/aa.log'
    #complex = book2.play()   #  get simple result about playbook, and log detail in log_file
    #print(complex.ok, complex.fail)

    book_m2 = Ansi_Play2()
    rules=[
        {'module': 'shell', 'args': 'echo "ok"', 'register': 'echo_ok'},
        {'module': 'debug', 'args': {'msg': '{{echo_ok.stdout}}'}}
    ]
    data = book_m2.run_module('localhost', rules)
    print(data.ok)
