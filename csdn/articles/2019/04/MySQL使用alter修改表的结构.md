+++
author = "南宫乘风"
title = "MySQL使用alter修改表的结构"
date = "2019-04-16 18:55:22"
tags=[]
categories=['MySQL']
image = "post/4kdongman/05.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89339520](https://blog.csdn.net/heian_99/article/details/89339520)

>  
 <h2>**SQL语句**</h2> 
 <h3>**    DLL        数据定义语言**</h3> 
 **        create，drop** 
 <h3>**    DML     数据操纵语言**</h3> 
 **        insert，delete，select，update** 
 <h3>**    DCL        数据控制语言**</h3> 
 **        grant，revoke** 


### **    DML     数据操纵语言**

#         <br>使用ALTER TABLE修改表结构

## **（1）修改表名**

ALTER TABLE &lt;表名&gt; RENAME &lt;新表名&gt;

```
mysql&gt; alter table game_account rename account;
Query OK, 0 rows affected (0.05 sec)
```

## **（2）修改表的搜索引擎**

```
mysql&gt; alter table account engine=MyISAM;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### <br>**查看表的信息**

```
mysql&gt; show create table account\G;
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

ALTER TABLE &lt;表名&gt; ADD &lt;字段名称&gt; &lt;字段定义&gt;

### 后面添加：

```
mysql&gt; alter table account add game_sex enum("M","F") not null;
```

### <br>     <br>前面添加：

```
mysql&gt; alter table account add game_address varchar(20) not null default "huabei" first;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## 中间添加：

```
mysql&gt; alter table account add game_money int after game_name;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## <br>**（4）删除字段**

ALTER TABLE &lt;表名&gt; drop &lt;字段名称&gt;

```
mysql&gt; alter table account drop game_wei;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## **（5）修改字段名称及字段定义**

ALTER TABLE &lt;表名&gt; CHANGE &lt;旧字段&gt; &lt;新字段名称&gt; &lt;字段定义&gt;

```
mysql&gt; alter table account change game_zhang wei char(25) not null;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```
mysql&gt; alter table account change wei wei varchar(60)  ;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## <br>**（6）修改字段定义**

ALTER TABLE &lt;表名&gt; MODIFY &lt;字段名称&gt; &lt;字段定义&gt;

```
mysql&gt; alter table account modify wei int ;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

 

```
mysql&gt; alter table account modify wei int  not null ;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

<br>  
