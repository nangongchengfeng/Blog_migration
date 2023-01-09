+++
author = "南宫乘风"
title = "MySQL读写分离之Proxy"
date = "2019-04-24 00:00:40"
tags=[]
categories=['MySQL']
image = "post/4kdongman/16.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89484004](https://blog.csdn.net/heian_99/article/details/89484004)

<br>**MySQL Proxy：**<br> ========================================================<br><br>![20190423235746381.png](https://img-blog.csdnimg.cn/20190423235746381.png)<br><br> MySQL_Proxy Master Slave1 Slave2<br> ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝=<br> IP 192.168.1.250                   192.168.1.215                     192.168.1.66<br> Server_ID  6                         215                                        66<br><br> 实现步骤：<br> MySQL主/备复制<br> 安装并配置MySQL Proxy<br> 测试Proxy<br><br><br> 一、MySQL主/备复制（略）<br><br><br> 二、安装并配置MySQL Proxy<br> 1. 安装并配置

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

<br><br> 2. 启动mysql-proxy

```
[root@MySQL_Proxy ~]# lsof -i TCP:3306
[root@MySQL_Proxy ~]# /usr/local/mysql-proxy/bin/mysql-proxy --help-proxy
```

<br> -P 指定proxy服务器工作的地址和端口<br> -b 指定写服务器的地址和端口<br> -r 指定读服务器的地址和端口<br> -s 指定判断的脚本<br> --daemon 以后台进程的方式启动<br><br> 调整最大打开的文件数

```
[root@MySQL_Proxy ~]# ulimit -a |grep 'open files'
[root@MySQL_Proxy ~]# ulimit -n 10240
[root@MySQL_Proxy ~]# ulimit -a |grep 'open files'
open files (-n) 10240
```

<br>  

```
[root@MySQL_Proxy ~]# /usr/local/mysql-proxy/bin/mysql-proxy -P 192.168.1.250:3306 -b 192.168.1.27:3306 -r 192.168.1.215:3306 -r 192.168.1.66:3306 -s /usr/local/mysql-proxy/share/doc/mysql-proxy/rw-splitting.lua --daemon
2014-02-13 17:15:54: (critical) plugin proxy 0.8.4 started
```

<br>  

```
[root@MySQL_Proxy ~]# netstat -tnlp |grep :3306
tcp 0 0 192.168.10.137:3306 0.0.0.0:* LISTEN 16620/mysql-proxy
```

<br>  

```
[root@MySQL_Proxy ~]# vim /etc/rc.local
ulimit -n 10240
/usr/local/mysql-proxy/bin/mysql-proxy -P 192.168.1.250:3306 -b 192.168.1.27:3306 -r 192.168.1.215:3306 -r 192.168.1.66:3306 -s /usr/local/mysql-proxy/share/doc/mysql-proxy/rw-splitting.lua --daemon
```

<br><br><br> 三、测试<br> 1. 主库

```
mysql&gt; grant ALL on bbs.* to bbs@'192.168.1.%' identified by 'localhost';
mysql&gt; flush privileges;

mysql&gt; create database bbs;
mysql&gt; create table bbs.t1 (name varchar(50));
```

<br><br> 2. 备库<br> mysql&gt; stop slave; //暂时断掉和主库的连接<br><br> 3. 从客户端测试<br> a. 读 ====主 or 备<br> b. 写 ====主<br><br> 4. 备库<br> mysql&gt; start slave;<br> =======================================================
