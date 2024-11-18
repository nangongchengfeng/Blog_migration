---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-20 21:20:34
description: 逻辑备份：备份的是建表、建库、插入等操作所执行语句，适用于中小型数据库，效率相对较低。使用实现逻辑备份语法：服务器用户名密码数据库名备份文件关于数据库名：所有库数据库名数据库的表、多个数据库关于其它参。。。。。。。
image: ../../title_pic/31.jpg
slug: '201904202120'
tags:
- 技术记录
title: MySQL数据逻辑备份
---

<!--more-->

逻辑备份： 备份的是建表、建库、插入等操作所执行SQL语句，适用于中小型数据库，效率相对较低。  
mysqldump  
mydumper  
  
**使用mysqldump实现逻辑备份**

  
语法：  
\# mysqldump \-h 服务器 \-u用户名 \-p密码 数据库名 > 备份文件.sql

关于数据库名：  
\-A, \--all-databases 所有库  
school 数据库名  
school stu\_info t1 school数据库的表stu\_info、t1  
\-B, \--databases bbs test mysql 多个数据库  
关于其它参数说明：  
\--single-transaction     #基于此项可以实现对InnoDB表做热备份  
\-x, \--lock-all-tables         #执行备份时为所有表请求加锁 MyISAM  
\-l, \--lock-tables  
\-E, \--events               #备份事件调度器代码  
\--opt                     #同时启动各种高级选项  
\-R, \--routines             #备份存储过程和存储函数  
\-F, \--flush-logs              #备份之前刷新日志  
\--triggers                #备份触发器  
\--master-data=2        #备库，该选项将会记录binlog的日志位置与文件名并追加到文件中，如果为1将会输出CHANGE MASTER命令，主从下有用  
注意：-B 作用：创建数据库和切换到数据库，恢复时不用创建数据库和删表。备份多个库，-B 数据库1 数据库2 .  
\-d只备份库结构，不包含数据内容  
备份：mysqldump \-u 用户名 \-p 数据库名 表名 > 备份的文件名  
备份多个表：mysqldump \-u 用户名 \-p 数据库名 表名1 表名2 > 备份的文件名

示例：

备份jiaowu数据库，名字为hei.sql

显示数据库

```
[root@wei ~]# mysql -uroot -proot -e 'show databases;'
```

![](../../image/20190420202910838.png)  
备份数据库

```
[root@wei ~]# mysqldump -uroot -proot jiaowu >hei.sql
```

![](../../image/20190420203308798.png)

  
\==备份==

```
[root@localhost ~]# mysqldump -uroot -proot --single-transaction --master-data=2 company > /tmp/company_`date +%F-%H-%M`.sql
[root@localhost ~]# mysqldump -uroot -proot --single-transaction --master-data=2 school > /tmp/school_`date +%F-%H-%M`.sql
[root@localhost ~]# mysqldump -uroot -proot --single-transaction --master-data=2 school |gzip > /tmp/school_`date +%F-%H-%M`.gz
[root@localhost ~]# mysqldump -uroot -proot --routines --events --triggers --master-data=2 --flush-logs --all-databases > /backup/all_`date +%F`.sql
```

![](../../image/20190420204345705.png)  
  
  
\==恢复==

```
[root@localhost ~]# mysql -uroot -p888 -e 'create database school'
[root@localhost ~]# mysql -uroot -p888 school < /tmp/school_2015-09-14-15-40.sql
root@(school)> source /tmp/school_2015-09-14-15-40.sql
[root@localhost tmp]# gunzip -fc school_2015-09-14-15-09.gz | mysql -uroot -p888 school
```

  
  
\==增量备份==  
![](../../image/2019042020225736.png)

**增量备份前提：**

1）my.cnf，是要开启MySQL log-bin日志功能，重启MySQL      log\_bin = /data/mysql/data/mysql-bin  
2）存在一个完全备份，生产环境一般凌晨某个时刻进行全备  
示例：

