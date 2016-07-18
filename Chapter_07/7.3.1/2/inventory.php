#!/usr/bin/php
<?php

/**
* @file
*基于PHP的动态Inventory脚本举例
*/

/**
* 
*
* @return array
*生成用于展示效果的JSON格式的Inventory文件内容
*/
function example_inventory() {
return [
'group' => [
'hosts' => ['192.168.28.71', '192.168.28.72'],
'vars' => [
'ansible_ssh_user' => 'vagrant',
'ansible_ssh_private_key_file' => '~/.vagrant.d/insecure_private_key',
'example_variable' => 'value',
],
],
'_meta' => [
'hostvars' => [
'192.168.28.71' => [
'host_specific_var' => 'foo',
],
'192.168.28.72' => [
'host_specific_var' => 'bar',
],
],
],
];
}

/**
* 
*
* @return array
* 生成用于测试的空Inventory
*/
function empty_inventory() {
return ['_meta' => ['hostvars' => new stdClass()]];
}

/**
* 获取Inventory
*
* @param array $argv
* 以数组形式传入变量(as returned by $_SERVER['argv']).
*
* @return array
* 
*/
function get_inventory($argv = []) {
$inventory = new stdClass();

// 设置`--list`选项
if (!empty($argv[1]) && $argv[1] == '--list') {
$inventory = example_inventory();
}
// 定义`--host [hostname]` 选项
elseif ((!empty($argv[1]) && $argv[1] == '--host') && !empty($argv[2])) {
//未部署，我们这里只演示--list选项功能
$inventory = empty_inventory();
}
//如果没有主机组或变量要设置，就返回一个空Inventory
else {
$inventory = empty_inventory();
}

print json_encode($inventory);
}

// 获取Iventory.
get_inventory($_SERVER['argv']);

?>
