+++
author = "南宫乘风"
title = "MySQL日志管理"
date = "2019-04-19 23:49:26"
tags=[]
categories=['MySQL']
image = "post/4kdongman/14.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89409908](https://blog.csdn.net/heian_99/article/details/89409908)

### **MySQL日志管理**

 

========================================================
- 错误日志: 记录 MySQL 服务器启动、关闭及运行错误等信息- 二进制日志: 又称binlog日志，以二进制文件的方式记录数据库中除 SELECT 以外的操作- 查询日志: 记录查询的信息- 慢查询日志: 记录执行时间超过指定时间的操作- 中继日志： 备库将主库的二进制日志复制到自己的中继日志中，从而在本地进行重放- 通用日志： 审计哪个账号、在哪个时段、做了哪些事件- 事务日志 或称redo日志，记录Innodb事务相关的如事务执行时间、检查点等
========================================================
|日志类型|记录信息
|日志文件|记入文件中的信息类型
|错误日志|记录启动、运行或停止时出现的问题。
|查询日志|记录建立的客户端连接和执行的语句。
|二进制日志|记录所有更改数据的语句。主要用于复制和即时点恢复。
|慢日志|记录所有执行时间超过long_query_time秒的所有查询或不使用索引的查询。
|事务日志|记录InnoDB等支持事务的存储引擎执行事务时产生的日志。

### <br><br><br> 一、错误日志

<br> 错误日志主要记录如下几种日志：<br> 服务器启动和关闭过程中的信息<br> 服务器运行过程中的错误信息<br> 事件调度器运行一个时间是产生的信息<br> 在从服务器上启动从服务器进程是产生的信息<br><br> 错误日志定义：可以用--log-error[=file_name]选项来指定mysqld保存错误日志文件的位置。<br> 如果没有给定file_name值，mysqld使用错误日志名host_name.err 并在数据目录中写入日志文件。如果你执行FLUSH LOGS，错误日志用-old重新命名后缀并且mysqld创建一个新的空日志文件。(如果未给出--log-error选项，则不会重新命名）。<br> 查看当前错误日志配置 mysql&gt; SHOW GLOBAL VARIABLES LIKE '%log_error%';

![20190419233639750.png](https://img-blog.csdnimg.cn/20190419233639750.png)<br> 是否记录警告日志 mysql&gt; SHOW GLOBAL VARIABLES LIKE '%log_warnings%';<br>![20190419233703307.png](https://img-blog.csdnimg.cn/20190419233703307.png)<br> 二、bin-log<br> 1. 启用<br> # vim /etc/my.cnf<br> [mysqld]<br> log-bin[=dir/[filename]] //目录权限必须mysql用户可写<br> # service mysqld restart<br><br> 注意：MySQL 5.7.3以后版本，启用bin-log功能，需要设置server-id<br> 2. 暂停<br> //仅当前会话<br> SET SQL_LOG_BIN=0;<br> SET SQL_LOG_BIN=1;<br><br> 3. 查看<br> 查看二进制日志的工具为：mysqlbinlog<br><br> 二进制日志包含了所有更新了数据或者已经潜在更新了数据（例如，没有匹配任何行的一个DELETE）的所有语句语句<br> 以“事件”的形式保存，它描述数据更改。二进制日志还包含关于每个更新数据库的语句的执行时间信息。它不包含没有修改任何数据的语句<br> 二进制日志的主要目的是在数据库存在故障时，恢复时能够最大可能地更新数据库（即时点恢复），因为二进制日志包含备份后进行的所有更新。<br> 二进制日志还用于在主复制服务器上记录所有将发送给从服务器的语句。<br><br> 查看全部：

```
# mysqlbinlog mysql.000002
```

![20190419234857667.png](https://img-blog.csdnimg.cn/20190419234857667.png)<br><br> 按时间：

```
# mysqlbinlog mysql.000002 --start-datetime="2012-12-05 10:02:56"

# mysqlbinlog mysql.000002 --stop-datetime="2012-12-05 11:02:54"

# mysqlbinlog mysql.000002 --start-datetime="2012-12-05 10:02:56" --stop-datetime="2012-12-05 11:02:54"


```

<br> 按字节数：

```
# mysqlbinlog mysql.000002 --start-position=260
# mysqlbinlog mysql.000002 --stop-position=260
# mysqlbinlog mysql.000002 --start-position=260 --stop-position=930

```

<br> 4. 截断bin-log（产生新的bin-log文件）<br> a. 重启mysql服务器<br> b. # mysql -uroot -p123 -e 'flush logs'<br><br> 5. 删除bin-log文件<br> # mysql -uroot -p123 -e 'reset master'<br> 二进制日志文件不能直接删除的，如果使用rm等命令直接删除日志文件，可能导致数据库的崩溃。<br> 必须使用命令PURGE删除日志，语法如下：PURGE { BINARY | MASTER } LOGS { TO 'log_name' | BEFORE datetime_expr }<br><br> 三、查询日志<br> 启用通用查询日志

```
# vim /etc/my.cnf
[mysqld]
log[=dir\[filename]]
# service mysqld restart
```

<br><br><br> 四、慢查询日志<br> 启用慢查询日志

```
# vim /etc/my.cnf
[mysqld]
log-slow-queries[=dir\[filename]]
long_query_time=n
# service mysqld restart
```

<br>  

```
MySQL 5.6:
slow-query-log=1
slow-query-log-file=slow.log
long_query_time=3
```

<br><br> 查看慢查询日志<br> 测试:BENCHMARK(count,expr)<br> SELECT BENCHMARK(50000000,2*3);<br><br> 默认与慢查询相关变量：mysql&gt; SHOW GLOBAL VARIABLES LIKE '%slow_query_log%';<br> 默认没有启用慢查询，为了服务器调优，建议开启<br> 开启方法：SET GLOBAL slow_query_log=ON;<br> 当前生效，永久有效配置文件中设置<br> 使用mysqldumpslow命令获得日志中显示的查询摘要来处理慢查询日志<br> # mysqldumpslow slow.log 那么多久算是慢呢？如果查询时长超过long_query_time的定义值（默认10秒），即为慢查询：<br>  

```
mysql&gt; SHOW GLOBAL VARIABLES LIKE 'long_query_time';
```

 
