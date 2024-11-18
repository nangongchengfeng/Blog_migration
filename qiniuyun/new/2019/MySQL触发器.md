---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-18 20:02:46
description: 触发器触发器简介创建触发器查看触发器删除触发器触发器案例一、触发器简介触发器是一个特殊的存储过程，它的执行不是由程序调用，也不是手工启动，而是由事件来触发，比如当对一个表进行操作，，时就会激活它执行。。。。。。。。
image: http://image.ownit.top/4kdongman/69.jpg
tags:
- 技术记录
title: MySQL触发器
---

<!--more-->

**MySQL触发器Triggers**  
  
\========================================================  
触发器简介  
创建触发器  
查看触发器  
删除触发器  
触发器案例

###   
一、触发器简介

  
触发器（trigger）是一个特殊的存储过程，它的执行不是由程序调用，也不是手工启动，而是由事件来触发，  
比如当对一个表进行操作（ insert，delete， update）时就会激活它执行。触发器经常用于加强数据的完整  
性约束和业务规则等。  
  
例如，当学生表中增加了一个学生的信息时，学生的总数就应该同时改变。因此可以针对学生表创建一个触发  
器，每次增加一个学生记录时，就执行一次学生总数的计算操作，从而保证学生总数与记录数的一致性。

###   
二、创建Trigger

  
语法：  
CREATE TRIGGER 触发器名称 BEFORE|AFTER 触发事件  
ON 表名 FOR EACH ROW  
BEGIN  
触发器程序体;  
END  
  
**\<触发器名称>** 最多64个字符，它和MySQL中其他对象的命名方式一样  
**\{ BEFORE | AFTER \}** 触发器时机  
**\{ INSERT | UPDATE | DELETE \}**触发的事件  
**ON \<表名称>** 标识建立触发器的表名，即在哪张表上建立触发器  
**FOR EACH ROW** 触发器的执行间隔：FOR EACH ROW子句通知触发器 每隔一行  
执行一次动作，而不是对整个表执行一次  
**\<触发器程序体>** 要触发的SQL语句：可用顺序，判断，循环等语句实现一般程序需要的逻辑功能  
 

## 触发器示例  
1\. 创建表

```
mysql> create table student(
-> id int unsigned auto_increment primary key not null,
-> name varchar(50)
-> );
mysql> insert into student(name) values('wei');

mysql> create table student_total(total int);
mysql> insert into student_total values(1);
```

![](http://image.ownit.top/csdn/20190418171344804.png)

###   
2\. 创建触发器student\_insert\_trigger

### 创建触发器，实现添加学生信息，数量自动增加

```
mysql> \d  $$
mysql> create trigger student_insert_tigger after insert
		on student for each row 
		begin update nummber set count=count+1; 
		end$$
Query OK, 0 rows affected (0.00 sec)

mysql> \d ;
```

### ![](http://image.ownit.top/csdn/20190418195155866.png)

### 创建触发器，删除学生信息，数量自动减少

```
mysql> \d $  # 修改mysql结束符
mysql> create trigger student_delete_trigger after delete
    -> on student for each row
    -> begin
    -> update number set count=count-1;
    -> end$
Query OK, 0 rows affected (0.01 sec)

mysql> \d ;  

```

### 删除一个学生信息

```
mysql> delete from student wheree id="2";
```

查看学生信息

### ![](http://image.ownit.top/csdn/20190418195455665.png)  
三、查看触发器

  
1\. 通过SHOW TRIGGERS语句查看

```
mysql> show triggers\G;
```

  
![](http://image.ownit.top/csdn/20190418195633646.png)

2\. 通过系统表triggers查看

  
USE information\_schema  
SELECT \* FROM triggers\\G  
SELECT \* FROM triggers WHERE TRIGGER\_NAME='触发器名称'\\G

### ![](http://image.ownit.top/csdn/20190418195914784.png)  
四、删除触发器

  
1\. 通过DROP TRIGGERS语句删除  
DROP TRIGGER 解发器名称

```
mysql> drop trigger student_delete_trigger;
Query OK, 0 rows affected (0.00 sec)
```

![](http://image.ownit.top/csdn/20190418200217998.png)