---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-21 22:18:59
description: 它是开源免费的支持数据库热备份的软件，它能对和存储引擎的数据库非阻塞地备份。它不暂停服务创建热备份；为做增量备份；在服务器之间做在线表迁移；使创建更加容易；备份而不增加服务器的负载。是一家老牌的技术咨。。。。。。。
image: http://image.ownit.top/4kdongman/66.jpg
tags:
- 技术记录
title: MySQL数据物理备份之xtrabackup
---

<!--more-->

 

# **percona-xtrabackup**

  
  
它是开源免费的支持MySQL 数据库热备份的软件，它能对InnoDB和XtraDB存储引擎的数据库非阻塞地备份。它不暂停服务创建Innodb**热备份**；  
为mysql做增量备份；在mysql服务器之间做在线表迁移；使创建replication更加容易；备份mysql而不增加服务器的负载。  
percona是一家老牌的mysql技术咨询公司。它不仅提供mysql的技术支持、培训、咨询，还发布了mysql的分支版本--percona Server。并围绕  
percona Server还发布了一系统的mysql工具。  
\=================================================================================  
 

## 完全备份

 

## 增量备份

![](http://image.ownit.top/csdn/20190421220749983.png)

 

## 差异备份

![](http://image.ownit.top/csdn/20190421220813787.png)

xtrabackup  
Xtrabackup是一个对InnoDB做数据备份的工具，支持在线热备份（备份时不影响数据读写），是商业备份工具InnoDB Hotbackup的一个很好的替代品。  
Xtrabackup有两个主要的工具：xtrabackup、innobackupex  
xtrabackup 只能备份InnoDB和XtraDB两种数据表，而不能备份MyISAM数据表。 innobackupex 是参考了InnoDB Hotbackup的innoback脚本修改而来的.innobackupex是一个perl脚本封装，封装了xtrabackup。主要是为了方便的同时备份InnoDB和MyISAM引擎的表，但在处理myisam时需要加一个读锁。并且加入了一些使用的选项。如slave-info可以记录备份恢复后作为slave需要的一些信息，根据这些信息，可以很方便的利用备份来重做slave。支持完全备份和增量备份

-  备份过程快速、可靠；
- 备份过程不会打断正在执行的事务；
-  能够基于压缩等功能节约磁盘空间和流量；
- 自动实现备份检验；
- 还原速度快；

使用innobakupex备份时，其会调用xtrabackup备份所有的InnoDB表，复制所有关于表结构定义的相关文件\(.frm\)、以及MyISAM、MERGE、CSV和ARCHIVE表的相关文件，同时还会备份触发器和数据库配置信息相关的文件。这些文件会被保存至一个以时间命令的目录中。

\(1\)xtrabackup\_checkpoints —— 备份类型（如完全或增量）、备份状态（如是否已经为prepared状态）和LSN\(日志序列号\)范围信息；每个InnoDB页\(通常为16k大小\)都会包含一个日志序列号，即LSN。LSN是整个数据库系统的系统版本号，每个页面相关的LSN能够表明此页面最近是如何发生改变的。

\(2\)xtrabackup\_binlog\_info —— mysql服务器当前正在使用的二进制日志文件及至备份这一刻为止二进制日志事件的位置。\(3\)xtrabackup\_binlog\_pos\_innodb —— 二进制日志文件及用于InnoDB或XtraDB表的二进制日志文件的当前position。

\(4\)xtrabackup\_binary —— 备份中用到的xtrabackup的可执行文件；

\(5\)backup-my.cnf —— 备份命令用到的配置选项信息；

###   
安装xtrabackup  
 

```
[root@localhost ~]# yum -y install percona-xtrabackup-2.1.9-744.rhel6.x86_64.rpm
[root@localhost ~]# rpm -ql percona-xtrabackup |grep bin
/usr/bin/innobackupex 支持myisam、innodb
/usr/bin/innobackupex-1.5.1
/usr/bin/xbcrypt
/usr/bin/xbstream
/usr/bin/xtrabackup 仅适用于percona Server
/usr/bin/xtrabackup_55 适用mysql 5.5数据库
/usr/bin/xtrabackup_56 适用mysql5.6数据库
```

# 完整备份实例

：  
\==备份==

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 /mysqlbackup/full
[root@localhost ~]# ls /mysqlbackup/full/2015-09-15_11-03-03/
backup-my.cnf company mysql school test xtrabackup_binary xtrabackup_checkpoints
bbs 　　ibdata1 performance_schema shop weibo xtrabackup_binlog_info xtrabackup_logfile
[root@localhost 2015-09-15_11-03-03]# cat xtrabackup_binlog_info
localhost-bin.000003 2090096
```

  
\==恢复==  
a. 准备新环境

```
[root@localhost ~]# rm -rf /usr/local/mysql/data
[root@localhost ~]# chown -R mysql.mysql /usr/local/mysql
[root@localhost ~]# /usr/local/mysql/scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data
[root@localhost ~]# killall -9 mysqld
[root@localhost ~]# service mysqld start
```

  
b. 恢复

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --apply-log /mysqlbackup/full/2015-09-15_11-03-03/
[root@localhost ~]# rm -rf /usr/local/mysql/data/*
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --copy-back /mysqlbackup/full/2015-09-15_11-03-03/
[root@localhost ~]# cd /usr/local/mysql
[root@localhost ~]# chown -R mysql.mysql .
[root@localhost ~]# killall -9 mysqld
[root@localhost ~]# service mysqld start
```

  
  
 

# 增量备份实例：

  
\==备份==  
1、完整备份：周一

```
create database testdb;
use testdb;
create table test(id int);
insert into test values(1);
select * from test;
```

 

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 /mysqlbackup/full
```

  
2、增量备份：周二　——　周六

```
insert into testdb.test values(2);
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --incremental /mysqlbackup/incremental
--incremental-basedir=完全备份目录
```

  
 

```
insert into testdb.test values(3);
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --incremental /mysqlbackup/incremental
--incremental-basedir=上次增量目录
```

  
 

```
insert into testdb.test values(4);
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --incremental /mysqlbackup/incremental
--incremental-basedir=上次增量目录
```

  
 

# \==恢复==

  
1.恢复全量的redo log

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --apply-log --redo-only /mysqlbackup/full/...
```

  
2.恢复增量的redo log

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --apply-log --redo-only /mysqlbackup/full/...
--incremental-dir=/mysqlbackup/incremental/第一次增量
```

 

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --apply-log --redo-only /mysqlbackup/full/...
--incremental-dir=/mysqlbackup/incremental/第二次增量
```

 

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --apply-log --redo-only /mysqlbackup/full/...
--incremental-dir=/mysqlbackup/incremental/第Ｎ次增量
```

  
  
3.关闭mysqld，替换数据文件\(cp,rsyn,innobackupex copy-back\)，修改权限  
  
4.启动mysqld  
  
5.通过binlog增量恢复  
  
 

```
create database testdb;
use testdb;
create table test(id int);
insert into test values(1);
select * from test;

[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 /mysqlbackup/full
```

# 差异备份实例：

  
\==备份==  
1、完整备份：周一  
  
  
2、差异备份：周二　——　周六

```
insert into testdb.test values(2);
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --incremental /mysqlbackup/incremental
--incremental-basedir=完全备份目录
```

 

```
insert into testdb.test values(3);
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --incremental /mysqlbackup/incremental
--incremental-basedir=完全备份目录
```

  
  
 

```
insert into testdb.test values(4);
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --incremental /mysqlbackup/incremental
--incremental-basedir=完全备份目录
```

# \==恢复==

  
1.恢复全量的redo log

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --apply-log --redo-only /mysqlbackup/full/...
```

  
2.恢复差异的redo log

```
[root@localhost ~]# innobackupex --host=localhost --socket=/tmp/mysql.sock --defaults-file=/etc/my.cnf --user=root --password=888 --apply-log --redo-only /mysqlbackup/full/...
--incremental-dir=/mysqlbackup/incremental/某个差异备份
```

  
3.关闭mysqld，替换数据文件\(cp,rsyn\)，修改权限  
  
4.启动mysqld  
  
5.通过binlog增量恢复  
  
备份单库、多库、多表单数据库备份  
innobackupex \--defaults-file=/etc/my.cnf \--socket=/tmp/mysql.sock \--databases=uplook \--no-timestamp /server/backup/uplook  
多数据库备份innobackupex \--user=root \--password=123456 \--include='dba.\*|dbb.\*' /server/backup  
多表备份方法一：innobackupex \--user=root \--password=123456 \--include='dba.tablea|dbb.tableb' /server/backup  
方法二：使用--tables-file参数，这种方式是将所有要备份的完整表名都写在一个文本文件中，每行一个完整表名，然后程序读取这个文本文件进行备份。完整表名即：databasename.tablename  
echo "lianxi.Student" >/tmp/table1.txt  
innobackupex \--defaults-file=/etc/my.cnf \--socket=/tmp/mysql.sock \--tables-file='/tmp/table1.txt' \--no-timestamp /server/backup/table1  
  
恢复单库、多库、多表单数据库恢复应用日志：  
innobackupex \--apply-log /server/backup/uplook  
删除数据库数据文件：systemctl stop mysql；rm \-rf /usr/local/mysql/data/\*  
还原数据：innobackupex \--copy-back /server/backup/uplook  
授权：chown \-R mysql.mysql /usr/local/mysql  
初始化数据库：/usr/local/mysql/scripts/mysql\_install\_db \--user=mysql \--datadir=/usr/local/mysql/data \--basedir=/usr/local/mysql \--explicit\_defaults\_for\_timestamp  
启动数据库：systemctl start mysql  
测试：mysql \-e "select \* from uplook.Student;"  
  
多表数据恢复应用日志：  
innobackupex \--apply-log \--export /server/backup/table1/  
定义表--删除表空间--拷贝\*.ibd/\*.cfg文件--导入表空间  
定义表：模拟删除表，重新定义表结构，过程略  
删除表空间：mysql> ALTER TABLE Student DISCARD TABLESPACE;  
拷贝\*.ibd/\*.cfg文件：\[root\@localhost \~\]# cp /server/backup/table1/lianxi/Student.\{cfg,ibd\} /usr/local/mysql/data/lianxi/  
\[root\@localhost \~\]# chown \-R mysql.mysql /usr/local/mysql/data/lianxi/  
导入表空间：mysql> ALTER TABLE Student IMPORT TABLESPACE;  
测试：mysql> select \* from Student;