---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-17 23:46:10
description: 视图视图就是一个表或多个表的查询结果，它是一张虚拟的表，因为它并不能存储数据。视图的作用、优点：限制对数据的访问让复杂查询变得简单提供数据的独立性可以完成对相同数据的不同显示创建、修改视图通常不对视图。。。。。。。
image: http://image.ownit.top/4kdongman/50.jpg
tags:
- 技术记录
title: MySQL视图及索引
---

<!--more-->

**视图**

视图就是一个表或多个表的查询结果，它是一张虚拟的表，因为它并不能存储数据。

视图的作用、优点：

　　限制对数据的访问

　　让复杂查询变得简单

　　提供数据的独立性

　　可以完成对相同数据的不同显示

```
//创建、修改视图
create or replace view view_temp
as
select name, age from temp;

//通常不对视图的数据做修改操作，因为视图是一张虚拟的表，它并不存储实际数据。如果想让视图不被修改，可以用with check option来完成限制。
create or replace view view_temp
as 
select *from temp
with check option;

//删除视图
drop view view_temp;

//显示创建语法
show create view v_temp;
```

显示学生成绩单的视图

```
mysql> create view student_cj as select students.number,students.name,course.math,course.english,course.chinese
    -> from students,course
    -> where students.number=course.number;
Query OK, 0 rows affected (0.00 sec)
```

使用student\_cj个视图，显示结果

![](http://image.ownit.top/csdn/20190417212343364.png)

删除这个视图

```
mysql> drop view student_cj;
Query OK, 0 rows affected (0.00 sec)
```

![](http://image.ownit.top/csdn/20190417212641238.png)

查看视图的信息

```
mysql> show create view student_cj\G
```

![](http://image.ownit.top/csdn/20190417212918556.png)

**索引**

**1.在不读取整个表的情况下，索引使数据库应用程序可以更快地查找数据。\[ 是为了快速查询而针对某些字段建立起来的。\]  
2.更新一个包含索引的表需要比更新一个没有索引的表更多的时间，这是由于索引本身也需要更新。  
3.表**

**01.数据库中的数据都是存储在表中的  
02.表是物理存储的，真实存在的**

2.案例

创建索引：`create index degree_fast on score (degree);`   
这里的`dgeree_fast`是索引名，`score`是表明，`degree`是表中的一个字段。   
创建视图：

```
create view [viewName] as 
select [someFields]
from [tableName]
```

删除索引：   
\- 01.方式一：`drop index degree_fast on score;`   
\- 02.方式二：`alter table score drop index degree_fast;`

`Mysql cannot drop index needed in a foreign key constraint.`Mysql不能在外键约束下删除索引。如果有外键的话，需要先把外键删除，然后再删除索引。