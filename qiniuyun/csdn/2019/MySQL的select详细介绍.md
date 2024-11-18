---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-16 23:50:12
description: 查询数据数据库使用语句来查询数据。你可以通过命令提示窗口中在数据库中查询数据语法以下为在数据库中查询数据通用的语法：查询语句中你可以使用一个或者多个表，表之间使用逗号分割，并使用语句来设定查询条件。命。。。。。。。
image: ../../title_pic/43.jpg
slug: '201904162350'
tags:
- 技术记录
title: MySQL的select详细介绍
---

<!--more-->

# MySQL 查询数据

MySQL 数据库使用SQL SELECT语句来查询数据。

你可以通过 mysql> 命令提示窗口中在数据库中查询数据

### 语法

以下为在MySQL数据库中查询数据通用的 SELECT 语法：

SELECT column\_name,column\_name
FROM table\_name
\[WHERE Clause\]
\[LIMIT N\]\[ OFFSET M\]

- 查询语句中你可以使用一个或者多个表，表之间使用逗号\(,\)分割，并使用WHERE语句来设定查询条件。
- SELECT 命令可以读取一条或者多条记录。
- 你可以使用星号（\*）来代替其他字段，SELECT语句会返回表的所有字段数据
- 你可以使用 WHERE 语句来包含任何条件。
- 你可以使用 LIMIT 属性来设定返回的记录数。
- 你可以通过OFFSET指定SELECT语句开始查询的数据偏移量。默认情况下偏移量为0。

建一张表用于我们测试： 

```
create table student
(
    ids int auto_increment primary key,
    name varchar(20),
    chinese float,
    english float,
    math float 
);
```

  
插入如下数据：   
 

```
insert into student values(1,'李明',89,78,90); 
insert into student values(2,'乘风',67,89,56); 
insert into student values(3,'南宫流云',87,78,77); 
insert into student values(4,'南宫皓月',88,98,90); 
insert into student values(5,'南宫紫月',82,84,67); 
insert into student values(6,'萧炎',55,85,45); 
insert into student values(7,'林动',75,65,30);
```

![](../../image/20190416215956815.png)

### 1、指定查询列

```
mysql> select id,name,chinese from student;
```

![](../../image/20190416220159527.png)

### 2、去重查询

用distinct关键字， 如果结果中有完全相同的行，就去除重复行

```
mysql> select distinct math from student;
```

![](../../image/20190416220343424.png)

### 3、select语句中进行运算

查询学生总成绩 

```
mysql> select id,name,(chinese+math+english) as 总成绩 from student;
```

![](../../image/20190416220512845.png)

## **查询所有姓南宫人的总成绩。** 

```
mysql> select id,name,(chinese+math+english) as 总成绩 from student  
    -> where name like '南宫%';
```

![](../../image/20190416220807102.png)

### 4、where查询过滤

在where子句中有很多经常使用的运算符，如下： 

![è¿éåå¾çæè¿°](../../image/70.jpg)

（1）查询所有英语成绩大于90的同学成绩： 

```
mysql> select id,name,english as 英语 from student
    -> where english > 90;
```

![](../../image/20190416221041984.png)

（2）查询所有总分大于200分的同学 

注意：**where子句后不能用别名**   
因为数据库中先执行where子句，再执行select子句。 

```
mysql> select id,name,(chinese+math+english) as 总成绩 from student
    -> where (chinese+math+english) > 200;
```

![](../../image/20190416231905681.png)

 

（3）查询姓林并且id大于6的学生信息 

```
mysql> select id,name from student
    -> where name like '林%' and id >6;
```

![](../../image/20190416232118591.png)

（4）查询英语成绩大于语文成绩的同学 

```
mysql> select id,name from student
    -> where english > chinese;
```

![](../../image/20190416232251100.png)

（5）查询所有总分大于200并且数学成绩小于语文成绩的学生信息 

```
mysql> select id,name from student
    -> where (chinese+math+english) >200 and math < chinese;
```

![](../../image/20190416232442576.png)

（6）查询所有英语成绩在80到90分的同学   
方法一： 

```
mysql> select id,name,english from student
    -> where english >=80 and english <= 90;
```

![](../../image/20190416232722872.png)

方法二： 

**注意：between是闭区间**

```
mysql> select id,name,english from student
    -> where english between 80 and 90;
```

![](../../image/20190416232943203.png)

（7）查询数学成绩为89,90,91的同学信息   
or: 

```
mysql> select id,name,math from student
    -> where math=89 or math=90 or math=91;
```

![](../../image/20190416233143636.png)

 

in: 

```
mysql> select id,name,math from student
    -> where math in(89,90,91);
```

![](../../image/20190416233535455.png)

### 5、order by排序语句

**asc升序\(默认\)，desc降序 **  
order by 子句应该位于select语句的结尾   
eg：对数学成绩进行排序   
默认升序： 

```
mysql> select id,name,math from student
    -> order by math;
```

![](../../image/20190416233714121.png)

降序： 

```
mysql> select id,name,math from student
    -> order by math desc;
```

![](../../image/20190416233809519.png)

对总分进行从高到低输出   
 

```
mysql> select (chinese+math+english) as 总成绩 from student
    -> order by 总成绩 desc;
```

![](../../image/20190416234113731.png)

### 6、常用函数

（1\)count\(）   
**count\(\*\)统计null值 count\(列名\)排除null值**   
eg :统计当前student表中一共有多少学生 

```
mysql> select count(*) as 人数 from student;
```

![](../../image/20190416234234676.png)

 

\(2\)sum\(\)   
eg：统计一个班数学总成绩 

```
mysql> select sum(math) as 数学总成绩 from student;
```

![](../../image/20190416234431711.png)

（3）平均值：avg（） 

求数学的平均值

```
mysql> select sum(math)/count(*) as 数学平均值 from student;
```

![](../../image/2019041623475797.png)

```
mysql> select avg(math) as 数学平均值 from student;
```

![](../../image/20190416234929331.png)

7、group by 子句的使用  
假设有一个职工信息表，   
EMP:表名 ；部门：depton；sal：工资；job：工作   
我们设想：   
（1）显示每个部门的平均工资和最高工资   
select deptno,avg\(sal\),max\(sal\) from EMP group by deptno;   
（2）显示每个部门的每种岗位的平均工资和最低工资   
select avg\(sal\),min\(sal\),job, deptno from EMP group by deptno, job;   
补充：首先按照deptno分组，然后各组再按照job进行分组。   
（3）显示平均工资低于2000的部门和它的平均工资   
解题思路：   
1\. 统计各个部门的平均工资   
select avg\(sal\) from EMP group by deptno   
2\. having往往和group by配合使用，对group by结果进行过滤   
select avg\(sal\) as myavg from EMP group by deptno having myavg\<2000;