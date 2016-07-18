#!/bin/bash
# 安装Apache
yum install --quiet -y httpd httpd-devel
# 复制配置文件
cp /path/to/config/httpd.conf /etc/httpd/conf/httpd.conf
cp /path/to/httpd-vhosts.conf /etc/httpd/conf/httpd-vhosts.conf
# 启动Apache，并设置开机启动
service httpd start
chkconfig httpd on

