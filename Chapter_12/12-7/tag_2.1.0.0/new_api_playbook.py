#!/usr/bin/env python

import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
try:
    from ansible.utils.display import log_file
except:
    pass
import sys

variable_manager = VariableManager()
loader = DataLoader()

inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list='/etc/ansible/hosts')

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'remote_user', 'verbosity', 'check'])
options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100,private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False, become_method=None, become_user=None, remote_user=None, verbosity=None, check=False)

playbook_path = 'test.yml'                    # modify here, change playbook
variable_manager.extra_vars = {"args": "pong",} # modify here, This can accomodate various other command line arguments.`
if not os.path.exists(playbook_path):
    print '[INFO] The playbook does not exist'
    sys.exit()

passwords = {}

pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)

code = pbex.run()
stats = pbex._tqm._stats
hosts = sorted(stats.processed.keys())
result = [{h: stats.summarize(h)} for h in hosts]
results = {'code': code, 'result': result, 'playbook': playbook_path} 
print(results)
