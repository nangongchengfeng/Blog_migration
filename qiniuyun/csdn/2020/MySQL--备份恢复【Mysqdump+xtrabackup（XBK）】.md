---
author: 南宫乘风
categories:
- MySQL
date: 2020-05-28 17:18:38
description: 运维在数据库备份恢复方面的职责设计备份策略全备、增量、时间、自动日常备份检查备份存在性备份空间够用否定期恢复演练测试库一季度或者半年故障恢复通过现有备份能够将数据库恢复到故障之前的时间点迁移停机时间回。。。。。。。
image: ../../title_pic/29.jpg
slug: '202005281718'
tags:
- mysql
- linux
- 数据库
- 运维
- 服务器
title: MySQL--备份恢复【Mysqdump+xtrabackup（XBK）】
---

<!--more-->

## 1.运维在数据库备份恢复方面的职责

**1.设计备份策略**

> 全备 、增量、时间、自动

**2.日常备份检查**

> 1.  备份存在性
> 2.  备份空间够用否

** 3.定期恢复演练\(测试库\)**

> 一季度 或者 半年

**4.故障恢复**

> 通过现有备份,能够将数据库恢复到故障之前的时间点.  

**5.迁移**

> 1\. 停机时间  
> 2\. 回退方案

## **2.Mysql数据损坏类型**

**1.物理损坏**

> 磁盘损坏：硬件，磁道坏，dd，格式化
> 
> 文件损坏：数据文件损坏，redo损坏

**2.逻辑损坏**

```bash
drop
delete
truncate
update
```

## 3\. 备份类型

**1.热备**

> 在数据库正常业务时,备份数据,并且能够一致性恢复（只能是innodb）
> 
> 对业务影响非常小

**2.温备**

> 锁表备份,只能查询不能修改（myisam）  
> 影响到写入操作

**3.冷备**

> 关闭数据库业务,数据库没有任何变更的情况下,进行备份数据.  
> 业务停止

## 4\. 备份方式及工具介绍

**1.逻辑备份工具**

```bash
基于SQL语句进行备份
mysqldump       *****
mysqlbinlog     *****
```

**2\. 物理备份工具**

```bash
基于磁盘数据文件备份
xtrabackup(XBK) ：percona 第三方   *****
MySQL Enterprise Backup（MEB）
```

## 5\. 逻辑备份和物理备份的比较

 mysqldump \(MDP\)

**优点：**

- 1.不需要下载安装
- 2.备份出来的是SQL，文本格式，可读性高,便于备份处理
- 3.压缩比较高，节省备份的磁盘空间

**缺点：**

- 依赖于数据库引擎，需要从磁盘把数据读出，然后转换成SQL进行转储，比较耗费资源，数据量大的话效率较低

**建议：**

- 100G以内的数据量级，可以使用mysqldump
- 超过TB以上，我们也可能选择的是mysqldump，配合分布式的系统
- 1EB  =1024 PB =1000000 TB

## 6.备份策略

**备份方式：**

- 全备:全库备份，备份所有数据
- 增量:备份变化的数据

**备份工具**

- 逻辑备份=mysqldump+mysqlbinlog
- 物理备份=xtrabackup\_full+xtrabackup\_incr+binlog或者xtrabackup\_full+binlog

**备份周期:**

- 根据数据量设计备份周期
- 比如：周日全备，周1-周6增量

**备份监控**

- 备份空间
- 备份日志

## 7.容灾策略

**备份**

**架构**

- 高可用         负载均衡
- 演示从库         主从同步
- 灾备库           异地备份

**定期的故障恢复演练**

## 8.mysqldump应用

**介绍：逻辑备份工具。备份的是sql语句**

**备份方式**

InnoDB

> - 可以采取快照备份的方式
> - 开启一个独立的事务，获取当前最新的一致性快照，将快照数据，放在临时表中，转换成SQL（Create database，create table，insert），保存到sql文件中

非InnoDB

> - 需要锁表备份。触发FTWRL，全局锁表。
> - 将快照数据，放在临时表中，转换成SQL（Create database，create table，insert），保存到sql文件中

**核心参数**

建立备份目录，授权

```bash
mkdir -p /data/backup
chown -R mysql.mysql /data/backup/
```

### **连接参数**

 -    \-u  #用户
 -    \-p  #密码
 -    \-h   #主机地址
 -    \-P   #端口
 -    \-S  #socket连接
 -    \-A   #全备

```bash
 mysqldump -uroot -proot -A >/data/backup/full.sql
```

 -    \-B  #备份一个或者多个

```bash
mysqldump -uroot -proot -B gtid gtid2  >/data/backup/db.sql
```

**备份库下的多个表（不加参数）**

```bash
 mysqldump -uroot -proot gtid t1 t1 >/data/backup/db.sql
```

