require 'serverspec'
require 'spec_helper'

describe 'Zabbix proxy Packages' do
    describe package('zabbix-proxy-mysql') do
        it { should be_installed }
    end
    describe package('zabbix-proxy') do
        it { should be_installed }
    end
    describe package('mysql') do
        it { should be_installed }
    end
end

describe 'Zabbix proxy Services' do
    describe service('zabbix-proxy') do
        it { should be_enabled }
        it { should be_running }
    end

    describe port(10051) do
        it { should be_listening }
    end
end

describe 'Zabbix proxy Configuration' do
    describe file('/etc/zabbix/zabbix_proxy.conf') do
        it { should be_file}
        it { should be_owned_by 'zabbix'}
        it { should be_grouped_into 'zabbix'}

        it { should contain "ListenPort=10051" }
        it { should contain "DBHost=localhost" }
        it { should contain "DBName=zabbix_proxy" }
        it { should contain "DBUser=zabbix_proxy" }
        it { should contain "DBPassword=zabbix_proxy" }
    end
end
