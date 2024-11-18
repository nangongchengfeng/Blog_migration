---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-16 18:55:22
description: 语句数据定义语言，数据操纵语言，，，数据控制语言，使用修改表结构修改表名表名新表名修改表的搜索引擎查看表的信息添加字段表名字段名称字段定义后面添加：前面添加：中间添加：删除字段表名字段名称修改字段名称。。。。。。。
image: http://image.ownit.top/4kdongman/58.jpg
tags:
- 技术记录
title: MySQL使用alter修改表的结构
---

<!--more-->

> ## **SQL语句**
> 
> ### **    DLL        数据定义语言**
> 
> **        create，drop**
> 
> ### **    DML     数据操纵语言**
> 
> **        insert，delete，select，update**
> 
> ### **    DCL        数据控制语言**
> 
> **        grant，revoke**

#           
使用ALTER TABLE修改表结构

## **（1）修改表名**

ALTER TABLE \<表名> RENAME \<新表名>

```
mysql> alter table game_account rename account;
Query OK, 0 rows affected (0.05 sec)
```

## **（2）修改表的搜索引擎**

```
mysql> alter table account engine=MyISAM;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

###   
**查看表的信息**

```
mysql> show create table account\G;
*************************** 1. row ***************************
       Table: account
Create Table: CREATE TABLE `account` (
  `game_name` char(15) NOT NULL,
  `game_password` char(25) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
ERROR: 
No query specified
```

## **（3）添加字段**

ALTER TABLE \<表名> ADD \<字段名称> \<字段定义>

### 后面添加：

```
mysql> alter table account add game_sex enum("M","F") not null;
```

###   
      
前面添加：

```
mysql> alter table account add game_address varchar(20) not null default "huabei" first;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## 中间添加：

```
mysql> alter table account add game_money int after game_name;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

##   
**（4）删除字段**

ALTER TABLE \<表名> drop \<字段名称>

```
mysql> alter table account drop game_wei;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## **（5）修改字段名称及字段定义**

ALTER TABLE \<表名> CHANGE \<旧字段> \<新字段名称> \<字段定义>

```
mysql> alter table account change game_zhang wei char(25) not null;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```
mysql> alter table account change wei wei varchar(60)  ;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

##   
**（6）修改字段定义**

ALTER TABLE \<表名> MODIFY \<字段名称> \<字段定义>

```
mysql> alter table account modify wei int ;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

 

```
mysql> alter table account modify wei int  not null ;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```