### **备份高级参数**

```bash
--master-data=2
```

```bash
以注释的形式,保存备份开始时间点的binlog的状态信息

mysqldump -uroot -p  -A  -R --triggers --master-data=2   >/back/world.sql
[root@db01 ~]# grep 'CHANGE' /backup/world.sql 
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000035', MASTER_LOG_POS=194;

功能：
（1）在备份时，会自动记录，二进制日志文件名和位置号
0 默认值
1  以change master to命令形式，可以用作主从复制
2  以注释的形式记录，备份时刻的文件名+postion号
（2） 自动锁表
（3）如果配合--single-transaction，只对非InnoDB表进行锁表备份，InnoDB表进行“热“”备，实际上是实现快照备份。
```

```bash
--single-transaction
```

```bash
innodb 存储引擎开启热备(快照备份)功能       
master-data可以自动加锁
（1）在不加--single-transaction ，启动所有表的温备份，所有表都锁定
（1）加上--single-transaction ,对innodb进行快照备份,对非innodb表可以实现自动锁表功能
例子6: 备份必加参数
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
```

```bash
--set-gtid-purged=auto
```

```bash
auto , on
off 
使用场景:
1. --set-gtid-purged=OFF,可以使用在日常备份参数中.
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
2. auto , on:在构建主从复制环境时需要的参数配置
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=ON >/data/backup/full.sql
```

```
--max-allowed-packet=#
```

```bash
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF --max-allowed-packet=256M >/data/backup/full.sql

 --max-allowed-packet=# 
The maximum packet length to send to or receive from server.
```

- \-R            备份存储过程及函数
- \--triggers  备份触发器
- \-E             备份事件

 

### 生产备份语句（只是建议，根据自己需求来改）

```bash
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF --max-allowed-packet=256M >/data/backup/full.sql
```

### 练习   实现所有表的单独备份

```bash
提示：
information_schema.tables
mysqldump -uroot -p123 world city >/backup/world_city.sql

select concat("mysqldump -uroot -p123 ",table_schema," ",table_name," --master-data=2 --single-transaction --set-gtid-purged=0  -R -E --triggers>/backup/",table_schema,"_",table_name,".sql") from information_schema.tables where table_schema not in ('sys','information_schema','performance_schema');
```

## 9\. 备份时优化参数:

```
(1) max_allowed_packet   最大的数据包大小

mysqldump -uroot -p123 -A  -R  --triggers --set-gtid-purged=OFF --master-data=2 max_allowed_packet=128M  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz

(2) 增加key_buffer_size    (临时表有关)
(3) 分库分表并发备份       (作业)
(4) 架构分离,分别备份      (架构拆分,分布式备份)
```

## 10\. MySQL物理备份工具-xtrabackup\(XBK、Xbackup\)

安装并安装

```bash
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.12/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.12-1.el7.x86_64.rpm

https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.4/binary/redhat/6/x86_64/percona-xtrabackup-24-2.4.4-1.el6.x86_64.rpm

yum -y install percona-xtrabackup-24-2.4.4-1.el7.x86_64.rpm
```

**备份命令介绍:**

```bash
xtrabackup
innobackupex    ******
```

**备份方式——物理备份**

```bash
（1）对于非Innodb表（比如 myisam）是，锁表cp数据文件，属于一种温备份。
（2）对于Innodb的表（支持事务的），不锁表，拷贝数据页，最终以数据文件的方式保存下来，把一部分redo和undo一并备走，属于热备方式。
```

### xbk 在innodb表备份恢复的流程

```
  0、xbk备份执行的瞬间,立即触发ckpt,已提交的数据脏页,从内存刷写到磁盘,并记录此时的LSN号
  1、备份时，拷贝磁盘数据页，并且记录备份过程中产生的redo和undo一起拷贝走,也就是checkpoint LSN之后的日志
  2、在恢复之前，模拟Innodb“自动故障恢复”的过程，将redo（前滚）与undo（回滚）进行应用
  3、恢复过程是cp 备份到原来数据目录下
```

### innobackupex使用

**全备**

```bash
innobackupex --user=root --password=123  /data/backup
```

**自主定制备份路径名**

```bash
 innobackupex --user=root --password=123 --no-timestamp /data/backup/full
```

**备份集中多出来的文件：**

