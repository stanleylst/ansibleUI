#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import jinja2, os
from tempfile import NamedTemporaryFile

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.errors import AnsibleParserError
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import constants as C

from ansible.utils.display import Display
from .callbacks import ResultCallback
import re

class New_Display(Display):

    def __init__(self, log_file='', debug=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = debug
        self.log_file = log_file
        self.log_add = []

    def display(self, msg, *args, **kwargs):
        if self.debug:
            super().display(msg, *args, **kwargs)
        ansi_escape = re.compile(r'\x1b[^m]*m')
        msg = ansi_escape.sub('', msg)
        self.log_add.append(msg)
        if self.log_file:
            with open(self.log_file, 'a+') as f:
                f.write(msg + '\n')

class Options(object):

    def __init__(self, connection=C.DEFAULT_TRANSPORT,
                forks=C.DEFAULT_FORKS,
                become=False,
                become_method=C.DEFAULT_BECOME_METHOD,
                become_user=None,
                check=False,
                module_path=None,
                remote_user=C.DEFAULT_REMOTE_USER,
                private_key_file=C.DEFAULT_PRIVATE_KEY_FILE,
                ssh_common_args='',
                sftp_extra_args='',
                scp_extra_args='',
                ssh_extra_args='',
                verbosity=0,
                listhosts=False,
                listtags=False,
                listtasks=False,
                syntax=False,
                inventory=None,
                diff=False):
        self.connection = connection
        self.forks = forks
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.check = check
        self.module_path = module_path
        self.remote_user = remote_user
        self.private_key_file = private_key_file
        self.ssh_common_args = ssh_common_args
        self.sftp_extra_args = sftp_extra_args
        self.scp_extra_args = scp_extra_args
        self.ssh_extra_args = ssh_extra_args
        self.verbosity = verbosity
        self.listhosts = listhosts
        self.listtags = listtags
        self.listtasks = listtasks
        self.syntax = syntax
        self.inventory = inventory
        self.diff = diff


class Ansi_Template(object):

    def __init__(self, default_user='vmuser', default_port='22'):
        self.inventory_template = """
{%- for host in hosts %}
    {%- set host_template = host.name + ' ansible_ssh_port=' + host.port + ' ansible_ssh_host=' + host.ip + ' ansible_ssh_user=' + host.user %}
    {%- if host.pass %}
        {%- set host_template = host_template + ' ansible_ssh_pass=' + host.pass %}
    {%- endif %}
    {%- if host.use_root %}
        {%- set host_template = host_template + ' ansible_ssh_user=root' %}
    {%- endif %}
    {%- if host.private_key_file %}
        {%- set host_template = host_template + ' ansible_private_key_file=' + host.private_key_file %}
    {%- endif %}
    {%- if host.su == true and host.sudo_pass %}
        {%- set host_template = host_template + ' ansible_become=true ansible_become_user=root ansible_become_method=su ansible_become_pass=' + host.sudo_pass %}
    {%- endif %}
{{host_template}}
{%- endfor %}
"""
        self.default_user = default_user
        self.default_port = default_port
        self.debug = False
        self.step_template = """
- name: template
  hosts: all
  gather_facts: no

  tasks:

      - {{module}}: {{command_args|default('')}}
"""

    def form_host(self, host_list, use_root=False):
        for host in host_list:
            if 'user' not in host or not host['user']:
                host['user'] = self.default_user
            if 'port' not in host or not host['port']:
                host['port'] = self.default_port
            else:
                host['port'] = str(host['port'])
            host['use_root'] = False
            if use_root:
                host['use_root'] = True
            if 'name' not in host or not host['name']:
                host['name'] = '{0}@{1}__{2}'.format(host['user'], host['ip'], host['port'])
        return host_list

    def make_host_template(self, host_list, root_hosts=False):
        template = jinja2.Template(self.inventory_template)
        host_list = self.form_host(host_list, root_hosts)
        rendered_inventory = template.render({'hosts': host_list})
        host_file = NamedTemporaryFile(delete=False)
        host_file.write(rendered_inventory.encode('utf-8'))
        host_file.close()
        return [i['name'] for i in host_list], host_file.name

    def make_playbook_template(self, module, args):
        template = jinja2.Template(self.step_template)
        rendered_inventory = template.render({'module': module, 'command_args': args})
        if self.debug == True:
            print(rendered_inventory)
        playbook_file = NamedTemporaryFile(delete=False)
        playbook_file.write(rendered_inventory.encode('utf-8'))
        playbook_file.close()
        return rendered_inventory, playbook_file.name


module_dir = os.path.abspath(os.path.dirname(__file__)) + '/modules/'
ansible_cfg = os.path.abspath(os.path.dirname(__file__)) + '/ansible.cfg'


class Ansi_Play2(object):

    def __init__(self,
                 module_path=module_dir,
                 ansible_cfg=ansible_cfg,
                 debug=False):
        self.options = Options()
        self.options.module_path = module_path
        os.environ['ANSIBLE_CONFIG'] = ansible_cfg
        self.loader = DataLoader()
        self.result = {
            'errno': 0,
            'summary': {},
            'detail': [],
            'success': False,
            'msg': '',
        }
        self.debug = debug

    def run(self, playbook,
            hosts,
            extra_vars={},
            log='',
            with_output=False,
            use_root=False):
        self.result['playbook'] = playbook
        if not os.path.exists(playbook):
            result = {
                'errno': -3,
                'msg': 'not exists playbook: ' + playbook
            }
        else:
            AT = Ansi_Template()
            hosts, host_file = AT.make_host_template(hosts, use_root)
            extra_vars['ansible_hosts'] = ':'.join(hosts)
            inventory = InventoryManager(loader=self.loader, sources=[host_file])
            variable_manager = VariableManager(loader=self.loader, inventory=inventory)
            variable_manager.extra_vars = extra_vars
            pbex = PlaybookExecutor(playbooks=[playbook],
                                    inventory=inventory,
                                    variable_manager=variable_manager,
                                    loader=self.loader,
                                    options=self.options,
                                    passwords={})

            new_display = New_Display(log_file=log, debug=self.debug)
            results_callback = ResultCallback(new_display=new_display)

            pbex._tqm._stdout_callback = results_callback
            try:
                errno = pbex.run()
                result = results_callback.tasks
                result['errno'] = errno
            except AnsibleParserError as e:
                msg = 'syntax problems: {0}'.format(str(e))
                result = {
                    'errno': -2,
                    'msg': msg
                }
                self.write_log(log, msg)
                print('syntax problems: {0}'.format(str(e)))
            if with_output:
                result['output'] = '\n'.join(new_display.log_add)
            if result['errno'] != -2 and not result['summary']:
                msg = 'no host executed'
                result = {
                    'errno': -1,
                    'msg': msg
                }
                self.write_log(log, msg)
            os.unlink(host_file)
        self.result.update(result)
        if self.result['errno'] != 0:
            self.result['msg'] = '无法配置完成，请联系管理员！'
        return self.result

    def write_log(self, log='', msg=''):
        if log:
            with open(log, 'a+') as f:
                f.write(msg + '\n')
