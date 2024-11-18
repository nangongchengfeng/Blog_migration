---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-18 22:33:16
description: 一、概述：存储过程和函数是事先经过编译并存储在数据库中的一段语句的集合。存储过程和函数的区别：函数必须有返回值，而存储过程没有。存储过程的参数可以是、、类型，函数的参数只能是优点：存储过程只在创建时进。。。。。。。
image: ../../title_pic/53.jpg
slug: '201904182233'
tags:
- 技术记录
title: MySQL存储过程与函数
---

<!--more-->

一、概述：  
存储过程和函数是事先经过编译并存储在数据库中的一段SQL语句的集合。  
存储过程和函数的区别：  
• 函数必须有返回值，而存储过程没有。  
• 存储过程的参数可以是IN、OUT、INOUT类型，函数的参数只能是IN  
**优点：**  
• 存储过程只在创建时进行编译；而SQL语句每执行一次就编译一次，所以使用存储过程可以提高数据库执行速度。  
• 简化复杂操作，结合事务一起封装。  
• 复用性好  
• 安全性高，可指定存储过程的使用权。  
**说明：**  
并发量少的情况下，很少使用存储过程。  
并发量高的情况下，为了提高效率，用存储过程比较多。  
  
二、创建与调用  
创建存储过程语法 ：  
create procedure sp\_name\(参数列表\)  
\[特性...\]过程体  
  
存储过程的参数形式：\[IN | OUT | INOUT\]参数名 类型  
IN 输入参数  
OUT 输出参数  
INOUT 输入输出参数  
  
delimiter \$\$  
create procedure 过程名\(参数列表\)  
begin  
SQL语句  
end \$\$  
delimiter ;  
  
调用：  
call 存储过程名\(实参列表\)  
 

# 存储过程三种参数类型：IN, OUT, INOUT

  
  
\===================**NONE**\========================

```
mysql> \d $$
mysql> create procedure p1()
-> begin
-> select count(*) from mysql.user;
-> end$$
Query OK, 0 rows affected (0.51 sec)

mysql> \d ;
mysql> call p1()
```

![](../../image/20190418222049281.png)  
  
 

```
mysql> create school.table t1(
-> id int,
-> name varchar(50)
-> );
Query OK, 0 rows affected (2.81 sec)

mysql> delimiter $$
mysql> create procedure autoinsert1()
-> BEGIN
-> declare i int default 1;
-> while(i<=20000)do
-> insert into school.t1 values(i,md5(i));
-> set i=i+1;
-> end while;
-> END$$
mysql> delimiter ;
```

  
\====================**IN**\==========================

```
mysql> create procedure autoinsert2(IN a int)
-> BEGIN
-> declare i int default 1;
-> while(i<=a)do
-> insert into school.t1 values(i,md5(i));
-> set i=i+1;
-> end while;
-> END$$
Query OK, 0 rows affected (0.00 sec)

mysql> call autoinsert1(10);
Query OK, 1 row affected (1.10 sec)

mysql> set @num=20;
mysql> select @num;
+------+
| @num |
+------+
| 20 |
+------+
1 row in set (0.00 sec)

mysql> call autoinsert1(@num);
```

  
  
  
\====================**OUT**\=======================

```
mysql> delimiter $$
mysql> CREATE PROCEDURE p2 (OUT param1 INT)
-> BEGIN
-> SELECT COUNT(*) INTO param1 FROM t1;
-> END$$
Query OK, 0 rows affected (0.00 sec)

mysql> delimiter ;

mysql> select @a;
+------+
| @a |
+------+
| NULL |
+------+
1 row in set (0.00 sec)

mysql> CALL p2(@a);
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @a;
+------+
| @a |
+------+
| 3 |
+------+
```

  
\===================**IN 和 OUT**\=====================

### 作用：统计指定部门的员工数

 

```
mysql> create procedure count_num(IN p1 varchar(50), OUT p2 int)
-> BEGIN
-> select count(*) into p2 from employee
-> where post=p1;
-> END$$
Query OK, 0 rows affected (0.00 sec)
mysql> \d ;


mysql> call count_num('hr',@a);

mysql>select @a;
```

  
  
 

### 作用：统计指定部门工资超过例如5000的总人数

 

```
mysql> create procedure count_num(IN p1 varchar(50), IN p2 float(10,2), OUT p3 int)
-> BEGIN
-> select count(*) into p3 from employee
-> where post=p1 and salary=>p2;
-> END$$
Query OK, 0 rows affected (0.00 sec)
mysql> \d ;

mysql> call count_num('hr',5000,@a);

```

  
\====================**INOUT**\======================

