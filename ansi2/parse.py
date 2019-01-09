#!/usr/bin/env  python
# -*- coding: utf-8 -*-


class ModuleResultBase(object):
    '''
    code: 0, ok
    code: 100, unreachable
    code: 99, skipped
    code: other, failed
    '''

    def parse(self, module, result):
        host = {}
        unreachable = result._result.get('unreachable', False)
        skipped = result._result.get('skipped', False)
        host['when'] = result._task_fields.get('when')
        host['failed_when'] = result._task_fields.get('failed_when')
        if unreachable:
            if module == 'command':
                host['raw_args'] = result._task_fields.get('_raw_params', None)
            else:
                host['raw_args'] = {k: v  for k, v in
                    result._task_fields.get('args', {}).items() if not k.startswith('_')}
            host['result'] = result._result.get('msg', None)
            host['code'] = 100
            host['status'] = 'unreachable'
        elif skipped:
            if module == 'command':
                host['raw_args'] = result._task_fields.get('_raw_params', None)
            else:
                host['raw_args'] = {k: v  for k, v in
                    result._task_fields.get('args', {}).items() if not k.startswith('_')}
            host['result'] = result._result.get('skip_reason', None)
            host['code'] = 99
            host['status'] = 'skipped'
        else:
            host['module'] = module
            use_module = 'module_parse_' + module
            if use_module in self.__dir__():
                getattr(self, use_module)(host, result)
            else:
                self.module_parse_common(host, result)
        return host

    def module_parse_base(self, host, result):
        '''
        tested module: ['copy', 'service', 'cron', 'unarchive', 'synchronize']
        '''
        failed = result._result.get('failed', False)
        if failed:
            host['code'] = 98
            host['status'] = 'failed'
        else:
            host['code'] = 0
            host['status'] = 'success'

    def module_parse_common(self, host, result):
        self.module_parse_base(host, result)
        host['raw_args'] = {k: v  for k, v in
                    result._task_fields.get('args', {}).items() if not k.startswith('_')}
        host['result'] = result._result.get('msg', None)


class ModuleResultParse_Mix(ModuleResultBase):
    '''
    all function names must startswith with module_parse_
    and + module_name(ansible action name)
    '''
    def module_parse_command(self, host, result):
        super().module_parse_base(host, result)
        host['code'] = result._result.get('rc', host['code'])
        host['raw_args'] = result._task_fields['args'].get('_raw_params', None)
        if host['code'] != 0:
            host['result'] = result._result.get('stderr', 'Unknown error')
        else:
            host['result'] = result._result.get('stdout', None)

    def module_parse_setup(self, host, result):
        super().module_parse_base(host, result)
        host['raw_args'] = 'setup'
        host['result'] = result._result.get('ansible_facts', None)

    def module_parse_ping(self, host, result):
        host['raw_args'] = 'ping'
        host['result'] = result._result.get('ping', None)
        if host['result'] == 'pong':
            host['code'] = 0
        else:
            host['code'] = -100

    def module_parse_file(self, host, result):
        super().module_parse_base(host, result)
        host['raw_args'] = {k: v  for k, v in
                    result._task_fields.get('args', {}).items() if not k.startswith('_')}
        host['result'] = result._result.get('module_stdout', None)
