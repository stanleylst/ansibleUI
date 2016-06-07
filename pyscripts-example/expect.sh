#!/usr/bin/expect

#设置要连接的远程主机IP信息
set IP     [ lindex $argv 0 ] 
#设置要连接的远程主机登录用户
set USER   [ lindex $argv 1 ] 
#设置要连接的远程主机登录用户的密码信息
set PASSWD [ lindex $argv 2 ] 
#设置要执行的命令
set CMD    [ lindex $argv 3 ] 
 
#spawn是expect内部命令，开启ssh连接
spawn ssh $USER@$IP $CMD    
#判断上次执行结果
expect {                    
    #如果有yes或no关键字，
    "(yes/no)?" {           
        #则输入yes
        send "yes\r"        
        #输入完yes后如果输出结果有： password: 关键字，
        expect "password:"  
        #则输入密码文件
        send "$PASSWD\r"    
        }
    #如果上次输出结果有：password: ,则输入密码
    "password:" {send "$PASSWD\r"}  
    #如果上次输出结果有：* to host ,则退出
    "* to host" {exit 1}            
    }
expect eof
