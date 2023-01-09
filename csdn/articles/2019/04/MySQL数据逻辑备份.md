+++
author = "南宫乘风"
title = "MySQL数据逻辑备份"
date = "2019-04-20 21:20:34"
tags=[]
categories=['MySQL']
image = "post/4kdongman/26.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89422787](https://blog.csdn.net/heian_99/article/details/89422787)

逻辑备份： 备份的是建表、建库、插入等操作所执行SQL语句，适用于中小型数据库，效率相对较低。<br> mysqldump<br> mydumper<br><br>**使用mysqldump实现逻辑备份**

<br> 语法：<br> # mysqldump -h 服务器 -u用户名 -p密码 数据库名 &gt; 备份文件.sql

关于数据库名：<br> -A, --all-databases 所有库<br> school 数据库名<br> school stu_info t1 school数据库的表stu_info、t1<br> -B, --databases bbs test mysql 多个数据库<br> 关于其它参数说明：<br> --single-transaction     #基于此项可以实现对InnoDB表做热备份<br> -x, --lock-all-tables         #执行备份时为所有表请求加锁 MyISAM<br> -l, --lock-tables<br> -E, --events               #备份事件调度器代码<br> --opt                     #同时启动各种高级选项<br> -R, --routines             #备份存储过程和存储函数<br> -F, --flush-logs              #备份之前刷新日志<br> --triggers                #备份触发器<br> --master-data=2        #备库，该选项将会记录binlog的日志位置与文件名并追加到文件中，如果为1将会输出CHANGE MASTER命令，主从下有用<br> 注意：-B 作用：创建数据库和切换到数据库，恢复时不用创建数据库和删表。备份多个库，-B 数据库1 数据库2 .<br> -d只备份库结构，不包含数据内容<br> 备份：mysqldump -u 用户名 -p 数据库名 表名 &gt; 备份的文件名<br> 备份多个表：mysqldump -u 用户名 -p 数据库名 表名1 表名2 &gt; 备份的文件名

示例：

备份jiaowu数据库，名字为hei.sql

显示数据库

```
[root@wei ~]# mysql -uroot -proot -e 'show databases;'
```

