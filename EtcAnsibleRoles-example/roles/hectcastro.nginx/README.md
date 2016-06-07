# ansible-nginx

An Ansible role for Nginx as a reverse proxy.

## Role Variables

- `nginx_site_name` - Site name for the reverse proxy configuration
- `nginx_site_server_name` - Server name for the site configuration
- `nginx_site_proxy_pass_scheme` - Scheme for the `proxy_pass` setting
- `nginx_site_proxy_pass_host` Host for the `proxy_pass` setting
- `nginx_site_proxy_pass_port` Port for the `proxy_pass` setting

## Example Playbook

See the [examples](./examples/) directory.
