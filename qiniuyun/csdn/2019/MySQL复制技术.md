---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-22 22:17:01
description: 高可用方案投票选举机制，较复杂本身没有提供的解决方案，自动切换需要依赖脚本可以有多台从库，从库可以做报表和备份复制技术重置数据库：复制拓扑：复制原理：在主库上把数据更改记录到二进制日志中。备库将主库上。。。。。。。
image: ../../title_pic/40.jpg
slug: '201904222217'
tags:
- 技术记录
title: MySQL复制技术
---

<!--more-->

MySQL高可用方案

![](../../image/20190422213949323.png)

投票选举机制，较复杂  
MySQL本身没有提供replication failover的解决方案，自动切换需要依赖[MHA脚本](http://os.51cto.com/art/201307/401702.htm)  
可以有多台从库，从库可以做报表和备份

![](../../image/20190422214023814.png)

![](../../image/20190422214041808.png)

![](../../image/20190422214117224.png)

![](../../image/20190422214128620.png)

![](../../image/201904222141421.png)

![](../../image/20190422214211319.png)

**MySQL复制技术**  
  
  
  
\===========================================================================  
重置数据库：

```
# service mysqld stop
# rm -rf /usr/local/mysql/data/*
# /usr/local/mysql/scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data
```

  
 

## 复制拓扑：

![](../../image/20190422214313244.png)

![](../../image/20190422214332500.png)

## 复制原理：

![](../../image/20190422214350321.png)

## 1\. 在主库上把数据更改记录到二进制日志（Binary Log）中。  
2\. 备库将主库上的日志复制到自己的中继日志（Relay Log）中。  
3\. 备库读取中继日志中的事件，将其重放到备库数据库之上。

![](../../image/20190422214418640.png)

一、主/备均为刚初始的数据库  
单主到多备： Master-MultiSlave  
Master                        Slave1                        Slave2  
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝  
IP 192.168.1.27          192.168.1.66             192.168.1.251  
Server\_ID  27               66                             251  
  
  
如何实现主从复制？  
在主服务器（master）上  
启用二进制日志  
选择一个唯一的server-id  
创建具有复制权限的用户  
在从服务器（slave）上  
启用中继日志（二进制日志可开启，也可不开启）  
选择一个唯一的server-id  
连接至主服务器，并开始复制  
1\. 主库

```
[root@master ~]# vim /etc/my.cnf
[mysqld]
log-bin=master-bin
binlog_format = row
sync_binlog = 1
skip_name_resolv = 1
log_slave_updates = 1
server_id = 27
[root@master ~]# service mysqld start
[root@master ~]# mysql
mysql> reset master;
mysql> grant replication slave, replication client on *.*
-> to rep@'192.168.1.%' identified by 'localhost';
mysql> flush privileges;
```

  
2\. 备库  
a. 测试复制账号

```
[root@slave1 ~]# mysql -h 192.168.1.27 -urep -plocalhost
```

  
b. 配置复制

```
[root@slave1 ~]# vim /etc/my.cnf
log-bin=slave1-bin
binlog_format = row
sync_binlog = 1
skip_name_resolv = 1
log_slave_updates = 1
server_id = 66
[root@slave1 ~]# service mysqld start
[root@slave1 ~]# mysql
mysql> reset master;
mysql> change master to
-> master_host='192.168.1.27',
-> master_user='rep',
-> master_password='localhost',
-> master_log_file='master-bin.000001',
-> master_log_pos=0;
Query OK, 0 rows affected (0.02 sec)

mysql> show slave status\G
*************************** 1. row ***************************
Slave_IO_State:
Master_Host: 192.168.1.27
Master_User: rep
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.000001
Read_Master_Log_Pos: 4
Relay_Log_File: mysql-relay-bin.000001
Relay_Log_Pos: 4
Relay_Master_Log_File: mysql-bin.000001
Slave_IO_Running: No
Slave_SQL_Running: No

mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

mysql> show slave status\G
*************************** 1. row ***************************
Slave_IO_State: Waiting for master to send event
Master_Host: 192.168.1.27
Master_User: rep
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.000001
Read_Master_Log_Pos: 354
Relay_Log_File: mysql-relay-bin.000002
Relay_Log_Pos: 500
Relay_Master_Log_File: mysql-bin.000001
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

  
3\. 测试

```
Master：
mysql> show processlist\G
*************************** 2. row ***************************
Id: 2
User: rep
Host: 192.168.10.37:50915
db: NULL
Command: Binlog Dump
Time: 324
State: Master has sent all binlog to slave; waiting for binlog to be updated
Info: NULL
2 rows in set (0.00 sec)

mysql> create database bbs;
Query OK, 1 row affected (0.00 sec)

mysql> create table bbs.t1(id int);
Query OK, 0 rows affected (0.03 sec)

mysql> insert into bbs.t1 values(1);
Query OK, 1 row affected (0.02 sec)
mysql> select * from bbs.t1;
+------+
| id |
+------+
| 1 |
+------+
1 row in set (0.00 sec)

Slave：
mysql> show processlist\G
*************************** 2. row ***************************
Id: 2
User: system user
Host:
db: NULL
Command: Connect
Time: 356
State: Waiting for master to send event
Info: NULL
*************************** 3. row ***************************
Id: 3
User: system user
Host:
db: NULL
Command: Connect
Time: -173772
State: Slave has read all relay log; waiting for the slave I/O thread to update it
Info: NULL
3 rows in set (0.00 sec)

mysql> select * from bbs.t1;
+------+
| id |
+------+
| 1 |
+------+
1 row in set (0.03 sec)
```

  
  
  
  
二、针对已经运行一段时间的主库实现主/备  
单主到多备： Master-MultiSlave  
Master                       Slave1                             Slave2  
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝  
IP 192.168.1.27          192.168.1.66                 192.168.1.251  
Server\_ID   27            66                                   251  
  
  
1\. 主库

```
[root@master ~]# vim /etc/my.cnf
log-bin=master-bin
binlog_format = row
sync_binlog = 1
skip_name_resolv = 1
log_slave_updates = 1
server_id = 27
[root@master ~]# service mysqld restart
[root@master ~]# mysql
mysql> grant replication slave, replication client on *.*
-> to rep@'192.168.1.%' identified by 'localhost';
mysql> flush privileges;
```

  
\========================================================  
初始化备库（使其和主库数据一致）： 逻辑备份，物理备份  
主库：

```
mysql> flush tables with read lock; //主服务器锁定表
[root@master ~]# mysqldump --all-databases > all.sql
[root@master ~]# mysql -e 'show master status'
+------------------+----------+--------------+------------------+
| File | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| master-bin.000001 | 699 | | |
+------------------+----------+--------------+------------------+
mysql> unlock tables; //解锁表
[root@master ~]# rsync -va all.sql 192.168.1.66:/
```

  
\========================================================  
  
  
2\. 备库

```
[root@slave1 ~]# vim /etc/my.cnf
server-id = 66
[root@slave1 ~]# service mysqld start
[root@slave1 ~]# mysql
mysql> reset master;
mysql> source /all.sql

mysql> change master to
master_host='192.168.1.27',
master_user='rep',
master_password='localhost',
master_log_file='master-bin.000001',
master_log_pos=699;
Query OK, 0 rows affected (0.02 sec)

mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

mysql> show slave status\G
*************************** 1. row ***************************
Slave_IO_State: Waiting for master to send event
Master_Host: 192.168.1.27
Master_User: rep
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: master-bin.000001
Read_Master_Log_Pos: 354
Relay_Log_File: mysql-relay-bin.000002
Relay_Log_Pos: 500
Relay_Master_Log_File: mysql-bin.000001
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

  
MySQL主从复制的状况监测  
主从状况监测主要参数  
Slave\_IO\_Running: IO线程是否打开 YES/No/NULL  
Slave\_SQL\_Running: SQL线程是否打开 YES/No/NULL  
Seconds\_Behind\_Master: NULL #和主库比同步的延迟的秒数  
  
可能导致主从延时的因素  
主从时钟是否一致  
网络通信是否存在延迟  
是否和日志类型，数据过大有关  
从库性能，有没开启binlog  
从库查询是否优化  
  
常见状态错误排除  
发现IO进程错误，检查日志，排除故障：  
\# tail localhost.localdomain.err  
...2015-11-18 10:55:50 3566 \[ERROR\] Slave I/O: Fatal error: The slave I/O thread stops because master and slave have equal MySQL server UUIDs; these UUIDs must be different for replication to work. Error\_code: 1593  
找到原因：从5.6开始复制引入了uuid的概念，各个复制结构中的server\_uuid得保证不一样  
解决方法：\(从库是克隆机器\)修改从库的uuid  
\# vim auto.cnf server-uuid=  
  
show slave status;报错：Error xxx doesn’t exist  
解决方法：  
stop slave;  
set global sql\_slave\_skip\_counter = 1;  
start slave;  
三、常见复制拓朴  
1\. 一主库多备库  
2\. 主库，分发主库以及备库  
3\. 主——主复制（双主）  
  
  
  
四、MySQL 主主同步  
重置数据库：

```
# service mysqld stop
# rm -rf /usr/local/mysql/data/*
# /usr/local/mysql/scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data
```

  
1\. mysql1 192.168.1.4:

```
[root@mysql1 ~]# vim /etc/my.cnf
log-bin=mysql-bin
server-id = 4
[root@mysql1 ~]# service mysqld start
[root@mysql1 ~]# mysql
mysql> reset master;
mysql> grant replication slave, replication client on *.*
-> to rep@'192.168.1.%' identified by 'localhost';
mysql> flush privileges;
mysql> change master to
-> master_host='192.168.1.251',
-> master_user='rep',
-> master_password='localhost',
-> master_log_file='mysql-bin.000001',
-> master_log_pos=0;
Query OK, 0 rows affected (0.02 sec)
mysql> show slave status\G
```

  
  
2\. mysql2 192.168.1.251:

```
[root@mysql2 ~]# vim /etc/my.cnf
log-bin=mysql-bin
server-id = 251
[root@mysql2 ~]# service mysqld start
[root@mysql2 ~]# mysql
mysql> reset master;
mysql> grant replication slave, replication client on *.*
-> to rep@'192.168.1.%' identified by 'localhost';
mysql> flush privileges;
mysql> change master to
-> master_host='192.168.1.4',
-> master_user='rep',
-> master_password='localhost',
-> master_log_file='mysql-bin.000001',
-> master_log_pos=0;
Query OK, 0 rows affected (0.02 sec)
mysql> show slave status\G
```

  
3\. mysql1,mysql2

```
mysql> slave start;
mysql> show slave status\G
```

  
  
4\. 测试  
  
5\. 建立用于客户连接用户

```
mysql> grant ALL on *.* to admin@'192.168.1.%' identified by 'localhost';
mysql> flush privileges;
```

  
\===========================================================================  
  
生产环境其他常用设置  
1、配置忽略权限库同步参数  
binlog-ignore-db='information\_schema mysql test'  
2、从库备份开启binlog  
log-slave-updates  
log\_bin = mysql-bin  
expire\_logs\_days = 7  
应用场景：级联复制或从库做数据备份。  
3、从库只读read-only来实现  
innodb\_read\_only = ON或1，或者innodb\_read\_only  
结论：当用户权限中没有SUPER权限\(ALL权限是包括SUPER的\)时，从库的read-only生效！