```
mysql> create procedure proce_param_inout(inout p1 int)
-> begin
-> if (p1 is not null) then
-> set p1=p1+1;
-> else
-> select 100 into p1;
-> end if;
-> end$$
Query OK, 0 rows affected (0.00 sec)


mysql> select @h;
+------+
| @h |
+------+
| NULL |
+------+
1 row in set (0.00 sec)

mysql> call proce_param_inout(@h);
Query OK, 1 row affected (0.00 sec)

mysql> select @h;
+------+
| @h |
+------+
| 100 |
+------+begin
1 row in set (0.00 sec)

mysql> call proce_param_inout(@h);
Query OK, 0 rows affected (0.00 sec)

mysql> select @h;
+------+
| @h |
+------+
| 101 |
+------+
1 row in set (0.00 sec)

```

  
 

# FUNCTION函数

  
\=================================================

```
mysql> CREATE FUNCTION hello (s CHAR(20))
-> RETURNS CHAR(50) RETURN CONCAT('Hello, ',s,'!');
Query OK, 0 rows affected (0.00 sec)

mysql> select hello('localhost');
+------------------+
| hello('localhost') |
+------------------+
| Hello, localhost! |
+------------------+

root@(company)> select hello('localhost') return1;
+-----------------+
| return1 |
+-----------------+
| Hello, localhost! |
+-----------------+
1 row in set (0.00 sec)


mysql> create function name_from_employee(x int)
-> returns varchar(50)
-> BEGIN
-> return (select emp_name from employee
-> where emp_id=x);
-> END$$
Query OK, 0 rows affected (0.00 sec)

mysql> select name_from_employee(3);

mysql> select * from employee where emp_name=name_from_employee(1);
+--------+----------+------+------------+------------+-----------------+---------+--------+--------+
| emp_id | emp_name | sex | hire_date | post | job_description | salary | office | dep_id |
+--------+----------+------+------------+------------+-----------------+---------+--------+--------+
| 1 | jack | male | 2013-02-02 | instructor | teach | 5000.00 | 501 | 100 |
+--------+----------+------+------------+------------+-----------------+---------+--------+--------+
1 row in set (0.00 sec)

```

  
  
  
\==============================================  
创建函数的语法：  
create function 函数名\(参数列表\) returns 返回值类型  
\[特性...\] 函数体  
函数的参数形式：参数名 类型  
  
delimiter \$\$  
create function 函数名\(参数列表\) returns 返回值类型  
begin  
有效的SQL语句  
end\$\$  
delimiter ;  
调用：  
select 函数名\(实参列表\)  
  
delimiter \$\$  
create function fun1\(str char\(20\)\) returns char\(50\)  
return concat\("hello",str,"\!"\);  
\$\$  
delimiter ;  
  
select fun1\(' function'\);  
  
存储过程与函数的维护：  
show create procedure pr1 \\G;  
show create function pr1 \\G;  
  
show \{procedure|function\} status \{like 'pattern'\}  
  
drop \{procedure|function\} \{if exists\} sp\_name  
  
  
mysql变量的术语分类：  
1.用户变量：以"\@"开始，形式为"\@变量名"，由客户端定义的变量。  
用户变量跟mysql客户端是绑定的，设置的变量只对当前用户使用的客户端生效，当用户断开连接时，所有变量会自动释放。  
2.全局变量：定义时如下两种形式，set GLOBAL 变量名  或者  set \@\@global.变量名  
对所有客户端生效，但只有具有super权限才可以设置全局变量。  
3.会话变量：只对连接的客户端有效。  
4.局部变量：设置并作用于begin...end语句块之间的变量。  
declare语句专门用于定义局部变量。而set语句是设置不同类型的变量，包括会话变量和全局变量  
语法：declare 变量名\[...\] 变量类型 \[default 值\]  
declare定义的变量必须写在复合语句的开头，并且在任何其它语句的前面。  
  
变量的赋值：  
直接赋值： set 变量名=表达式值或常量值\[...\];  
  
用户变量的赋值：  
1、set 变量名=表达式或常量值;  
2、也可以将查询结果赋值给变量\(要求查询返回的结果只能有一行\)  
例：set 列名 into 变量名 from 表名 where 条件;  
3、select 值 into \@变量名；  
客户端变量不能相互共享。  
 

```
delimiter $$
create procedure pr2()
begin
declare xname varchar(50);
declare xdesc varchar(100);
set xname="caiwu";
set xdesc="accouting";
insert into dept(name,desc) values(xname,xdesc);
end$$
delimiter ;
call pr2();
```

  
 

```
delimiter $$
create procedure pr3(in x int,in y int,out sum int)
begin
set sum=x+y;
end$$
delimiter ;
call pr3(3,4,@sum);
select @sum;
```

  
 

```
delimiter //
create function fun6(x int,y int) returns int
begin
declare sum int;
set sum=x+y;
return sum;
end//
delimiter ;
select fun6(4,3);
```

  
 

```
delimiter //
create function fun_add_rand(in_int int )
RETURNS int
BEGIN
declare i_rand int;
declare i_return int;
set i_rand=floor(rand()*100);
set i_return = in_int + i_rand;
return i_return;
END;
//
```