![20190420202910838.png](https://img-blog.csdnimg.cn/20190420202910838.png)<br> 备份数据库

```
[root@wei ~]# mysqldump -uroot -proot jiaowu &gt;hei.sql

```

![20190420203308798.png](https://img-blog.csdnimg.cn/20190420203308798.png)

<br> ==备份==

```
[root@localhost ~]# mysqldump -uroot -proot --single-transaction --master-data=2 company &gt; /tmp/company_`date +%F-%H-%M`.sql
[root@localhost ~]# mysqldump -uroot -proot --single-transaction --master-data=2 school &gt; /tmp/school_`date +%F-%H-%M`.sql
[root@localhost ~]# mysqldump -uroot -proot --single-transaction --master-data=2 school |gzip &gt; /tmp/school_`date +%F-%H-%M`.gz
[root@localhost ~]# mysqldump -uroot -proot --routines --events --triggers --master-data=2 --flush-logs --all-databases &gt; /backup/all_`date +%F`.sql

```

![20190420204345705.png](https://img-blog.csdnimg.cn/20190420204345705.png)<br><br><br> ==恢复==

```
[root@localhost ~]# mysql -uroot -p888 -e 'create database school'
[root@localhost ~]# mysql -uroot -p888 school &lt; /tmp/school_2015-09-14-15-40.sql
root@(school)&gt; source /tmp/school_2015-09-14-15-40.sql
[root@localhost tmp]# gunzip -fc school_2015-09-14-15-09.gz | mysql -uroot -p888 school
```

<br><br> ==增量备份==<br>![2019042020225736.png](https://img-blog.csdnimg.cn/2019042020225736.png)

**增量备份前提：**

1）my.cnf，是要开启MySQL log-bin日志功能，重启MySQL      log_bin = /data/mysql/data/mysql-bin<br> 2）存在一个完全备份，生产环境一般凌晨某个时刻进行全备<br> 示例：

```
mysqldump -uroot -p --default-character-set=gbk --single-transaction -F -B school |gzip &gt; /server/backup/school_$(date +%F).sql.gz
```

<br> InnoDB 表在备份时，通常启用选项 --single-transaction 来保证备份的一致性<br><br> 增量备份--恢复过程<br> 1、检查凌晨备份<br> 2、检查全备后的所有binlog # ls -lrt /usr/local/mysql/data/mysql-bin.*<br> 3、立即刷新并备份出binlog mysqladmin -uroot -p flush-logs<br> cp /usr/local/mysql/data/mysql-bin.000004 /server/backup/<br> 提示：根据时间点及前一个binlog可以知道发现问题时刻前binlog日志为mysql-bin.000004<br> 4、恢复binlog生成sql语句mysqlbinlog mysql-bin.000004 &gt; bin.log<br> 5、恢复凌晨备份<br> 6、恢复增量备份<br><br> mysqlbinlog增量恢复方式<br> 基于时间点恢复<br> 1）指定开始时间到结束时间 myslbinlog mysqlbin.000008 --start-datetime=’2014-10-45 01:10:46’ --stop-datetime=’2014-10-45 03:10:46’-r time.sql<br> 2）指定开始时间到文件结束 myslbinlog mysqlbin.000008 --start-datetime=’2014-10-45 01:10:46’ -d esen -r time.sql<br> 3）从文件开头到指定结束时间 myslbinlog mysqlbin.000008 --stop-datetime=’2014-10-45 03:10:46’ -d esen -r time.sql<br> 基于位置点的增量恢复<br> 1）指定开始位置到结束位置 myslbinlog mysqlbin.000008 --start-position=510 --stop-position=1312 -r pos.sql<br> 2）指定开始位置到文件结束 myslbinlog mysqlbin.000008 --start-position=510 -r pos.sql<br> 3）从文件开始位置到指定结束位置 myslbinlog mysqlbin.000008 --stop-position=1312 -r pos.sql<br><br> ==恢复binlog==<br> 单库？全库

```
[root@localhost ~]# mysqlbinlog -d school localhost-bin.000002 --start-position=11574908 &gt; school-bin.sql
[root@localhost ~]# mysqlbinlog -d school localhost-bin.000003 &gt;&gt; school-bin.sql
[root@localhost ~]# mysqlbinlog -d school localhost-bin.000004 &gt;&gt; school-bin.sql
[root@localhost ~]# mysql -uroot -p888 school &lt; school-bin.sql

```

<br><br> 实现自动化备份（数据库小）<br> 备份计划：<br> 1. 什么时间 2:00<br> 2. 对哪些数据库备份<br> 3. 备份文件放的位置<br><br> 备份脚本：

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
mysqldump -u${user} -p${pass} --lock-all-tables --routines --events --triggers --master-data=2 --flush-logs --all-databases &gt; /$back_dir/$back_file

# 只保留最近一周的备份
cd $back_dir
find . -mtime +7 -exec rm -rf {} \;

```

<br> 手动测试：

```
[root@yang ~]# chmod a+x /mysql_back.sql
[root@yang ~]# chattr +i /mysql_back.sql
[root@yang ~]# /mysql_back.sql

```

<br> 配置cron：<br>  

```
[root@yang ~]# crontab -e
0 2 * * * /mysql_back.sql
```

### Mydumper介绍

<br> Mydumper是一个针对MySQL和Drizzle的高性能多线程备份和恢复工具。开发人员主要来自MySQL,Facebook,SkySQL公司。目前已经在一些线上使用了Mydumper。<br> Mydumper主要特性：<br> • 轻量级C语言写的<br> • 执行速度比mysqldump快10倍<br> • 事务性和非事务性表一致的快照(适用于0.2.2以上版本)<br> • 快速的文件压缩<br> • 支持导出binlog<br> • 多线程恢复(适用于0.2.1以上版本)<br> • 以守护进程的工作方式，定时快照和连续二进制日志(适用于0.5.0以上版本)<br> • 开源 (GNU GPLv3)<br>  

```
#wget https://launchpadlibrarian.net/225370879/mydumper-0.9.1.tar.gz
# yum -y install glib2-devel mysql-devel zlib-devel pcre-devel
[root@localhost ~]# tar xf mydumper-0.9.1.tar.gz -C /usr/local/src/
[root@localhost ~]# cd /usr/local/src/mydumper-0.9.1/
# cmake .
# make
# make install
```

<br><br> mydumper参数介绍：<br> -d, --directory 导入备份目录<br> -q, --queries-per-transaction 每次执行的查询数量, 默认1000<br> -o, --overwrite-tables 如果表存在删除表<br> -B, --database 需要备份的库<br> -T, --tables-list 需要备份的表，用，分隔<br> -o, --outputdir 输出目录<br> -s, --statement-size Attempted size of INSERT statement in bytes, default 1000000<br> -r, --rows 试图分裂成很多行块表<br> -c, --compress 压缩输出文件<br> -e, --build-empty-files 即使表没有数据，还是产生一个空文件<br> -x, --regex 支持正则表达式<br> -i, --ignore-engines 忽略的存储引擎，用，分隔<br> -m, --no-schemas 不导出表结构<br> -k, --no-locks 不执行临时共享读锁 警告：这将导致不一致的备份<br> -l, --long-query-guard 长查询，默认60s<br> --kill-long-queries kill掉长时间执行的查询(instead of aborting)<br> -b, --binlogs 导出binlog<br> -D, --daemon 启用守护进程模式<br> -I, --snapshot-interval dump快照间隔时间，默认60s，需要在daemon模式下<br> -L, --logfile 日志文件<br> -h, --host<br> -u, --user<br> -p, --password<br> -P, --port<br> -S, --socket<br> -t, --threads 使用的线程数，默认4<br> -C, --compress-protocol 在mysql连接上使用压缩<br> -V, --version<br> -v, --verbose 更多输出, 0 = silent, 1 = errors, 2 = warnings, 3 = info, default 2<br><br> mydumper输出文件：<br> metadata:元数据 记录备份开始和结束时间，以及binlog日志文件位置。<br> table data:每个表一个文件<br> table schemas:表结构文件<br> binary logs: 启用--binlogs选项后，二进制文件存放在binlog_snapshot目录下<br> daemon mode:在这个模式下，有五个目录0，1，binlogs，binlog_snapshot，last_dump。<br> 备份目录是0和1，间隔备份，如果mydumper因某种原因失败而仍然有一个好的快照，<br> 当快照完成后，last_dump指向该备份。<br><br>  

## mydumper用例

<br> ==备份==

```
#export LD_LIBRARY_PATH="/usr/local/mysql/lib:$LD_LIBRARY_PATH"
[root@localhost ~]# mydumper -h localhost -u root -p 123456 -t 6 -S /tmp/mysql.sock -B uplook -o /mysqlbackup/
[root@localhost ~]# ls /mysqlbackup/
metadata uplooking.Student-schema.sql uplook-schema-create.sql uplook.Student.sql
uplooking-schema-create.sql uplooking.Student.sql uplook.Student-schema.sql

** (mydumper:5247): CRITICAL **: Error connecting to database: Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)
```

<br> 解决方法：建立软连接

```
ln -sv /tmp/mysql.sock /var/lib/mysql/mysql.sock

[root@localhost ~]# cat /mysqlbackup/metadata
[root@localhost ~]# cat /mysqlbackup/metadata
Started dump at: 2017-08-05 15:48:09
Finished dump at: 2017-08-05 15:48:09

```

<br><br> ==恢复==

```
[root@localhost ~]# mysql -uroot -p -e 'drop database uplook;'
[root@localhost ~]# myloader -h localhost -u root -p 123456 -S /tmp/mysql.sock -d /mysqlbackup/ -o -B uplook
```

<br>  
