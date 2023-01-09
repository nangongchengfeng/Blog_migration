+++
author = "南宫乘风"
title = "MySQL基本库表管理"
date = "2019-04-16 12:43:20"
tags=[]
categories=['MySQL']
image = "post/4kdongman/29.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89331002](https://blog.csdn.net/heian_99/article/details/89331002)

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

### ** \! clear**

# <br>**<u>数据库基本管理操作</u>**

## **（1）查看数据库**

** **

```
show databases;

mysql&gt; show databases;
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

## <br>**（2）创建数据库**

**CREATE DATABASE &lt;db_name&gt; [CHARACTER=&lt;字符集&gt; COLLATE=&lt;排序规则&gt;]**

```
mysql&gt; create database game;
Query OK, 1 row affected (0.01 sec)
```

## ![20190416123455639.png](https://img-blog.csdnimg.cn/20190416123455639.png)<br>**(3)查看数据库的创建信息**

```
mysql&gt; show create database game;
+----------+-----------------------------------------------------------------+
| Database | Create Database                                                 |
+----------+-----------------------------------------------------------------+
| game     | CREATE DATABASE `game` /*!40100 DEFAULT CHARACTER SET latin1 */ |
+----------+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

## ![201904161235477.png](https://img-blog.csdnimg.cn/201904161235477.png)<br>**（4）查看mysql数据库支持的字符集**

** **

```
   mysql&gt; show character set;
```

![20190416123631307.png](https://img-blog.csdnimg.cn/20190416123631307.png)

## **（5）查看mysql数据库支持字符集的排序规则**

```
    mysql&gt; show collation;
```

## ![20190416123719340.png](https://img-blog.csdnimg.cn/20190416123719340.png)<br>**（6）删除数据库**

```
mysql&gt; drop database lol;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; show databases;
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
mysql&gt; use game
Database changed
```

## **示例：创建一个lol的数据库，字符集为utf8,排序为utf8_general_ci**

```
mysql&gt; create database lol 
    -&gt; character set=utf8
    -&gt; collate=utf8_general_ci;
Query OK, 1 row affected (0.00 sec)

mysql&gt; show create database lol;
    
+----------+--------------------------------------------------------------+
| Database | Create Database                                              |
+----------+--------------------------------------------------------------+
| lol      | CREATE DATABASE `lol` /*!40100 DEFAULT CHARACTER SET utf8 */ |
+----------+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

 

### **rpm默认数据目录**

**    /var/lib/mysql  -----&gt;数据目录：rpm默认数据目录**

**数据库一般存在数据目录下/var/lib/mysql **

```
[root@wei ~]# ls /var/lib/mysql
auto.cnf  game     ib_logfile0  lol    mysql.sock
farm      ibdata1  ib_logfile1  mysql  performance_schema
```

![20190416123906229.png](https://img-blog.csdnimg.cn/20190416123906229.png)

# **数据表的基本操作管理：**

## **（1）查看表**

 

```
mysql&gt; show tables;
+----------------+
| Tables_in_game |
+----------------+
| game_account   |
+----------------+
1 row in set (0.00 sec)
```

## **（2）创建表**

**CREATE TABLE &lt;表名&gt;(字段名称 数据类型 [属性],字段名称 数据类型 [属性]...)**

**数据类型：**

<img alt="" class="has" src="https://gss0.baidu.com/9fo3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D600%2C800/sign=b3e5187076ec54e741b912188908b768/08f790529822720e9e2977b476cb0a46f31fab9d.jpg">

**数值型**

<img alt="" class="has" src="https://gss0.baidu.com/-Po3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D600%2C800/sign=72f193848f8ba61edfbbc0297104bb32/ac345982b2b7d0a2cf3091d3c6ef76094a369a87.jpg"><br>**字符型**

<img alt="" class="has" src="https://gss0.baidu.com/-fo3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D600%2C800/sign=7296315d9adda144da5c64b48287fc9a/10dfa9ec8a1363271c91577d9c8fa0ec08fac704.jpg"><br>**日期/时间型**

<img alt="" class="has" src="https://gss0.baidu.com/9fo3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D600%2C800/sign=6b7013a09182d158bbd751b7b03a35e0/b3119313b07eca80df41aca99c2397dda144833c.jpg">

```
mysql&gt; create table game_account(
    -&gt; game_name char(15) not null,
    -&gt; game_passwd char(15) not null,
    -&gt; );
```

## **    <br> （3）查看创建表的信息**

```
mysql&gt; show create table game_account\G;
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
mysql&gt; drop table gam;
Query OK, 0 rows affected (0.01 sec)
```

## **（5）查看表结构**

```
mysql&gt; desc game_account;
+---------------+----------+------+-----+---------+-------+
| Field         | Type     | Null | Key | Default | Extra |
+---------------+----------+------+-----+---------+-------+
| game_name     | char(15) | NO   |     | NULL    |       |
| game_password | char(25) | NO   |     | NULL    |       |
+---------------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)
```

 
