+++
author = "南宫乘风"
title = "Xtrabackup工具进行在线主从搭建"
date = "2021-11-01 12:01:06"
tags=['mysql', '数据库', 'database']
categories=['MySQL']
image = "post/4kdongman/22.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/121077163](https://blog.csdn.net/heian_99/article/details/121077163)

在工作中，我们经常会使用mysql的主从，来去报数据的安全性。

首先目前主流的备份工作mysqldump和Xtrabackup，都可以实现数据库的备份。

关于那个用来备份数据，来做mysql主从，毫无疑问就是 Xtrabackup了。

首先MySQL做主从时，需要使用到binlog日志 和 pos号，关键就是这个pos。

如果是mysqldump来备份，需要进行锁表才行，如果是Xtrabackup 完全可以在任务运行中，进行备份，完全不需要锁表，更不会影响业务。所以我们首选就是Xtrabackup

相关原理，可以进行谷歌。

在这个只暂时先关步骤

## Mysql日志选择

### （1）mysql的binlog日志格式

mysql的binlog有3种日志格式。

[mysql](http://lib.csdn.net/base/mysql) binlog日志有三种格式，分别为Statement,MiXED,以及ROW！

查看binlog的格式的脚本：

![90d66f3df1f0a7fa84354614dfdad784.png](https://img-blog.csdnimg.cn/img_convert/90d66f3df1f0a7fa84354614dfdad784.png)

### （2）binlog 的不同模式有什么区别呢？ 

1.Statement：每一条会修改数据的sql都会记录在binlog中。

优点：不需要记录每一行的变化，减少了binlog日志量，节约了IO，提高性能。(相比row能节约多少性能与日志量，这个取决于应用的SQL情况，正常同一条记录修改或者插入row格式所产生的日志量还小于Statement产生的日志量，但是考虑到如果带条件的update操作，以及整表删除，alter表等操作，ROW格式会产生大量日志，因此在考虑是否使用ROW格式日志时应该跟据应用的实际情况，其所产生的日志量会增加多少，以及带来的IO性能问题。)

缺点：由于记录的只是执行语句，为了这些语句能在slave上正确运行，因此还必须记录每条语句在执行的时候的一些相关信息，以保证所有语句能在slave得到和在master端执行时候相同的结果。另外mysql 的复制,像一些特定函数功能，slave可与master上要保持一致会有很多相关问题(如sleep()函数， last_insert_id()，以及user-defined functions(udf)会出现问题).<br>  

2.Row:不记录sql语句上下文相关信息，仅保存哪条记录被修改。

优点： binlog中可以不记录执行的sql语句的上下文相关的信息，仅需要记录那一条记录被修改成什么了。所以rowlevel的日志内容会非常清楚的记录下每一行数据修改的细节。而且不会出现某些特定情况下的存储过程，或function，以及trigger的调用和触发无法被正确复制的问题

缺点:所有的执行的语句当记录到日志中的时候，都将以每行记录的修改来记录，这样可能会产生大量的日志内容,比如一条update语句，修改多条记录，则binlog中每一条修改都会有记录，这样造成binlog日志量会很大，特别是当执行alter table之类的语句的时候，由于表结构修改，每条记录都发生改变，那么该表每一条记录都会记录到日志中。

3.Mixedlevel: 是以上两种level的混合使用，一般的语句修改使用statment格式保存binlog，如一些函数，statement无法完成主从复制的操作，则采用row格式保存binlog,MySQL会根据执行的每一条具体的sql语句来区分对待记录的日志形式，也就是在Statement和Row之间选择一种.新版本的MySQL中队row level模式也被做了优化，并不是所有的修改都会以row level来记录，像遇到表结构变更的时候就会以statement模式来记录。至于update或者delete等修改数据的语句，还是会记录所有行的变更。



### （3）Binlog基本配制与格式设定

1.基本配制

Mysql BInlog日志格式可以通过mysql的my.cnf文件的属性binlog_format指定。如以下：

binlog_format           = MIXED                 //binlog日志格式

log_bin                     =目录/mysql-bin.log    //binlog日志名

expire_logs_days     = 7                //binlog过期清理时间

max_binlog_size      100m                    //binlog每个日志文件大小



2.Binlog日志格式选择

Mysql默认是使用Statement日志格式，推荐使用MIXED.

由于一些特殊使用，可以考虑使用ROWED，如自己通过binlog日志来同步数据的修改，这样会节省很多相关操作。对于binlog数据处理会变得非常轻松,相对mixed，解析也会很轻松(当然前提是增加的日志量所带来的IO开销在容忍的范围内即可)。 

```
1.先修改从库的binlog格式
set global binlog_format=MIXED;
2.再修改主库的binlog格式
set global binlog_format=MIXED;
3.修改主库的my.cnf(避免重启失效)
binlog_format=MIXED
4.重启stop slave，start slave
```

## 2、主备库均安装Xtrabackup开源工具在线热备份搭建备库



```
#下载工具包percona-xtrabackup-2.4.14-Linux-x86_64.libgcrypt183.tar.gz

tar -xf percona-xtrabackup-2.4.14-Linux-x86_64.libgcrypt183.tar.gz
mv percona-xtrabackup-2.4.14-Linux-x86_64 xtrabackup
mv xtrabackup/ /usr/local/
echo "export PATH=$PATH:/usr/local/xtrabackup/bin" &gt;&gt; /etc/profile
source /etc/profile
```

## 3、主库在线备份(不影响业务)

```
innobackupex --user='root' --password='xxxxxx' --slave-info /data1/backup/20210927 --no-timestamp --socket=/tmp/mysql.sock

#以下是输出结果:
xtrabackup: recognized server arguments: --server-id=1 --log_bin=binlog --datadir=/data1/mysql/data/ --tmpdir=/tmp 
xtrabackup: recognized client arguments: --server-id=1 --log_bin=binlog --datadir=/data1/mysql/data/ --tmpdir=/tmp 
200615 16:26:27 innobackupex: Starting the backup operation

IMPORTANT: Please check that the backup run completes successfully.
           At the end of a successful backup run innobackupex
           prints "completed OK!".
         ..........
xtrabackup: Transaction log of lsn (5055292518) to (5055292527) was copied.
200615 16:26:30 completed OK!
```

## 4、检查全备的POS

```
cat /data/backup/20200615/xtrabackup_binlog_info
binlog.000002   184668420
```

## 5、将备份文件压缩传输到备机上

```
cd /data1/backup/
tar -zcf 20210927.tar.gz  20210927
scp 20210927.tar.gz  dam@dam02:/home/dam/
```

## 6、停止备库,将原来的备库datadir的路径重命名并创建新的数据data目录

```
/etc/init.d/mysqld stop
cd  /data1/mysql
mv data  data3
mkdir data
```

## 7、解压缩备份文件并恢复数据到新的data目录

```
tar -xf  20210927.tar.gz  -C /data1/mysql/

#数据一致性恢复
innobackupex --apply-log /data1/mysql/20210927
#数据copy到dir目录
innobackupex --copy-back /data1/mysql/20210927

chown -R mysql.mysql /data1/mysql/data
chmod -R 775 /data1/mysql/data
```

## 8、重启备机228的mysql

```
/etc/init.d/mysqld stop
/etc/init.d/mysqld start
```

## 9、配置主从同步

```
#227主机创建同步用户:
create  USER 'xxxx'@'172.17.8.%' IDENTIFIED WITH mysql_native_password BY 'xxxxxx';
grant replication slave on *.* to 'syncuser'@'172.17.8.%';
flush privileges;

#228配置备机：
reset slave all; 
stop slave;
change master to master_host='172.17.8.227',master_port=3306,master_user='syncuser',master_password='xxxxx',master_log_file='binlog.000002',master_log_pos=184668420;
start slave;
show slave status\G;
show master status\G;
```

## 10、为解决msyql主从延迟问题进行的相关调优：

```
#主从并行复制参数：
vim my.cnf
master_info_repository=TABLE                   #master信息放到表里      
relay_log_info_repository=TABLE                #relay日志信息放到表里      
slave_parallel_type = LOGICAL_CLOCK            #基于组提交的并行复制方式
slave_parallel_workers=8                       #sql并行量
slave_preserve_commit_order=ON                  #relay顺序与master并行顺序保持一致
relay_log_recovery=ON                          #宕机时重新从master获取日志，保证relay完整性
replicate-wild-ignore-table=scheduler.tb_qa%   #不同步scheduler.tb_qa开头的表
replicate-wild-ignore-table=scheduler.tb_qc%   #不同步scheduler.tb_qc开头的表										   
stop slave;

set global master_info_repository='table';
set global relay_log_info_repository='table';
set global slave_parallel_type='logical_clock';
set global slave_parallel_workers=8;
set global slave_preserve_commit_order='on';
set global relay_log_recovery='on';

start slave;
```

![50e66a7d6f4d45aea6a78b1f17d3e9a6.png](https://img-blog.csdnimg.cn/50e66a7d6f4d45aea6a78b1f17d3e9a6.png)
