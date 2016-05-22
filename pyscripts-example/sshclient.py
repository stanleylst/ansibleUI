#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko  

def sshe(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        print stdout.read()
        print "%s\tOK\n"%(ip)
        ssh.close()
    except :
        print "%s\tError\n"%(ip)

sshe("192.168.37.142","linuxlst","redhat","hostname;ifconfig")