```
mysqldump -uroot -p --default-character-set=gbk --single-transaction -F -B school |gzip > /server/backup/school_$(date +%F).sql.gz
```

  
InnoDB 表在备份时，通常启用选项 \--single-transaction 来保证备份的一致性  
  
增量备份--恢复过程  
1、检查凌晨备份  
2、检查全备后的所有binlog # ls \-lrt /usr/local/mysql/data/mysql-bin.\*  
3、立即刷新并备份出binlog mysqladmin \-uroot \-p flush-logs  
cp /usr/local/mysql/data/mysql-bin.000004 /server/backup/  
提示：根据时间点及前一个binlog可以知道发现问题时刻前binlog日志为mysql-bin.000004  
4、恢复binlog生成sql语句mysqlbinlog mysql-bin.000004 > bin.log  
5、恢复凌晨备份  
6、恢复增量备份  
  
mysqlbinlog增量恢复方式  
基于时间点恢复  
1）指定开始时间到结束时间 myslbinlog mysqlbin.000008 \--start-datetime=’2014-10-45 01:10:46’ \--stop-datetime=’2014-10-45 03:10:46’-r time.sql  
2）指定开始时间到文件结束 myslbinlog mysqlbin.000008 \--start-datetime=’2014-10-45 01:10:46’ \-d esen \-r time.sql  
3）从文件开头到指定结束时间 myslbinlog mysqlbin.000008 \--stop-datetime=’2014-10-45 03:10:46’ \-d esen \-r time.sql  
基于位置点的增量恢复  
1）指定开始位置到结束位置 myslbinlog mysqlbin.000008 \--start-position=510 \--stop-position=1312 \-r pos.sql  
2）指定开始位置到文件结束 myslbinlog mysqlbin.000008 \--start-position=510 \-r pos.sql  
3）从文件开始位置到指定结束位置 myslbinlog mysqlbin.000008 \--stop-position=1312 \-r pos.sql  
  
\==恢复binlog==  
单库？全库

```
[root@localhost ~]# mysqlbinlog -d school localhost-bin.000002 --start-position=11574908 > school-bin.sql
[root@localhost ~]# mysqlbinlog -d school localhost-bin.000003 >> school-bin.sql
[root@localhost ~]# mysqlbinlog -d school localhost-bin.000004 >> school-bin.sql
[root@localhost ~]# mysql -uroot -p888 school < school-bin.sql
```

  
  
实现自动化备份（数据库小）  
备份计划：  
1\. 什么时间 2:00  
2\. 对哪些数据库备份  
3\. 备份文件放的位置  
  
备份脚本：

```
[root@yang ~]# vim /mysql_back.sql
#!/bin/bash
back_dir=/backup
back_file=`date +%F`_all.sql
user=root
pass=123

if [ ! -d /backup ];then
mkdir -p /backup
fi

# 备份并截断日志
mysqldump -u${user} -p${pass} --lock-all-tables --routines --events --triggers --master-data=2 --flush-logs --all-databases > /$back_dir/$back_file

# 只保留最近一周的备份
cd $back_dir
find . -mtime +7 -exec rm -rf {} \;
```

  
手动测试：

```
[root@yang ~]# chmod a+x /mysql_back.sql
[root@yang ~]# chattr +i /mysql_back.sql
[root@yang ~]# /mysql_back.sql
```

  
配置cron：  
 

```
[root@yang ~]# crontab -e
0 2 * * * /mysql_back.sql
```

### Mydumper介绍

  
Mydumper是一个针对MySQL和Drizzle的高性能多线程备份和恢复工具。开发人员主要来自MySQL,Facebook,SkySQL公司。目前已经在一些线上使用了Mydumper。  
Mydumper主要特性：  
• 轻量级C语言写的  
• 执行速度比mysqldump快10倍  
• 事务性和非事务性表一致的快照\(适用于0.2.2以上版本\)  
• 快速的文件压缩  
• 支持导出binlog  
• 多线程恢复\(适用于0.2.1以上版本\)  
• 以守护进程的工作方式，定时快照和连续二进制日志\(适用于0.5.0以上版本\)  
• 开源 \(GNU GPLv3\)  
 

