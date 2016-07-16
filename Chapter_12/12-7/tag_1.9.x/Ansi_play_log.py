#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import re

class Ansi_Play(object):
    ''' 1.9.x 上通过测试   '''
    def __init__(self, playbook, extra_vars={}):   # 初始化参数
        self.stats = callbacks.AggregateStats()
        self.playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        self.extra_vars = extra_vars
        self.playbook = playbook
        self.setbook = self.book_set()

    def book_set(self):              #使用playbook模块
        runner_cb = callbacks.PlaybookRunnerCallbacks(self.stats, verbose=utils.VERBOSITY)
        self.pb = ansible.playbook.PlayBook(
            playbook = self.playbook,
            stats = self.stats,
            extra_vars = self.extra_vars,
            callbacks = self.playbook_cb,
            runner_callbacks = runner_cb
        )

    def ansi_escape(self, text):           #移除linux字体颜色
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', text)

    def run(self, log_file=''):
        if log_file:
            callbacks.log_file.append(log_file)
        simple = self.pb.run()
        detail = self.ansi_escape('\n'.join(callbacks.log_add))
        # 添加日志内容到detail
        return {'simple': simple, 'detail': detail}

if __name__ == "__main__":
    excute = Ansi_Play('test.yml',{'args': 'pong'})
    result = excute.run('/tmp/test.log')
    print result

