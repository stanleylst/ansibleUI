# Ansible Role: Elasticsearch Curator

[![Build Status](https://travis-ci.org/geerlingguy/ansible-role-elasticsearch-curator.svg?branch=master)](https://travis-ci.org/geerlingguy/ansible-role-elasticsearch-curator)

An Ansible Role that installs [Elasticsearch Curator](https://github.com/elasticsearch/curator) on RedHat/CentOS or Debian/Ubuntu.

## Requirements

None, but it's a lot more helpful if you have Elasticsearch running somewhere :)

On RedHat/CentOS, make sure you have the EPEL repository configured, so the `python-pip` package can be installed. You can install the EPEL repo by simply adding `geerlingguy.repo-epel` to your playbook's roles.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    elasticsearch_curator_cron_jobs:
      - {
        name: "Delete old elasticsearch indices.",
        job: "/usr/local/bin/curator delete --older-than 30",
        minute: "0",
        hour: "1"
      }
      - {
        name: "Close old elasticsearch indices.",
        job: "/usr/local/bin/curator close --older-than 14",
        minute: "30",
        hour: "1"
      }

A list of cron jobs to use curator to prune, optimize, close, and otherwise maintain your Elasticsearch indexes. If you're connecting to an Elasticsearch server on a different host/port than `localhost` and `9200`, you need to add `--host [hostname]` and/or `--port [port]` to the jobs. More documentation is available on the [Elasticsearch Curator wiki](https://github.com/elasticsearch/curator/wiki/Examples). You can add any of `minute`, `hour`, `day`, `weekday`, and `month` to the cron jobs—values that are not explicitly set will default to `*`.

## Dependencies

  - geerlingguy.repo-epel (RedHat/CentOS only)

## Example Playbook

    - hosts: search
      roles:
        - { role: geerlingguy.elasticsearch-curator }

## License

MIT / BSD

## Author Information

This role was created in 2014 by [Jeff Geerling](http://jeffgeerling.com/), author of [Ansible for DevOps](http://ansiblefordevops.com/).
