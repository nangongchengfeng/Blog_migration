---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-26 21:07:54
description: 实现主从复制读写分离的安装及部署、部署环境用开发，需要有运行环境，依赖的环境上传月安装设置环境变量内容如下：使环境变量当前终端生效测试、安装上传包月解压解压后内容如下：总用量月月月月月月添加环境变量、。。。。。。。
image: http://image.ownit.top/4kdongman/86.jpg
tags:
- 技术记录
title: MySQL读写分离之MyCAT
---

<!--more-->

Mycat实现MySQL主从复制读写分离  
  
  
MyCAT的安装及部署  
  
1、部署jdk环境  
MyCAT用Java开发，需要有JAVA运行环境，mycat依赖jdk1.7的环境  
1）上传jdk

```
[root@localhost tools]# ll jdk-7u45-linux-x64.tar.gz
-rw-r--r-- 1 root root 138094686 10月 24 2013 jdk-7u45-linux-x64.tar.gz
```

  
  
2）安装jdk

```
[root@localhost tools]# mkdir /usr/java
[root@localhost tools]# tar xf jdk-7u45-linux-x64.tar.gz -C /usr/java/
```

  
  
3）设置环境变量

```
[root@localhost tools]# vim /etc/profile.d/java.sh
```

  
内容如下：

```
export JAVA_HOME=/usr/java/jdk1.7.0_45/
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```

  
  
使环境变量当前终端生效

```
[root@localhost tools]# source /etc/profile.d/java.sh
```

  
  
4）测试

```
[root@localhost tools]# java -version
java version "1.7.0_45"
Java(TM) SE Runtime Environment (build 1.7.0_45-b18)
Java HotSpot(TM) 64-Bit Server VM (build 24.45-b08, mixed mode)
```

  
  
2、安装Mycat  
1）上传mycat包

```
[root@localhost tools]# ll Mycat-server-1.5.1-RELEASE-20161130213509-linux.tar.gz
-rw-r--r--. 1 root root 11499865 12月 15 16:33 Mycat-server-1.5.1-RELEASE-20161130213509-linux.tar.gz
```

  
  
  
2）解压

```
[root@localhost tools]# tar xf Mycat-server-1.5.1-RELEASE-20161130213509-linux.tar.gz -C /usr/local/
```

  
  
解压后内容如下：

```
[root@localhost tools]# ll /usr/local/mycat
```

  
总用量 16

```
drwxr-xr-x 2 root root 4096 12月 15 11:36 bin
drwxrwxrwx 2 root root 6 3月 1 2016 catlet
drwxrwxrwx 4 root root 4096 12月 15 11:36 conf
drwxr-xr-x 2 root root 4096 12月 15 11:36 lib
drwxrwxrwx 2 root root 6 10月 28 20:47 logs
-rwxrwxrwx 1 root root 217 10月 28 20:47 version.txt
```

  
  
3）添加环境变量

```
[root@localhost tools]# vim /etc/profile.d/mycat.sh
export PATH=$PATH:/usr/local/mycat/bin

[root@localhost tools]# source /etc/profile.d/mycat.sh
```

  
  
  
3、读写分离配置  
1）不使用Mycat托管MySQL主从服务器，简单使用如下配置  
#注意：配置前备份下配置文件

```
[root@localhost tools]# cd /usr/local/mycat/conf
[root@localhost conf]# cp schema.xml{,.bak}
```

>   
>   
> \(1\)\<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="dn1">  
> 这里的TESTDB就是我们所宣称的数据库名称，必须和server.xml中的用户指定的数据库名称一致。添加一个dataNode="dn1"，是指定了我们这个库只有在dn1上，没有分库。  
>   
> \(2\)\<dataNode name="dn1" dataHost="localhost1" database="db1" />  
> 这里只需要改database的名字，就是你真是的数据库上的数据库名，可根据自己的数据库名称修改。  
>   
> \(3\) \<dataHost name="localhost1" maxCon="1000" minCon="10" balance="1"  
> writeType="0" dbType="mysql" dbDriver="native" switchType="1" slaveThreshold="100">  
>   
> 需要配置的位置：  
> balance="1" writeType="0" switchType="1"  
>   
> balance  
> 1、balance=0 不开启读写分离机制，所有读操作都发送到当前可用的writehostle .  
>   
> 2、balance=1 全部的readhost与stand by writeHost 参与select语句的负载均衡。简单的说，双主双从模式\(M1->S1,M2->S2，并且M1和M2互为主备\)，正常情况下，M1，S1，S2都参与select语句的复杂均衡。  
>   
> 3、balance=2 所有读操作都随机的在readhost和writehost上分发  
>   
> writeType  
> 负载均衡类型，目前的取值有3种：  
> 1、writeType="0", 所有写操作发送到配置的第一个writeHost。  
> 2、writeType="1"，所有写操作都随机的发送到配置的writeHost。  
> 3、writeType="2"，不执行写操作。  
>   
> switchType  
> 1、switchType=-1 表示不自动切换  
> 2、switchType=1 默认值，自动切换  
> 3、switchType=2 基于MySQL 主从同步的状态决定是否切换