```
#wget https://launchpadlibrarian.net/225370879/mydumper-0.9.1.tar.gz
# yum -y install glib2-devel mysql-devel zlib-devel pcre-devel
[root@localhost ~]# tar xf mydumper-0.9.1.tar.gz -C /usr/local/src/
[root@localhost ~]# cd /usr/local/src/mydumper-0.9.1/
# cmake .
# make
# make install
```

  
  
mydumper参数介绍：  
\-d, \--directory 导入备份目录  
\-q, \--queries-per-transaction 每次执行的查询数量, 默认1000  
\-o, \--overwrite-tables 如果表存在删除表  
\-B, \--database 需要备份的库  
\-T, \--tables-list 需要备份的表，用，分隔  
\-o, \--outputdir 输出目录  
\-s, \--statement-size Attempted size of INSERT statement in bytes, default 1000000  
\-r, \--rows 试图分裂成很多行块表  
\-c, \--compress 压缩输出文件  
\-e, \--build-empty-files 即使表没有数据，还是产生一个空文件  
\-x, \--regex 支持正则表达式  
\-i, \--ignore-engines 忽略的存储引擎，用，分隔  
\-m, \--no-schemas 不导出表结构  
\-k, \--no-locks 不执行临时共享读锁 警告：这将导致不一致的备份  
\-l, \--long-query-guard 长查询，默认60s  
\--kill-long-queries kill掉长时间执行的查询\(instead of aborting\)  
\-b, \--binlogs 导出binlog  
\-D, \--daemon 启用守护进程模式  
\-I, \--snapshot-interval dump快照间隔时间，默认60s，需要在daemon模式下  
\-L, \--logfile 日志文件  
\-h, \--host  
\-u, \--user  
\-p, \--password  
\-P, \--port  
\-S, \--socket  
\-t, \--threads 使用的线程数，默认4  
\-C, \--compress-protocol 在mysql连接上使用压缩  
\-V, \--version  
\-v, \--verbose 更多输出, 0 = silent, 1 = errors, 2 = warnings, 3 = info, default 2  
  
mydumper输出文件：  
metadata:元数据 记录备份开始和结束时间，以及binlog日志文件位置。  
table data:每个表一个文件  
table schemas:表结构文件  
binary logs: 启用--binlogs选项后，二进制文件存放在binlog\_snapshot目录下  
daemon mode:在这个模式下，有五个目录0，1，binlogs，binlog\_snapshot，last\_dump。  
备份目录是0和1，间隔备份，如果mydumper因某种原因失败而仍然有一个好的快照，  
当快照完成后，last\_dump指向该备份。  
  
 

## mydumper用例

  
\==备份==

```
#export LD_LIBRARY_PATH="/usr/local/mysql/lib:$LD_LIBRARY_PATH"
[root@localhost ~]# mydumper -h localhost -u root -p 123456 -t 6 -S /tmp/mysql.sock -B uplook -o /mysqlbackup/
[root@localhost ~]# ls /mysqlbackup/
metadata uplooking.Student-schema.sql uplook-schema-create.sql uplook.Student.sql
uplooking-schema-create.sql uplooking.Student.sql uplook.Student-schema.sql

** (mydumper:5247): CRITICAL **: Error connecting to database: Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)
```

  
解决方法：建立软连接

```
ln -sv /tmp/mysql.sock /var/lib/mysql/mysql.sock

[root@localhost ~]# cat /mysqlbackup/metadata
[root@localhost ~]# cat /mysqlbackup/metadata
Started dump at: 2017-08-05 15:48:09
Finished dump at: 2017-08-05 15:48:09
```

  
  
\==恢复==

```
[root@localhost ~]# mysql -uroot -p -e 'drop database uplook;'
[root@localhost ~]# myloader -h localhost -u root -p 123456 -S /tmp/mysql.sock -d /mysqlbackup/ -o -B uplook
```