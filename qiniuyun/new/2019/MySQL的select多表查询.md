---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-17 16:31:24
description: 语句：语句一般用法为字段名条件查询语句类型一般分为三种：单表查询，多表查询，子查询最简单的单表查询表示，所有字段查询特定字段投影：字段名，字段名，语句过滤查询选择条件使用子句进行多表查询字段名表，表表。。。。。。。
image: http://image.ownit.top/4kdongman/37.jpg
tags:
- linux
- mysql
title: MySQL的select多表查询
---

<!--more-->

# **select 语句：**

### **select 语句一般用法为: select 字段名 from tb\_name where 条件 ;**

## **select 查询语句类型一般分为三种：   
单表查询，多表查询，子查询**

**最简单的单表查询 : select \* from tb\_name;   
\*表示，所有字段**

**查询特定字段\(投影\)：   
select 字段名1，字段名2， from tb\_name;**

**where 语句过滤查询\(选择\)**

**select \* from tb\_name where 条件 ;**

 

**使用SELECT子句进行多表查询**

SELECT 字段名 FROM 表1，表2 … WHERE 表1.字段 = 表2.字段 AND 其它查询条件

  
SELECT a.id,a.name,a.address,a.date,b.math,b.english,b.chinese FROM tb\_demo065\_tel AS b,tb\_demo065 AS a WHERE a.id=b.id  
注:在上面的的代码中，以两张表的id字段信息相同作为条件建立两表关联，但在实际开发中不应该这样使用，最好用主外键约束来实现

# 首先创建一个数据库

![](http://image.ownit.top/csdn/20190417163020735.png)

### 学生人数表

![](http://image.ownit.top/csdn/20190417160835662.png)

## **学生成绩表**

![](http://image.ownit.top/csdn/20190417160900426.png)

## 显示每个学生的对应的成绩

**方法一：**

```
mysql> select students.number,students.name,students.sex,course.math,course.english,course.chinese 
    -> from students inner join course
    -> on students.number=course.number;
```

![](http://image.ownit.top/csdn/20190417161313710.png)

**方法二：**

```
mysql> select students.number,students.name,students.sex,course.math,course.english,course.chinese
    -> from students,course
    -> where students.number=course.number;
```

![](http://image.ownit.top/csdn/20190417161639262.png)

 

## 根据学号排名升序输出成绩

```
mysql> select students.number as 学号,students.name as 姓名,course.math as 数学,course.english as 英语,course.chinese as 语文 from students,course where students.number=course.number  order by students.number;

```

 

![](http://image.ownit.top/csdn/2019041716215157.png)

## 求学生的总成绩，并显示出来，成绩按降序排列

```
mysql> select students.number as 学号,students.name as 姓名,(course.math+course.english +course.chinese) as 总成绩 from students,course where students.number=course.number  order by 总成绩 desc;
```

![](http://image.ownit.top/csdn/20190417162912243.png)