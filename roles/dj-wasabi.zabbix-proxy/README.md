dj-wasabi.zabbix-proxy
=========

[![Build Status](https://travis-ci.org/dj-wasabi/ansible-zabbix-proxy.svg?branch=master)](https://travis-ci.org/dj-wasabi/ansible-zabbix-proxy)

This is an role for installing and maintaining the zabbix-proxy.

This is one of the 'dj-wasabi' roles which configures your whole zabbix environment. See an list for the complete list:

 * zabbix-server (https://galaxy.ansible.com/dj-wasabi/zabbix-server/)
 * zabbix-proxy (https://galaxy.ansible.com/dj-wasabi/zabbix-proxy/)
 * zabbix-javagateway (https://galaxy.ansible.com/dj-wasabi/zabbix-javagateway/)
 * zabbix-agent (https://galaxy.ansible.com/dj-wasabi/zabbix-agent/)

Requirements
------------

This role will work on:

* Red Hat
* Debian
* Ubuntu

So, you'll need one of those operating systems.. :-)

Role Variables
--------------

There are some variables in de default/main.yml which can (Or needs to) be changed/overriden:

* `zabbix_server_host`: The ip or dns name for the zabbix-server machine.

* `zabbix_server_port`: The port on which the zabbix-server is running. Default: 10051

* `zabbix_version`: This is the version of zabbix. Default it is 2.4, but can be overriden to 2.2 or 2.0.

* `zabbix_repo`: True / False. When you already have an repository with the zabbix components, you can set it to False.

There are some zabbix-proxy specific variables which will be used for the zabbix-proxy configuration file, these can be found in the default/main.yml file. There are 2 which needs some explanation:
```bash
  #database_type: mysql
  #database_type_long: mysql
  database_type: pgsql
  database_type_long: postgresql
```

There are 2 database_types which will be supported: mysql and postgresql. You'll need to comment or uncomment the database you would like to use. In example from above, the postgresql database is used. If you want to use mysql, uncomment the 2 lines from mysql and comment the 2 lines for postgresql.

Dependencies
------------

```text
You'll need to find the correct database role by yourself. I only want to use roles which supports the 3 main operating systems as well and for now I can't find one. If there is an role which supports these 3 operating systems, please let me know and I'll use it as dependency.
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: zabbix-proxy
      sudo: yes
      roles:
         - { role: dj-wasabi.zabbix-proxy, zabbix_server_host: 192.168.1.1, database_type: pgsql, database_type_long: postgresql }

License
-------

GPLv3

Author Information
------------------

This is my first attempt to create an ansible role, so please send suggestion or pull requests to make this role better. 

Github: https://github.com/dj-wasabi/ansible-zabbix-proxy

mail: ikben [ at ] werner-dijkerman . nl
