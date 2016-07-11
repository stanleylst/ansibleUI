#!/usr/bin/env python
import ansible.runner
runner = ansible.runner.Runner(
   module_name='echopong',
   module_args="args='ok'",
   pattern='localhost',
   forks=10
)
datastructure = runner.run()
print datastructure
