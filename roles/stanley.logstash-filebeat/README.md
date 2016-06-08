# Ansible Role: Logstash Forwarder

[![Build Status](https://travis-ci.org/geerlingguy/ansible-role-filebeat.svg?branch=master)](https://travis-ci.org/geerlingguy/ansible-role-filebeat)

An Ansible Role that installs Logstash Forwarder on RedHat/CentOS or Debian/Ubuntu.

**Note**: This role is well-tested on Debian/Ubuntu, but is still undergoing development for RedHat/CentOS. You've been warned!

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    filebeat_logstash_server: localhost
    filebeat_logstash_server_port: 5000

The central Logstash server/port to which filebeat should connect.

    logstash_ssl_dir: /etc/pki/logstash
    filebeat_ssl_certificate_file: filebeat-example.crt

The location and filename of the SSL certificate filebeat will use to authenticate to the logstash server. For the `filebeat_ssl_certificate_file`, you can provide a path relative to the role directory, or an absolute path to the file.

    filebeat_files:
      - paths:
          - /var/log/messages
          - /var/log/auth.log
        fields:
          type: syslog

Configuration of files monitored by filebeat. You can add more sets of files by adding to the list with another set of files; see `defaults/main.yml` for an example.

## Dependencies

None.

## Example Playbook

    - hosts: all
      roles:
        - { role: geerlingguy.filebeat }

## License

MIT / BSD

## Author Information

This role was created in 2014 by [Jeff Geerling](http://jeffgeerling.com/), author of [Ansible for DevOps](http://ansiblefordevops.com/).