> \(4\)\<writeHost host="hostM1" url="192.168.95.120:3306" user="mycat" password="123456">
> 
> \<\!– can have multi read hosts –>
> 
> \<readHost host="hostS2" url="192.168.95.140:3306" user="mycat\_r" password="123456" />
> 
> \<readHost host="hostS3" url="192.168.95.140:3307" user="mycat\_r" password="123456" />
> 
> \<\!--\<writeHost host="hostS1" url="localhost:3316" user="root"
> 
> password="123456" />-->

  
  
配置好文件内容如下:

```
<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">
<mycat:schema xmlns:mycat="http://org.opencloudb/" >


<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="dn1">
</schema>
<dataNode name="dn1" dataHost="localhost1" database="db1" />
<dataHost name="localhost1" maxCon="1000" minCon="10" balance="1"
writeType="0" dbType="mysql" dbDriver="native" switchType="1" slaveThreshold="100">
<heartbeat>select user()</heartbeat>
<writeHost host="hostM1" url="192.168.95.120:3306" user="root"
password="123456">
<readHost host="hostR1" url="192.168.95.140:3306" user="root" password="123456" />
<readHost host="hostR2" url="192.168.95.140:3307" user="root" password="123456" />
</writeHost>
</dataHost>
</mycat:schema>
```

  
4、创建管理用户  
主库上对mycat用户授权如下：  
  
用户：mycat 密码：123456 端口：3306  
  
权限：insert,delete,update,select  
  
命令：grant insert,delete,update,select on TD\_OA.\* to mycat\@'192.168.95.\%' identified by '123456';  
flush privileges;  
  
从库上mycat\_r用户授权如下：  
用户：mycat\_r 密码：123456 端口：3306/3307  
权限： select  
  
grant select on TD\_OA.\* to mycat\@'192.168.95.\%' identified by '123456';  
flush privileges;  
  
测试环境可以直接使用root用户，授予所有权限：

```
mysql> grant all on *.* to root@'192.168.95.%' identified by '123456';
Query OK, 0 rows affected (0.00 sec)

mysql> grant all on *.* to root@'localhost' identified by '123456';
```

  
  
  
5、修改mycat配置文件  
采用默认配置  
  
注意：  
  
①这里配置的是可以连接主库的两个用户  
  
用户：test 密码：test 给予此用户TESTDB数据库增删改查的权限。  
  
用户：user 密码：password 给予此用户TESTDB数据库读的权限。  
  
②这里的TESTDB，不一定是你数据库上的真实库名，可以任意指定，只要接下来和schema.xml的配置文件的库名统一即可。  
  
6、启动Mycat  
方法一：# mycat console #\<=通过console命令启动mycat，这样方便提取信息  
方法二：# mycat start  
方法三：# startup\_nowrap.sh #服务脚本方式启动  
  
  
\[root\@localhost conf\]# netstat \-lnupt | egrep "\(8|9\)066"  
tcp6 0 0 :::9066 :::\* LISTEN 3342/java  
tcp6 0 0 :::8066 :::\* LISTEN 3342/java  
  
重启：# mycat restart  
  
7、在客户端连接mysql主库服务器：  
 

```
# mysql -uuser -puser -h192.168.95.130 -P8066 -DTESTDB
Warning: Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.6.29-mycat-1.6-RELEASE-20161028204710 MyCat Server (OpenCloundDB)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

  
8、主从同步读写分离测试  
管理端创建表:

```
[root@localhost ~]# mysql -utest -ptest -h192.168.95.130 -P8066 -DTESTDB
CREATE TABLE test1 (id int(10),name varchar(10),address varchar(20) DEFAULT NULL);
```

  
  
手动停止主从同步: stop slave;  
  
分别在主从库插入数据:  
**master: insert into test1 values\(1,'test1','master'\);  
  
slave1: insert into test1 values\(2,'test1','slave1'\);  
slave2: insert into test1 values\(3,'test1','slave2'\);**  
  
管理端验证  
负载均衡:

```
mysql> select * from test1;
+------+-------+---------+
| id | name | address |
+------+-------+---------+
| 2 | test1 | slave1 |
+------+-------+---------+
1 row in set (0.00 sec)

