#!/bin/env  python
#function: upload files throuth ssh protocal and excute command
#-*- conding = utf-8 -*-

import paramiko
import sys
import threading
import os
import re
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep,ctime


MULTI_PROC = 2  #process
pool = ThreadPool(MULTI_PROC)

def Usage():
    print '*' * 50
    print '''
Usage: 
     mabs.py command iplist

*****cat command*****
com:::ls /home/linuxlst/datafile/songtaoli/
file:::/home/linuxlst/pylear/paramiko/sftp/sftp_v2.py /home/linuxlst/sftp_v2.py put

*****cat iplist*****
192.168.37.142 linuxlst redhat 22
    '''
    print '*' * 50

def FileUsage():
    print "Usage:"
    print "    file:::/home/linuxlst/pylear/paramiko/sftp/sftp_v2.py /home/linuxlst/sftp_v2.py put"


def FileTran(comm,TranType,hostname,username,pwd,port):
    try:
        #print 'hostname:',hostname
        #print 'port:',port
        t = paramiko.Transport((hostname,int(port)))
        t.connect(username=username,password=pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        filetran = comm.split(' ')
        local = filetran[0].strip('\n')
        remote = filetran[1].strip('\n')
        if TranType == "put":
            #print '***put file %s to remote %s' % (local,remote)
            sftp.put(local,remote)
        elif TranType == "get":
            #print '***get remote file %s to local %s' % (remote,local)
            sftp.get(remote,local)
        else:
            print "ERROR:lack of tran TranType."
            sys.exit()
        t.close()
    except Exception, e:
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
 
def Execu(hostname,username,pwd,port,command):
    try:
        #print '***Run command {%s} on host {%s} by username {%s}' % (command,hostname,username)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        #ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname,port=int(port),username=username,password=pwd)
        stdin,stdout,stderr = ssh.exec_command(command)
        #stdin,stdout,stderr = ssh.exec_command('hostname')
        #print stdin.read()
        print stdout.read()
        print stderr.read()
    except Exception,e:
        print 'change file auth or excute file failed:',e
    ssh.close()

def main(config):
    ip = config[0]
    username = config[1]
    pwd = config[2]
    port = config[3]
    comm = config[4]
    print ip,username,pwd,port,comm
    maincomm = [] 
    TranType = ''
    sp = comm.split(':::')
    if sp[0] == "com":
        #maincomm = [sp[1].strip('\n'),'com']
        commandline = sp[1].strip('\n')
        Execu(ip,username,pwd,port,commandline)  
    elif sp[0] == "file":
        m = sp[1].strip('\n')
        if re.search('put',m):
            TranType = 'put'
            #maincomm = [sp[1].strip('\n'),TranType]
            commandline = sp[1].strip('\n')
            FileTran(commandline,TranType,ip,username,pwd,port)
        elif re.search('get',m):
            TranType = 'get'
            #maincomm = [sp[1].strip('\n'),TranType]
            commandline = sp[1].strip('\n')
            FileTran(commandline,TranType,ip,username,pwd,port)
        else:
            print 'ERROR:lack of tran TranType'
            FileUsage()
            sys.exit()
    else:
        print 'ERROR:lack com or file mark'
        FileUsage()
        sys.exit()   


def MyMul():
    threads = []
    com = open(sys.argv[1],'r')  #command file
    confs  = open(sys.argv[2],'r')  #config file
    confs.seek(0)
    config = []
    for conf in confs:
        com.seek(0)
        #print ip,username,port
        if not conf.startswith('#') and len(conf) > 1:
            ip,username,pwd,port = conf.strip('\r\n').split(' ')
            #lconf += 1
            for comm in com:
                if not comm.startswith('#') and len(comm) > 1:
                    config.append([ip,username,pwd,port,comm])

    pool.map(main,config)
    pool.close()
    pool.join()

if len(sys.argv) != 3:
    Usage()
    os.sys.exit()

if __name__ == '__main__':
    MyMul()
