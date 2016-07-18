1 #!/usr/bin/env python
2
3 '''
4 基于Python的动态Inventory脚本举例
5 '''
6
7 import os
8 import sys
9 import argparse
10
11 try:
12     import json
13 except ImportError:
14     import simplejson as json
15
16 class ExampleInventory(object):
17
18     def __init__(self):
19         self.inventory = {}
20         self.read_cli_args()
21
22         # 定义`--list`选项
23         if self.args.list:
24             self.inventory = self.example_inventory()
25         # 定义`--host [hostname]`选项
26         elif self.args.host:
27             # 未部署，我们这里只演示--list选项功能
28             self.inventory = self.empty_inventory()
29         # 如果没有主机组或变量要设置，就返回一个空Inventory
30         else:
31             self.inventory = self.empty_inventory()
32
33         print json.dumps(self.inventory);
34
35     # 用于展示效果的JSON格式的Inventory文件内容
36     def example_inventory(self):
37         return {
38             'group': {
39                 'hosts': ['192.168.28.71', '192.168.28.72'],
40                 'vars': {
41                     'ansible_ssh_user': 'vagrant',
42                     'ansible_ssh_private_key_file':
43                         '~/.vagrant.d/insecure_private_key',
44                     'example_variable': 'value'
45                 }
46             },
47             '_meta': {
48                 'hostvars': {
49                     '192.168.28.71': {
50                         'host_specific_var': 'foo'
51                     },
52                     '192.168.28.72': {
53                         'host_specific_var': 'bar'
54                     }
55                 }
56             }
57         }
58
59     # 返回仅用于测试的空Inventory 
60     def empty_inventory(self):
61         return {'_meta': {'hostvars': {}}}
62
63     # 读取并分析读入的选项和参数
64     def read_cli_args(self):
65         parser = argparse.ArgumentParser()
66         parser.add_argument('--list', action = 'store_true')
67         parser.add_argument('--host', action = 'store')
68         self.args = parser.parse_args()
69
70 # 获取Inventory
71 ExampleInventory()
