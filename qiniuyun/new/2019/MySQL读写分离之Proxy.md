---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-24 00:00:40
description: ：实现步骤：主备复制安装并配置测试一、主备复制略二、安装并配置安装并配置启动指定服务器工作的地址和端口指定写服务器的地址和端口指定读服务器的地址和端口指定判断的脚本以后台进程的方式启动调整最大打开的文。。。。。。。
image: http://image.ownit.top/4kdongman/31.jpg
tags:
- 技术记录
title: MySQL读写分离之Proxy
---

<!--more-->

  
**MySQL Proxy：**  
\========================================================  
  
![](http://image.ownit.top/csdn/20190423235746381.png)  
  
MySQL\_Proxy Master Slave1 Slave2  
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝=  
IP 192.168.1.250                   192.168.1.215                     192.168.1.66  
Server\_ID  6                         215                                        66  
  
实现步骤：  
MySQL主/备复制  
安装并配置MySQL Proxy  
测试Proxy  
  
  
一、MySQL主/备复制（略）  
  
  
二、安装并配置MySQL Proxy  
1\. 安装并配置

```
[root@MySQL_Proxy ~]# service mysqld stop
[root@MySQL_Proxy ~]# chkconfig mysqld off
[root@MySQL_Proxy ~]# rpm -qa |grep lua
lua-5.1.4-4.1.el6.x86_64
[root@MySQL_Proxy ~]# tar xf mysql-proxy-0.8.4-linux-el6-x86-64bit.tar.gz -C /usr/local/
[root@MySQL_Proxy ~]# cd /usr/local/
[root@MySQL_Proxy ~]# ln -s mysql-proxy-0.8.4-linux-el6-x86-64bit mysql-proxy
[root@MySQL_Proxy ~]# vim /usr/local/mysql-proxy/share/doc/mysql-proxy/rw-splitting.lua
min_idle_connections = 1,
max_idle_connections = 1,
```

  
  
2\. 启动mysql-proxy

```
[root@MySQL_Proxy ~]# lsof -i TCP:3306
[root@MySQL_Proxy ~]# /usr/local/mysql-proxy/bin/mysql-proxy --help-proxy
```

  
\-P 指定proxy服务器工作的地址和端口  
\-b 指定写服务器的地址和端口  
\-r 指定读服务器的地址和端口  
\-s 指定判断的脚本  
\--daemon 以后台进程的方式启动  
  
调整最大打开的文件数

```
[root@MySQL_Proxy ~]# ulimit -a |grep 'open files'
[root@MySQL_Proxy ~]# ulimit -n 10240
[root@MySQL_Proxy ~]# ulimit -a |grep 'open files'
open files (-n) 10240
```

  
 

```
[root@MySQL_Proxy ~]# /usr/local/mysql-proxy/bin/mysql-proxy -P 192.168.1.250:3306 -b 192.168.1.27:3306 -r 192.168.1.215:3306 -r 192.168.1.66:3306 -s /usr/local/mysql-proxy/share/doc/mysql-proxy/rw-splitting.lua --daemon
2014-02-13 17:15:54: (critical) plugin proxy 0.8.4 started
```

  
 

```
[root@MySQL_Proxy ~]# netstat -tnlp |grep :3306
tcp 0 0 192.168.10.137:3306 0.0.0.0:* LISTEN 16620/mysql-proxy
```

  
 

```
[root@MySQL_Proxy ~]# vim /etc/rc.local
ulimit -n 10240
/usr/local/mysql-proxy/bin/mysql-proxy -P 192.168.1.250:3306 -b 192.168.1.27:3306 -r 192.168.1.215:3306 -r 192.168.1.66:3306 -s /usr/local/mysql-proxy/share/doc/mysql-proxy/rw-splitting.lua --daemon
```

  
  
  
三、测试  
1\. 主库

```
mysql> grant ALL on bbs.* to bbs@'192.168.1.%' identified by 'localhost';
mysql> flush privileges;

mysql> create database bbs;
mysql> create table bbs.t1 (name varchar(50));
```

  
  
2\. 备库  
mysql> stop slave; //暂时断掉和主库的连接  
  
3\. 从客户端测试  
a. 读 ====主 or 备  
b. 写 ====主  
  
4\. 备库  
mysql> start slave;  
\=======================================================