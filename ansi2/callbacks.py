#!/usr/bin/env  python
# -*- coding: utf-8 -*-
# 请安装ansible2.6

from ansible.plugins.callback.default import CallbackModule, hostcolor, hostcolor, C, colorize
import re, json

from .parse import ModuleResultParse_Mix


class ResultCallback(CallbackModule, ModuleResultParse_Mix):

    def __init__(self, new_display, v2_type='simple'):
        import re
        new_display = new_display
        self._play = None
        self._last_task_banner = None
        self.v2_type = v2_type
        super(CallbackModule, self).__init__(display=new_display)
        self.tasks = {
            'summary': {},
            'detail': [],
            'success': True,
            'msg': '',
            'report': {
                'ok': [],
                'unreachable': [],
                'failures': [],
                'skiped': []
            }
        }
        self.task = {}
        self._last_task_uuid = None
        self.step = 1

    def _v2_type_complex(self, result):
        host = result._host.get_name()
        module = result._task_fields['action']
        taskName = result._task.get_name().strip()
        loop_args = result._task_fields.get('loop_args', None)
        taskResult = self.parse(module, result)
        if self._last_task_uuid != result._task._uuid:
            if self.task:
                self.tasks['detail'].append(self.task)
            self.task = {'taskName': taskName, 'hosts': {}, 'step': self.step, 'module': module}
            self.step += 1
        if loop_args:
            init_status = {'errno': 96, 'status': 'failed', "when": [], "failed_when": [], 'result': 'Not all items success', 'raw_args': ''}
            if not host in self.task['hosts']:
                self.task['hosts'][host] = dict(init_status, **{'loops': []})
            item = result._result.get('item', None)
            if item:
                taskResult['item'] = item
                self.task['hosts'][host]['loops'].append(taskResult)
                if taskResult['errno'] != 0: self.task['hosts'][host].update(init_status)
            else:
                self.task['hosts'][host].update(taskResult)
                for i in self.task['hosts'][host]['loops']:
                    if i['errno'] != 0: self.task['hosts'][host].update(init_status)
        else:
            self.task['hosts'][host] = taskResult
        self._last_task_uuid = result._task._uuid


    def v2_runner_on_failed(self, result, ignore_errors=False):
        super().v2_runner_on_failed(result, ignore_errors)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_on_ok(self, result):

        super().v2_runner_on_ok(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_on_skipped(self, result):
        super().v2_runner_on_skipped(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_on_unreachable(self, result):
        super().v2_runner_on_unreachable(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_item_on_failed(self, result):
        super().v2_runner_item_on_failed(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_item_on_ok(self, result):
        super().v2_runner_item_on_ok(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_item_on_skipped(self, result):
        super().v2_runner_item_on_skipped(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_runner_item_on_unreachable(self, result):
        super().v2_runner_item_on_unreachable(result)
        if self.v2_type == 'complex':
            getattr(self, '_v2_type_' + self.v2_type)(result)

    def v2_playbook_on_stats(self, stats):
        self._v2_playbook_on_stats(stats)
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.tasks['summary'].update({h: t})
            if t['unreachable'] > 0 or t['failures'] > 0:
                self.tasks['success'] = False
            if t['ok'] > 0:
                self.tasks['report']['ok'].append(h)
            if t['failures'] > 0:
                self.tasks['report']['failures'].append(h)
            if t['skipped'] > 0:
                self.tasks['report']['skipped'].append(h)
            if t['unreachable'] > 0:
                self.tasks['report']['unreachable'].append(h)
        if self.v2_type == 'complex':
            self.tasks['detail'].append(self.task)
            self._v2_fill_reachable_stats()

    def _v2_fill_reachable_stats(self):
        if self.tasks['detail']:
            servers = self.tasks['detail'][0]['hosts'].keys()
        else:
            servers = set([])
        for task in self.tasks['detail']:
            module = task['module']
            taskHosts = task['hosts']
            fillHosts = list(servers - taskHosts.keys())
            for host in fillHosts:
                taskHosts.update(
                    {
                        host: {
                            'errno': -10,
                            'status': 'unreachable',
                            "module": module,
                            "raw_args": {
                            },
                            'result': host + ' is unreachable',
                            "failed_when": [],
                            "when": []
                        }
                    })


    def _v2_playbook_on_stats(self, stats):                  # 解决日志打印2次问题
        self._display.banner("PLAY RECAP")

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self._display.display(u"%s : %s %s %s %s" % (
                hostcolor(h, t),
                colorize(u'ok', t['ok'], C.COLOR_OK),
                colorize(u'changed', t['changed'], C.COLOR_CHANGED),
                colorize(u'unreachable', t['unreachable'], C.COLOR_UNREACHABLE),
                colorize(u'failed', t['failures'], C.COLOR_ERROR)),
                                  screen_only=True
                                  )
            '''
            self._display.display(u"%s : %s %s %s %s" % (
                hostcolor(h, t, False),
                colorize(u'ok', t['ok'], None),
                colorize(u'changed', t['changed'], None),
                colorize(u'unreachable', t['unreachable'], None),
                colorize(u'failed', t['failures'], None)),
                                  log_only=True
                                  )
            '''
        self._display.display("", screen_only=True)

        # print custom stats
        if self._plugin_options.get('show_custom_stats',
                                    C.SHOW_CUSTOM_STATS) and stats.custom:  # fallback on constants for inherited plugins missing docs
            self._display.banner("CUSTOM STATS: ")
            # per host
            # TODO: come up with 'pretty format'
            for k in sorted(stats.custom.keys()):
                if k == '_run':
                    continue
                self._display.display('\t%s: %s' % (k, self._dump_results(stats.custom[k], indent=1).replace('\n', '')))

            # print per run custom stats
            if '_run' in stats.custom:
                self._display.display("", screen_only=True)
                self._display.display(
                    '\tRUN: %s' % self._dump_results(stats.custom['_run'], indent=1).replace('\n', ''))
            self._display.display("", screen_only=True)
