---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-16 12:43:20
description: 基本管理指令登陆第一种第二种带参输入注意：每个命令后面必须加里面清屏数据库基本管理操作查看数据库创建数据库字符集排序规则查看数据库的创建信息查看数据库支持的字符集查看数据库支持字符集的排序规则删除数据。。。。。。。
image: http://image.ownit.top/4kdongman/14.jpg
tags:
- 技术记录
title: MySQL基本库表管理
---

<!--more-->

# **基本管理指令**

### **mysql登陆**

**第一种**

```
[root@wei ~]# mysql -u root -p
```

**第二种（带参输入）**

```
[root@wei ~]# mysql -uroot -proot
```

**注意：每个命令后面必须加;**

### **mysql里面清屏**

### ** \\\! clear**

#   
**数据库基本管理操作**

## **（1）查看数据库**

```
show databases;

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| farm               |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (0.00 sec)
```

##   
**（2）创建数据库**

**CREATE DATABASE \<db\_name> \[CHARACTER=\<字符集> COLLATE=\<排序规则>\]**

```
mysql> create database game;
Query OK, 1 row affected (0.01 sec)
```

## ![](http://image.ownit.top/csdn/20190416123455639.png)  
**\(3\)查看数据库的创建信息**

```
mysql> show create database game;
+----------+-----------------------------------------------------------------+
| Database | Create Database                                                 |
+----------+-----------------------------------------------------------------+
| game     | CREATE DATABASE `game` /*!40100 DEFAULT CHARACTER SET latin1 */ |
+----------+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

## ![](http://image.ownit.top/csdn/201904161235477.png)  
**（4）查看mysql数据库支持的字符集**

```
   mysql> show character set;
```

![](http://image.ownit.top/csdn/20190416123631307.png)

## **（5）查看mysql数据库支持字符集的排序规则**

```
    mysql> show collation;
```

## ![](http://image.ownit.top/csdn/20190416123719340.png)  
**（6）删除数据库**

```
mysql> drop database lol;
Query OK, 0 rows affected (0.00 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| farm               |
| game               |
| mysql              |
| performance_schema |
+--------------------+
5 rows in set (0.00 sec)
```

## **（7）切换数据库**

```
mysql> use game
Database changed
```

## **示例：创建一个lol的数据库，字符集为utf8,排序为utf8\_general\_ci**

```
mysql> create database lol 
    -> character set=utf8
    -> collate=utf8_general_ci;
Query OK, 1 row affected (0.00 sec)

mysql> show create database lol;
    
+----------+--------------------------------------------------------------+
| Database | Create Database                                              |
+----------+--------------------------------------------------------------+
| lol      | CREATE DATABASE `lol` /*!40100 DEFAULT CHARACTER SET utf8 */ |
+----------+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

 

### **rpm默认数据目录**

**    /var/lib/mysql  \----->数据目录：rpm默认数据目录**

**数据库一般存在数据目录下/var/lib/mysql **

```
[root@wei ~]# ls /var/lib/mysql
auto.cnf  game     ib_logfile0  lol    mysql.sock
farm      ibdata1  ib_logfile1  mysql  performance_schema
```

![](http://image.ownit.top/csdn/20190416123906229.png)

# **数据表的基本操作管理：**

## **（1）查看表**

 

```
mysql> show tables;
+----------------+
| Tables_in_game |
+----------------+
| game_account   |
+----------------+
1 row in set (0.00 sec)
```

## **（2）创建表**

**CREATE TABLE \<表名>\(字段名称 数据类型 \[属性\],字段名称 数据类型 \[属性\]...\)**

**数据类型：**

![](http://image.ownit.top/csdn/08f790529822720e9e2977b476cb0a46f31fab9d.jpg)

**数值型**

![](http://image.ownit.top/csdn/ac345982b2b7d0a2cf3091d3c6ef76094a369a87.jpg)  
**字符型**

![](http://image.ownit.top/csdn/10dfa9ec8a1363271c91577d9c8fa0ec08fac704.jpg)  
**日期/时间型**

![](http://image.ownit.top/csdn/b3119313b07eca80df41aca99c2397dda144833c.jpg)

```
mysql> create table game_account(
    -> game_name char(15) not null,
    -> game_passwd char(15) not null,
    -> );
```

## **      
（3）查看创建表的信息**

```
mysql> show create table game_account\G;
*************************** 1. row ***************************
       Table: game_account
Create Table: CREATE TABLE `game_account` (
  `game_name` char(15) NOT NULL,
  `game_password` char(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
ERROR: 
No query specified
```

## **（4）删除表**

```
mysql> drop table gam;
Query OK, 0 rows affected (0.01 sec)
```

## **（5）查看表结构**

```
mysql> desc game_account;
+---------------+----------+------+-----+---------+-------+
| Field         | Type     | Null | Key | Default | Extra |
+---------------+----------+------+-----+---------+-------+
| game_name     | char(15) | NO   |     | NULL    |       |
| game_password | char(25) | NO   |     | NULL    |       |
+---------------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)
```