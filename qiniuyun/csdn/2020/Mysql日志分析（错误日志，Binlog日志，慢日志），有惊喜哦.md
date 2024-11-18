---
author: 南宫乘风
categories:
- MySQL
date: 2020-05-27 17:51:57
description: 日志错误日志作用排查运行过程的故障默认配置默认就开启了默认路径和名字在这里插入图片描述人为定制位置重启生效在这里插入图片描述二进制日志作用备份恢复必须依赖二进制日志主从环境必须依赖二进制日志配置必须加。。。。。。。
image: ../../title_pic/32.jpg
slug: '202005271751'
tags:
- mysql
- 数据库
- linux
title: Mysql日志分析（错误日志，Binlog日志，慢日志），有惊喜哦
---

<!--more-->

# Mysql日志

## 1.错误日志

### 1.作用

**\- 排查MySQL运行过程的故障.**

### 2.默认配置

- ```
  1.默认就开启了
  ```
- ```
  2.默认路径和名字: datadir/hostname.err
  ```

![在这里插入图片描述](../../image/2020052717320827.png)

### 3.人为定制位置

```bash
- log_error=/tmp/mysql.log
```

重启生效

```bash
show variables like 'log_error';
```

![在这里插入图片描述](../../image/20200527173404582.png)

## 二进制日志\(binlog\)

### 1.作用

**\- \(1\)备份恢复必须依赖二进制日志**  
**\- \(2\)主从环境必须依赖二进制日志**

### 2\. binlog配置 \(5.7必须加server\_id\)

```
    1.默认：8.0版本以前，没有开启（注意：MySQL默认是没有开启二进制日志的
	说明：和数据盘分开，防止数据盘损坏，导致binlong无法恢复
	2.默认配置方法

	server_id=6   # 主机编号。主从使用，    5.7以后开启binlog要加此参数                        
	log_bin=/data/binlog/mysql-bin #日志存放目录+日志名前缀，例如：mysql-bin.000001
	sync_binlog=1   #binlog日志刷盘策略，双一的第二个1。每次事务提交立即刷写binlog到磁盘
	binlog_format=row  #binlog的记录格式为row模式
	重启完成
```

![在这里插入图片描述](../../image/20200527173938813.png)

**\- 基础参数查看**

```
- 开关（1：表示开启）

	- select @@log_bin;

- 日志路径及名字

	- select @@log_bin_basename;

- 服务ID号

	- select @@server_id;

- 二进制日志格式

	- select @@binlog_format;

- 双一标准之二

	- select @@sync_binlog;
```

![在这里插入图片描述](../../image/20200527173958351.png)  
![在这里插入图片描述](../../image/2020052717400897.png)

### 3.二进制内置查看命令

 -    查看一目前有几个日志binlog

```bash
 show binary logs;
```

 -    查看当前在使用的binlog

```bash
 show master status;
```

 -    查看二进制事件

```bash
 show binlog events in 'mysql-bin.000001 ';
```

### binlog文件内容详细查看

```bash
- mysql  -uroot  -proot  -e  "show binlog events in 'mysql-bin.000001'"
- 普通查看  mysqlbinlog 

	- mysqlbinlog   /mysql/mysql/data/binlog/mysql-bin.000001 > a.sql   #把binlog到成sql文件

- 翻译查看

	- mysqlbinlog  --base64-output=decode-rows  -vvv /data/binlog/mysql-bin.000003

- 基于时间查看

	- mysqlbinlog  --start-datetime='2019-05-06 17:00:00'   --stop-datetime='2019-05-06 17:01:00'    /data/binlog/mysql-bin.000004 

- 基于Position号进行日志截取

	- mysqlbinlog  --start-position=219  --stop-position=1347  /data/binlog/mysql-bin.000003 >/tmp/bin.sql

- 数据恢复

-   set sql_log_bin=0;
	source /tmp/bin.sql
```

### binlog维护操作

**\- 1.日志滚动**

```
- flush logs；
- mysqladmin -uroot -proot flush-logs
- 自动滚动，默认1G滚动一次，可以设置参数
- select @@max_binlog_size;
- mysqldump -F
- 重启数据自动滚动
```

**\- 2.日志的删除**

```
- 注意：不要使用rm命令删除日志
- 自动删除（默认：0 永不删除，单位是天）

- select @@expire_logs_days; 

- 问题：到底设置多少天合适？    一个全备周期（7+1）天，一般生产一遍建议2个全备周期+1

- show variables like '%expire%';


expire_logs_days  0   
自动清理时间,是要按照全备周期+1
set global expire_logs_days=8;
永久生效:
my.cnf
expire_logs_days=15;
企业建议,至少保留两个全备周期+1的binlog
```

```bash
- 手工删除

		- PURGE BINARY LOGS TO 'mysql-bin.010';
		- PURGE BINARY LOGS BEFORE '2008-04-02 22:46:26';

	- 全部清空

		-  reset master;

			- 比较危险，在主从执行此操作，主从必宕机
```

## binlog日志的GTID新特性

### 1.GTID 介绍

```
- 5.6 版本新加的特性,5.7中做了加强
5.6 中不开启,没有这个功能.
5.7 中的GTID,即使不开也会有自动生成
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'

- 对于一个已提交事务的编号，并且是一个全局唯一的编号。
它的官方定义如下：

GTID = source_id ：transaction_id
7E11FA47-31CA-19E1-9E56-C43AA21293967:29
```

### 2.开启参数

```
开启的参数
    gtid-mode=on
	enforce-gtid-consistency=true
查看
- select @@gtid_mode;
```

![在这里插入图片描述](../../image/20200527174329550.png)

### 3.具备GTID后,截取查看某些事务日志

```
 --include-gtids
 --exclude-gtids
 --skip-gtids
```

### 4.数据截取

- `mysqlbinlog --skip-gtids --include-gtids='3ca79ab5-3e4d-11e9-a709-000c293b577e:1-9' mysql-bin.000002 mysql-bin.000003 > /tmp/gtid.sql`

### 5.数据恢复

```bash
set sql_log_bin=0;
source /tmp/bin.sql
```

## 慢日志\(slow-log\)

### 1 作用：记录运行较慢的语句,优化过程中常用的工具日志.

### 2.配置方法（默认没开启）

```
select @@slow_query_log;      #0表示关闭

select @@slow_query_log_file;     #文件存放文字
```

\*\* 开关:\*\*

```bash
slow_query_log=1 
```

**文件位置及名字**

```bash
slow_query_log_file=/data/mysql/slow.log
```

**设定慢查询时间:**

```bash
long_query_time=0.1
```

**没走索引的语句也记录:**

```c
log_queries_not_using_indexes
```

```bash
vim /etc/my.cnf
slow_query_log=1 
slow_query_log_file=/data/mysql/slow.log
long_query_time=0.1
log_queries_not_using_indexes
systemctl restart mysqld
```

### 3.mysqldumpslow 分析慢日志

 -    `mysqldumpslow -s c -t 10 /data/mysql/slow.log`
 -    # 第三方工具\(自己扩展\)

```bash
https://www.percona.com/downloads/percona-toolkit/LATEST/
yum install perl-DBI perl-DBD-MySQL perl-Time-HiRes perl-IO-Socket-SSL perl-Digest-MD5
```

```
- toolkit工具包中的命令:
```

```bash
./pt-query-diagest  /data/mysql/slow.log
Anemometer基于pt-query-digest将MySQL慢查询可视化
```

![在这里插入图片描述](../../image/20200527175023286.png)