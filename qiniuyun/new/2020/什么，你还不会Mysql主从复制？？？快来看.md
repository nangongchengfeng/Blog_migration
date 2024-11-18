---
author: 南宫乘风
categories:
- MySQL
date: 2020-06-09 17:35:28
description: 目录、为什么需要主从复制？、什么是主从复制、复制原理、主从复制简介、延时从库、半同步复制、过滤复制、复制主从故障监控分析处理主从故障监控分析处理主从复制故障分析、为什么需要主从复制？、在业务复杂的系统。。。。。。。
image: http://image.ownit.top/4kdongman/51.jpg
tags:
- 数据库
- linux
- mysql
- 主从同步
- GTID
title: 什么，你还不会Mysql主从复制？？？快来看
---

<!--more-->

**目录**

[1、为什么需要主从复制？](#1%E3%80%81%E4%B8%BA%E4%BB%80%E4%B9%88%E9%9C%80%E8%A6%81%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6%EF%BC%9F)

[2、什么是mysql主从复制](#2%E3%80%81%E4%BB%80%E4%B9%88%E6%98%AFmysql%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6)

[3、Mysql复制原理](#3%E3%80%81Mysql%E5%A4%8D%E5%88%B6%E5%8E%9F%E7%90%86)

[4、主从复制简介](#4%E3%80%81%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6%E7%AE%80%E4%BB%8B)

[5、 延时从库](#5%E3%80%81%C2%A0%E5%BB%B6%E6%97%B6%E4%BB%8E%E5%BA%93)

[6、半同步复制](#6%E3%80%81%E5%8D%8A%E5%90%8C%E6%AD%A5%E5%A4%8D%E5%88%B6)

[7、过滤复制](#7%E3%80%81%E8%BF%87%E6%BB%A4%E5%A4%8D%E5%88%B6)

[8、GTID复制](#8%E3%80%81GTID%E5%A4%8D%E5%88%B6)

[9\. 主从故障监控\\分析\\处理](<#9. 主从故障监控\分析\处理>)

[主从复制故障分析](#%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6%E6%95%85%E9%9A%9C%E5%88%86%E6%9E%90)

---

### ![](http://image.ownit.top/csdn/20200609163414418.png)

### 1、**为什么需要主从复制？**

1、在业务复杂的系统中，有这么一个情景，有一句sql语句需要锁表，导致暂时不能使用读的服务，那么就很影响运行中的业务，使用主从复制，让主库负责写，从库负责读，这样，即使主库出现了锁表的情景，通过读从库也可以保证业务的正常运作。

2、做数据的热备

3、架构的扩展。业务量越来越大，I/O访问频率过高，单机无法满足，此时做多库的存储，降低磁盘I/O访问的频率，提高单个机器的I/O性能。

### 2、什么是mysql主从复制

Mysql主从复制是指数据可以从一个mysql数据库服务器节点复制到另一个或者多个节点。

Mysql默认采用异步复制方式，这样从节点不用一直访问主服务器来跟新自己的数据，数据的更新可以在远程连接上进行，从节点可以复制主数据库中的所有数据库或者特定的数据库，或者特定的表。

### 3、Mysql复制原理

**原理：**

**（1）master服务器将数据的改变记录二进制binlog日志，当master的数据发生改变是，这将改变写入二进制日志中；**

**（2）slave服务器会在一定时间间隔内对master二进制日志进行探测是否发生改变，如果发生改变，则开始一个IO线程请求master二进制时间**

**（3）同时主节点为每个IO线程启动一个dump线程，用于向其发送二进制事件，并保存至从节点本地的中继日志中，从节点将启动sql线程从中继日志读取二进制日志，在本地重放，使得其数据和主节点的保持一致，最后IO线程和sql线程进入睡眠状态，等待下一次唤醒**

> - **从库会生成两个线程,一个I/O线程,一个SQL线程;**
> - **I/O线程会去请求主库的binlog,并将得到的binlog写到本地的relay-log\(中继日志\)文件中;**
> - **主库会生成一个log dump线程,用来给从库I/O线程传binlog;**
> - **SQL线程,会读取relay log文件中的日志,并解析成sql语句逐一执行;**

**注意：**

1、master将操作语句记录到binlog日志中，然后授予slave远程连接的权限（master一定要开启binlog二进制日志功能；通常为了数据安全考虑，slave也开启binlog功能）。

2、slave开启两个线程：IO线程和SQL线程。其中：IO线程负责读取master的binlog内容到中继日志relay log里；SQL线程负责从relay log日志里读出binlog内容，并更新到slave的数据库里，这样就能保证slave数据和master数据保持一致了。

3、Mysql复制至少需要两个Mysql的服务，当然Mysql服务可以分布在不同的服务器上，也可以在一台服务器上启动多个服务。

4、Mysql复制最好确保master和slave服务器上的Mysql版本相同（如果不能满足版本一致，那么要保证master主节点的版本低于slave从节点的版本）

5、master和slave两节点间时间需同步

### 4、主从复制简介

> 1.1. 基于二进制日志复制的  
> 1.2. 主库的修改操作会记录二进制日志  
> 1.3. 从库会请求新的二进制日志并回放,最终达到主从数据同步  
> 1.4. 主从复制核心功能:  
> 辅助备份,处理物理损坏                     
> 扩展新型的架构:高可用,高性能,分布式架构等

**前提**

- 2.1 两台以上mysql实例 ,server\_id,server\_uuid不同
- 2.2 主库开启二进制日志
-  2.3 专用的复制用户
- 2.4 保证主从开启之前的某个时间点,从库数据是和主库一致\(补课\)
- 2.5 告知从库,复制user,passwd,IP port,以及复制起点\(change master to\)
- 2.6 线程\(三个\):Dump thread  IO thread  SQL thread 开启\(start slave\)

**主从复制搭建过程**

**清理主库数据**

```bash
rm -rf /data/3307/data/*
```

**重新初始化3307**

```bash
mysqld --initialize-insecure --user=mysql --basedir=/app/mysql --datadir=/data/3307/data
```

**修改my.cnf ,开启二进制日志功能**

```bash
[root@db01 3307]# vim /data/3307/my.cnf 
log_bin=/data/3307/data/mysql-bin
```

**启动所有节点**

```bash
[root@db01 3307]# systemctl start mysqld3307
[root@db01 3307]# systemctl start mysqld3308
[root@db01 3307]# systemctl start mysqld3309
[root@db01 3307]# ps -ef |grep mysqld
mysql      3684      1  4 09:59 ?        00:00:00 /app/mysql/bin/mysqld --defaults-file=/data/3307/my.cnf
mysql      3719      1  7 09:59 ?        00:00:00 /app/mysql/bin/mysqld --defaults-file=/data/3308/my.cnf
mysql      3754      1  8 09:59 ?        00:00:00 /app/mysql/bin/mysqld --defaults-file=/data/3309/my.cnf
[root@db01 3307]# mysql -S /data/3307/mysql.sock -e "select @@server_id"
[root@db01 3307]# mysql -S /data/3308/mysql.sock -e "select @@server_id"
[root@db01 3307]# mysql -S /data/3309/mysql.sock -e "select @@server_id"
```

**主库中创建复制用户**

```bash
[root@db01 3307]# mysql -S /data/3307/mysql.sock 
db01 [(none)]>grant replication slave on *.* to repl@'10.0.0.%' identified by '123';
db01 [(none)]>select user,host from mysql.user;
```

**备份主库并恢复到从库**

```bash
[root@db01 3307]# mysqldump -S /data/3307/mysql.sock -A --master-data=2 --single-transaction  -R --triggers >/backup/full.sql
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=653;
[root@db01 3307]# mysql -S /data/3308/mysql.sock
db01 [(none)]>source /backup/full.sql
```

**告知从库关键复制信息**

```
ip port user  password  binlog position 
[root@db01 3307]# mysql -S /data/3308/mysql.sock
db01 [mysql]>help change master to

CHANGE MASTER TO
  MASTER_HOST='10.0.0.51',   #主库ip地址
  MASTER_USER='repl',        #复制用户
  MASTER_PASSWORD='123',     #密码
  MASTER_PORT=3307,          #端口
  MASTER_LOG_FILE='mysql-bin.000001', #复制binlog的起始位置
  MASTER_LOG_POS=653,        #起始位置的pos好
  MASTER_CONNECT_RETRY=10;   #尝试连接次数
```

**开启主从专用线程**

```
start slave ;
```

**检查复制状态**

```
db01 [mysql]>show slave  status \G
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

**主从复制原理描述：**

- 1.change master to 时，ip pot user password binlog position写入到master.info进行记录
- 2\. start slave 时，从库会启动IO线程和SQL线程
- 3.IO\_T，读取master.info信息，获取主库信息连接主库
- 4\. 主库会生成一个准备binlog DUMP线程，来响应从库
- 5\. IO\_T根据master.info记录的binlog文件名和position号，请求主库DUMP最新日志
- 6\. DUMP线程检查主库的binlog日志，如果有新的，TP\(传送\)给从从库的IO\_T
- 7\. IO\_T将收到的日志存储到了TCP/IP 缓存，立即返回ACK给主库 ，主库工作完成
- 8.IO\_T将缓存中的数据，存储到relay-log日志文件,更新master.info文件binlog 文件名和postion，IO\_T工作完成
- 9.SQL\_T读取relay-log.info文件，获取到上次执行到的relay-log的位置，作为起点，回放relay-log
- 10.SQL\_T回放完成之后，会更新relay-log.info文件。
- 11\. relay-log会有自动清理的功能。
- 细节：
- 1.主库一旦有新的日志生成，会发送“信号”给binlog dump ，IO线程再请求

### 5、 延时从库

是我们认为配置的一种特殊从库.人为配置从库和主库延时N小时.

**为什么要有延时从？**

```
数据库故障?
物理损坏
主从复制非常擅长解决物理损坏.
逻辑损坏
普通主从复制没办法解决逻辑损坏
```

配置延时从库

```
SQL线程延时:数据已经写入relaylog中了,SQL线程"慢点"运行
一般企业建议3-6小时,具体看公司运维人员对于故障的反应时间

mysql>stop slave;
mysql>CHANGE MASTER TO MASTER_DELAY = 300;
mysql>start slave;
mysql> show slave status \G
SQL_Delay: 300
SQL_Remaining_Delay: NULL
```

**延时从库应用**

>               1主1从,从库延时5分钟,主库误删除1个库  
> 1\. 5分钟之内 侦测到误删除操作  
> 2\. 停从库SQL线程  
> 3\. 截取relaylog  
> 起点 :停止SQL线程时,relay最后应用位置  
> 终点:误删除之前的position\(GTID\)  
> 4\. 恢复截取的日志到从库  
> 5\. 从库身份解除,替代主库工作

**故障模拟及恢复**

```
1.主库数据操作
db01 [(none)]>create database relay charset utf8;
db01 [(none)]>use relay
db01 [relay]>create table t1 (id int);
db01 [relay]>insert into t1 values(1);
db01 [relay]>drop database relay;
```

```
2. 停止从库SQL线程
stop slave sql_thread;
```

```
3. 找relaylog的截取起点和终点
起点:
Relay_Log_File: db01-relay-bin.000002
Relay_Log_Pos: 482
终点:
show relaylog events in 'db01-relay-bin.000002'
| db01-relay-bin.000002 | 1046 | Xid            |         7 |        2489 | COMMIT /* xid=144 */                  |
| db01-relay-bin.000002 | 1077 | Anonymous_Gtid |         7 |        2554 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
mysqlbinlog --start-position=482 --stop-position=1077  /data/3308/data/db01-relay-bin.000002>/tmp/relay.sql
```

```bash
4.从库恢复relaylog
source /tmp/relay.sql
```

```bash
5.从库身份解除
db01 [relay]>stop slave;
db01 [relay]>reset slave all
```

### 6、半同步复制

**解决主从数据一致性问题**

** 半同步复制工作原理的变化**

- 1\. 主库执行新的事务,commit时,更新 show master  status\\G ,触发一个信号给
- 2\. binlog dump 接收到主库的 show master status\\G信息,通知从库日志更新了
- 3\. 从库IO线程请求新的二进制日志事件
- 4\. 主库会通过dump线程传送新的日志事件,给从库IO线程
- 5\. 从库IO线程接收到binlog日志,当日志写入到磁盘上的relaylog文件时,给主库ACK\_receiver线程
- 6\. ACK\_receiver线程触发一个事件,告诉主库commit可以成功了
- 7\. 如果ACK达到了我们预设值的超时时间,半同步复制会切换为原始的异步复制.

**配置半同步复制**

```
加载插件
主:
INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';
从:
INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';
查看是否加载成功:
show plugins;
启动:
主:
SET GLOBAL rpl_semi_sync_master_enabled = 1;
从:
SET GLOBAL rpl_semi_sync_slave_enabled = 1;
重启从库上的IO线程
STOP SLAVE IO_THREAD;
START SLAVE IO_THREAD;
查看是否在运行
主:
show status like 'Rpl_semi_sync_master_status';
从:
show status like 'Rpl_semi_sync_slave_status';
```

### 7、过滤复制

主库：

```
show master status;
Binlog_Do_DB
Binlog_Ignore_DB 
```

从库：

```
show slave status\G
Replicate_Do_DB: 
Replicate_Ignore_DB: 
```

**实现过程**

```
mysqldump -S /data/3307/mysql.sock -A --master-data=2 --single-transaction  -R --triggers >/backup/full.sql

vim  /backup/full.sql
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000002', MASTER_LOG_POS=154;

[root@db01 ~]# mysql -S /data/3309/mysql.sock 
source /backup/full.sql

CHANGE MASTER TO
MASTER_HOST='10.0.0.51',
MASTER_USER='repl',
MASTER_PASSWORD='123',
MASTER_PORT=3307,
MASTER_LOG_FILE='mysql-bin.000002',
MASTER_LOG_POS=154,
MASTER_CONNECT_RETRY=10;
start  slave;
[root@db01 ~]# vim /data/3309/my.cnf 
replicate_do_db=ppt
replicate_do_db=word
[root@db01 ~]# systemctl restart mysqld3309

主库：
Master [(none)]>create database word;
Query OK, 1 row affected (0.00 sec)
Master [(none)]>create database ppt;
Query OK, 1 row affected (0.00 sec)
Master [(none)]>create database excel;
Query OK, 1 row affected (0.01 sec)
```

### 8、GTID复制

GTID介绍

```
GTID(Global Transaction ID)是对于一个已提交事务的唯一编号，并且是一个全局(主从复制)唯一的编号。
它的官方定义如下：
GTID = source_id ：transaction_id
7E11FA47-31CA-19E1-9E56-C43AA21293967:29
什么是sever_uuid，和Server-id 区别？
核心特性: 全局唯一,具备幂等性
```

GTID核心参数

```
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1

gtid-mode=on                        --启用gtid类型，否则就是普通的复制架构
enforce-gtid-consistency=true               --强制GTID的一致性
log-slave-updates=1                 --slave更新是否记入日志
```

**GTID复制配置过程：**

```
主库db01：
cat > /etc/my.cnf <<EOF
[mysqld]
basedir=/data/mysql/
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=51
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
[mysql]
prompt=db01 [\\d]>
EOF

slave1(db02)：
cat > /etc/my.cnf <<EOF
[mysqld]
basedir=/data/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=52
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
[mysql]
prompt=db02 [\\d]>
EOF

slave2(db03)：
cat > /etc/my.cnf <<EOF
[mysqld]
basedir=/data/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=53
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
[mysql]
prompt=db03 [\\d]>
EOF
```

初始化数据

```
mysqld --initialize-insecure --user=mysql --basedir=/data/mysql  --datadir=/data/mysql/data 
```

启动数据库

```
/etc/init.d/mysqld start
```

构建主从

```
master:51
slave:52,53

51:
grant replication slave  on *.* to repl@'10.0.0.%' identified by '123';

52\53:
change master to 
master_host='10.0.0.51',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;

start slave;
```

GTID 从库误写入操作处理

```
查看监控信息:
Last_SQL_Error: Error 'Can't create database 'oldboy'; database exists' on query. Default database: 'oldboy'. Query: 'create database oldboy'

Retrieved_Gtid_Set: 71bfa52e-4aae-11e9-ab8c-000c293b577e:1-3
Executed_Gtid_Set:  71bfa52e-4aae-11e9-ab8c-000c293b577e:1-2,
7ca4a2b7-4aae-11e9-859d-000c298720f6:1

注入空事物的方法：

stop slave;
set gtid_next='99279e1e-61b7-11e9-a9fc-000c2928f5dd:3';
begin;commit;
set gtid_next='AUTOMATIC';
    
这里的xxxxx:N 也就是你的slave sql thread报错的GTID，或者说是你想要跳过的GTID。
最好的解决方案：重新构建主从环境
```

GTID 复制和普通复制的区别

```
CHANGE MASTER TO
MASTER_HOST='10.0.0.51',
MASTER_USER='repl',
MASTER_PASSWORD='123',
MASTER_PORT=3307,
MASTER_LOG_FILE='mysql-bin.000001',
MASTER_LOG_POS=444,
MASTER_CONNECT_RETRY=10;

change master to 
master_host='10.0.0.51',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;
start slave;

（0）在主从复制环境中，主库发生过的事务，在全局都是由唯一GTID记录的，更方便Failover
（1）额外功能参数（3个）
（2）change master to 的时候不再需要binlog 文件名和position号,MASTER_AUTO_POSITION=1;
（3）在复制过程中，从库不再依赖master.info文件，而是直接读取最后一个relaylog的 GTID号
（4） mysqldump备份时，默认会将备份中包含的事务操作，以以下方式
    SET @@GLOBAL.GTID_PURGED='8c49d7ec-7e78-11e8-9638-000c29ca725d:1';
    告诉从库，我的备份中已经有以上事务，你就不用运行了，直接从下一个GTID开始请求binlog就行。
```

 

### 9\. 主从故障监控\\分析\\处理

主库:

```bash
show full processlist;
每个从库都会有一行dump相关的信息
HOSTS: 
db01:47176
State:
Master has sent all binlog to slave; waiting for more updates
如果现实非以上信息,说明主从之间的关系出现了问题    
```

从库:

```
db01 [(none)]>show slave status \G
*************************** 1. row ***************************
```

主库相关信息监控

```
Master_Host: 10.0.0.51
Master_User: repl
Master_Port: 3307
Master_Log_File: mysql-bin.000005
Read_Master_Log_Pos: 444
```

从库中继日志的应用状态

```
Relay_Log_File: db01-relay-bin.000002
Relay_Log_Pos: 485
```

从库复制线程有关的状态

```
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
Last_IO_Errno: 0
Last_IO_Error: 
Last_SQL_Errno: 0
Last_SQL_Error: 
```

过滤复制有关的状态

```
Replicate_Do_DB: 
Replicate_Ignore_DB: 
Replicate_Do_Table: 
Replicate_Ignore_Table: 
Replicate_Wild_Do_Table: 
Replicate_Wild_Ignore_Table: 
```

主从延时相关状态\(非人为\)

```
Seconds_Behind_Master: 0
```

延时从库有关的状态\(人为\)

```
SQL_Delay: 0
SQL_Remaining_Delay: NULL
```

GTID 复制有关的状态

```
Retrieved_Gtid_Set: 
Executed_Gtid_Set: 
Auto_Position: 0
```

### 主从复制故障分析

```
(1) 用户 密码  IP  port
Last_IO_Error: error reconnecting to master 'repl@10.0.0.51:3307' - retry-time: 10  retries: 7
[root@db01 ~]# mysql -urepl  -p123333  -h 10.0.0.51 -P 3307
ERROR 1045 (28000): Access denied for user 'repl'@'db01' (using password: YES)

原因:
密码错误 
用户错误 
skip_name_resolve
地址错误
端口
```

处理方法

```
stop  slave  
reset slave all 
change master to 
start slave
```

**主库连接数上线,或者是主库太繁忙**

```
show slave  staus \G 
Last_IO_Errno: 1040
Last_IO_Error: error reconnecting to master 'repl@10.0.0.51:3307' - retry-time: 10  retries: 7
处理思路:
拿复制用户,手工连接一下

[root@db01 ~]# mysql -urepl -p123 -h 10.0.0.51 -P 3307 
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1040 (HY000): Too many connections
处理方法:
db01 [(none)]>set global max_connections=300;

(3) 防火墙,网络不通
```

**请求二进制日志**

```
主库缺失日志
从库方面,二进制日志位置点不对
Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'could not find next log; the first event 'mysql-bin.000001' at 154, the last event read from '/data/3307/data/mysql-bin.000002' at 154, the last byte read from '/data/3307/data/mysql-bin.000002' at 154.'
```

```
注意: 在主从复制环境中,严令禁止主库中reset master; 可以选择expire 进行定期清理主库二进制日志
解决方案:
重新构建主从
```

** SQL 线程故障**

SQL线程功能：

```
(1)读写relay-log.info 
(2)relay-log损坏,断节,找不到
(3)接收到的SQL无法执行
```

**导致SQL线程故障原因分析：**

```
1. 版本差异，参数设定不同，比如：数据类型的差异，SQL_MODE影响
2.要创建的数据库对象,已经存在
3.要删除或修改的对象不存在  
4.DML语句不符合表定义及约束时.  
归根揭底的原因都是由于从库发生了写入操作.
Last_SQL_Error: Error 'Can't create database 'db'; database exists' on query. Default database: 'db'. Query: 'create database db'
```

处理方法\(以从库为核心的处理方案\)：

```
方法一：
stop slave; 
set global sql_slave_skip_counter = 1;
#将同步指针向下移动一个，如果多次不同步，可以重复操作。
start slave;
方法二：
/etc/my.cnf
slave-skip-errors = 1032,1062,1007
常见错误代码:
1007:对象已存在
1032:无法执行DML
1062:主键冲突,或约束冲突

但是，以上操作有时是有风险的，最安全的做法就是重新构建主从。把握一个原则,一切以主库为主.
```

一劳永逸的方法:

```
(1) 可以设置从库只读.
db01 [(none)]>show variables like '%read_only%';
注意：
只会影响到普通用户，对管理员用户无效。
(2)加中间件
读写分离。
```

主从延时监控及原因 

```
主库做了修改操作,从库比较长时间才能追上.
```

外在因素

```
网络 
主从硬件差异较大
版本差异
参数因素
```

主库

```
(1) 二进制日志写入不及时
[rep]>select @@sync_binlog;
(2) CR的主从复制中,binlog_dump线程,事件为单元,串行传送二进制日志(5.6 5.5)

1. 主库并发事务量大,主库可以并行,传送时是串行
2. 主库发生了大事务,由于是串行传送,会产生阻塞后续的事务.

解决方案:
1. 5.6 开始,开启GTID,实现了GC(group commit)机制,可以并行传输日志给从库IO
2. 5.7 开始,不开启GTID,会自动维护匿名的GTID,也能实现GC,我们建议还是认为开启GTID
3. 大事务拆成多个小事务,可以有效的减少主从延时.
```

 从库

```
SQL线程导致的主从延时
在CR复制情况下: 从库默认情况下只有一个SQL,只能串行回放事务SQL
1. 主库如果并发事务量较大,从库只能串行回放
2. 主库发生了大事务,会阻塞后续的所有的事务的运行

解决方案:
1. 5.6 版本开启GTID之后,加入了SQL多线程的特性,但是只能针对不同库(database)下的事务进行并发回放.
2. 5.7 版本开始GTID之后,在SQL方面,提供了基于逻辑时钟(logical_clock),binlog加入了seq_no机制,
真正实现了基于事务级别的并发回放,这种技术我们把它称之为MTS(enhanced multi-threaded slave).
3. 大事务拆成多个小事务,可以有效的减少主从延时.
[https://dev.mysql.com/worklog/task/?id=6314]
```

![](http://image.ownit.top/csdn/20200609173050827.png)

![](http://image.ownit.top/csdn/20200609173240393.png)