```bash
-rw-r----- 1 root root       24 Jun 29 09:59 xtrabackup_binlog_info
-rw-r----- 1 root root      119 Jun 29 09:59 xtrabackup_checkpoints
-rw-r----- 1 root root      489 Jun 29 09:59 xtrabackup_info
-rw-r----- 1 root root     2560 Jun 29 09:59 xtrabackup_logfile

xtrabackup_binlog_info ：（备份时刻的binlog位置）
[root@db01 full]# cat xtrabackup_binlog_info 
mysql-bin.000003    536749
79de40d3-5ff3-11e9-804a-000c2928f5dd:1-7
记录的是备份时刻，binlog的文件名字和当时的结束的position，可以用来作为截取binlog时的起点。

xtrabackup_checkpoints ：
backup_type = full-backuped
from_lsn = 0            上次所到达的LSN号(对于全备就是从0开始,对于增量有别的显示方法)
to_lsn = 160683027      备份开始时间(ckpt)点数据页的LSN    
last_lsn = 160683036    备份结束后，redo日志最终的LSN
compact = 0
recover_binlog_info = 0
（1）备份时刻，立即将已经commit过的，内存中的数据页刷新到磁盘(CKPT).开始备份数据，数据文件的LSN会停留在to_lsn位置。
（2）备份时刻有可能会有其他的数据写入，已备走的数据文件就不会再发生变化了。
（3）在备份过程中，备份软件会一直监控着redo的undo，如果一旦有变化会将日志也一并备走，并记录LSN到last_lsn。
从to_lsn  ----》last_lsn 就是，备份过程中产生的数据变化.
```

##  innobackupex 增量备份\(incremental\)

- （1）增量备份的方式，是基于上一次备份进行增量。
- （2）增量备份无法单独恢复。必须基于全备进行恢复。
- （3）所有增量必须要按顺序合并到全备中。

### ![](../../image/20200528171555177.png)

### ![](../../image/2020052817161814.png)

### 增量备份命令

```bash
（1）删掉原来备份
略.
（2）全备（周日）
[root@db01 backup]# innobackupex --user=root --password --no-timestamp /backup/full >&/tmp/xbk_full.log
（3）模拟周一数据变化
db01 [(none)]>create database cs charset utf8;
db01 [(none)]>use cs
db01 [cs]>create table t1 (id int);
db01 [cs]>insert into t1 values(1),(2),(3);
db01 [cs]>commit;

（4）第一次增量备份（周一）
innobackupex --user=root --password=123 --no-timestamp --incremental --incremental-basedir=/backup/full  /backup/inc1 &>/tmp/inc1.log
（5）模拟周二数据
db01 [cs]>create table t2 (id int);
db01 [cs]>insert into t2 values(1),(2),(3);
db01 [cs]>commit;
（6）周二增量
 innobackupex --user=root --password=123 --no-timestamp --incremental --incremental-basedir=/backup/inc1  /backup/inc2  &>/tmp/inc2.log
（7）模拟周三数据变化
db01 [cs]>create table t3 (id int);
db01 [cs]>insert into t3 values(1),(2),(3);
db01 [cs]>commit;
db01 [cs]>drop database cs;
```

恢复到周三误drop之前的数据状态

```bash
恢复思路：
1.  挂出维护页，停止当天的自动备份脚本
2.  检查备份：周日full+周一inc1+周二inc2，周三的完整二进制日志
3. 进行备份整理（细节），截取关键的二进制日志（从备份——误删除之前）
4. 测试库进行备份恢复及日志恢复
5. 应用进行测试无误，开启业务
6. 此次工作的总结
```

恢复过程

```bash
1. 检查备份
1afe8136-601d-11e9-9022-000c2928f5dd:7-9
2. 备份整理（apply-log）+合并备份（full+inc1+inc2）
(1) 全备的整理
[root@db01 one]# innobackupex --apply-log --redo-only /data/backup/full
(2) 合并inc1到full中
[root@db01 one]# innobackupex --apply-log --redo-only --incremental-dir=/data/backup/inc1 /data/backup/full
(3) 合并inc2到full中
[root@db01 one]# innobackupex --apply-log  --incremental-dir=/data/backup/inc2 /data/backup/full
(4) 最后一次整理全备
[root@db01 backup]#  innobackupex --apply-log  /data/backup/full
3. 截取周二 23:00 到drop 之前的 binlog 
[root@db01 inc2]# mysqlbinlog --skip-gtids --include-gtids='1afe8136-601d-11e9-9022-000c2928f5dd:7-9' /data/binlog/mysql-bin.000009 >/data/backup/binlog.sql
4. 进行恢复
[root@db01 backup]# mkdir /data/mysql/data2 -p
[root@db01 full]# cp -a * /data/mysql/data2
[root@db01 backup]# chown -R mysql.  /data/*
[root@db01 backup]# systemctl stop mysqld
vim /etc/my.cnf
datadir=/data/mysql/data2
systemctl start mysqld
Master [(none)]>set sql_log_bin=0;
Master [(none)]>source /data/backup/binlog.sql
```

下面是我画的思维导图，可以很快加强记忆。

![](../../image/2020052817175226.png)