mysql> select * from test1;
+------+-------+---------+
| id | name | address |
+------+-------+---------+
| 3 | test1 | slave2 |
+------+-------+---------+
1 row in set (0.00 sec)
```

  
  
读写功能:  
管理端再次插入数据 insert into test1 values\(4,'test1','write'\);

```
mysql> insert into test1 values(4,'test1','write');
Query OK, 1 row affected (0.00 sec)
```

  
#注意：测试完毕启动主从同步功能。  
  
9、管理命令与监控  
mycat自身有类似其他数据库的管理监控方式，可通过mysql命令行，登陆端口9066执行相应的SQL操作，也可通过jdbc的方式进行远程连接管理。  
  
登录：目前mycat有两个端口，8066数据端口，9066管理端口。命令行登录时通过9066管理端口来执行：

```
# mysql -uuser -puser -h192.168.95.130 -P9066 -DTESTDB
Warning: Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.6.29-mycat-1.6-RELEASE-20161028204710 MyCat Server (monitor)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

  
  
选项：  
  
\-h 后面接主机  
  
\-u mycat server.xml配置的逻辑库用户  
  
\-p mycat server.xml配置的逻辑库密码  
  
\-P 后面接的端口9066，注意P大写  
  
  
\-D Mycat server.xml中配置的逻辑库  
  
1）查看所有的命令，如下：

```
mysql> show @@help;
```

  
  
2）显示mycat数据库的列表，对应的在scehma.xml配置的逻辑库

```
mysql> show @@databases;
+----------+
| DATABASE |
+----------+
| TESTDB |
+----------+
1 row in set (0.00 sec)
```

  
  
3）显示mycat数据节点的列表，对应的是scehma.xml配置文件的dataNode节点

```
mysql> show @@datanode;
+------+----------------+-------+-------+--------+------+------+---------+------------+----------+---------+---------------+
| NAME | DATHOST | INDEX | TYPE | ACTIVE | IDLE | SIZE | EXECUTE | TOTAL_TIME | MAX_TIME | MAX_SQL | RECOVERY_TIME |
+------+----------------+-------+-------+--------+------+------+---------+------------+----------+---------+---------------+
| dn1 | localhost1/db1 | 0 | mysql | 0 | 0 | 1000 | 0 | 0 | 0 | 0 | -1 |
| dn2 | localhost1/db2 | 0 | mysql | 0 | 0 | 1000 | 0 | 0 | 0 | 0 | -1 |
| dn3 | localhost1/db3 | 0 | mysql | 0 | 0 | 1000 | 0 | 0 | 0 | 0 | -1 |
+------+----------------+-------+-------+--------+------+------+---------+------------+----------+---------+---------------+
3 rows in set (0.00 sec)
```

  
其中，NAME表示datanode的名称；dataHost 对应的是dataHost属性的值，数据主机的名称，ACTIVE表示活跃的连接数，IDIE表示闲置的连接数，SIZE对应的是总连接的数量。  
 

```
mysql> show @@heartbeat;
+--------+-------+----------------+------+---------+-------+--------+---------+--------------+---------------------+-------+
| NAME | TYPE | HOST | PORT | RS_CODE | RETRY | STATUS | TIMEOUT | EXECUTE_TIME | LAST_ACTIVE_TIME | STOP |
+--------+-------+----------------+------+---------+-------+--------+---------+--------------+---------------------+-------+
| hostM1 | mysql | 192.168.95.120 | 3306 | 1 | 0 | idle | 0 | 1,0,0 | 2016-12-15 14:25:35 | false |
| hostS2 | mysql | 192.168.95.140 | 3306 | 1 | 0 | idle | 0 | 1,1,1 | 2016-12-15 14:25:35 | false |
| hostS3 | mysql | 192.168.95.140 | 3307 | 1 | 0 | idle | 0 | 1,1,1 | 2016-12-15 14:25:35 | false |
+--------+-------+----------------+------+---------+-------+--------+---------+--------------+---------------------+-------+
3 rows in set (0.01 sec)
```

  
RS\_CODE状态为1，正常状态  
  
4、获取当前mycat的版本

```
mysql> show @@version;
```

  
5、显示mycat前端连接状态

```
mysql> show @@connection;
```

  
6、显示mycat后端连接状态

```
mysql> show @@backend;
```

  
7、显示数据源  
 

```
mysql> show @@datasource
```