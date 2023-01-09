+++
author = "南宫乘风"
title = "MySQL存储过程与函数"
date = "2019-04-18 22:33:16"
tags=[]
categories=['MySQL']
image = "post/4kdongman/24.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89389495](https://blog.csdn.net/heian_99/article/details/89389495)

一、概述：<br> 存储过程和函数是事先经过编译并存储在数据库中的一段SQL语句的集合。<br> 存储过程和函数的区别：<br>• 函数必须有返回值，而存储过程没有。<br> • 存储过程的参数可以是IN、OUT、INOUT类型，函数的参数只能是IN<br>**优点：**<br> • 存储过程只在创建时进行编译；而SQL语句每执行一次就编译一次，所以使用存储过程可以提高数据库执行速度。<br> • 简化复杂操作，结合事务一起封装。<br> • 复用性好<br> • 安全性高，可指定存储过程的使用权。<br>**说明：**<br> 并发量少的情况下，很少使用存储过程。<br> 并发量高的情况下，为了提高效率，用存储过程比较多。<br><br> 二、创建与调用<br> 创建存储过程语法 ：<br> create procedure sp_name(参数列表)<br> [特性...]过程体<br><br> 存储过程的参数形式：[IN | OUT | INOUT]参数名 类型<br> IN 输入参数<br> OUT 输出参数<br> INOUT 输入输出参数<br><br> delimiter $$<br> create procedure 过程名(参数列表)<br> begin<br> SQL语句<br> end $$<br> delimiter ;<br><br> 调用：<br> call 存储过程名(实参列表)<br>  

# 存储过程三种参数类型：IN, OUT, INOUT

<br><br> ===================**NONE**========================

```
mysql&gt; \d $$
mysql&gt; create procedure p1()
-&gt; begin
-&gt; select count(*) from mysql.user;
-&gt; end$$
Query OK, 0 rows affected (0.51 sec)

mysql&gt; \d ;
mysql&gt; call p1()
```

![20190418222049281.png](https://img-blog.csdnimg.cn/20190418222049281.png)<br><br>  

```
mysql&gt; create school.table t1(
-&gt; id int,
-&gt; name varchar(50)
-&gt; );
Query OK, 0 rows affected (2.81 sec)

mysql&gt; delimiter $$
mysql&gt; create procedure autoinsert1()
-&gt; BEGIN
-&gt; declare i int default 1;
-&gt; while(i&lt;=20000)do
-&gt; insert into school.t1 values(i,md5(i));
-&gt; set i=i+1;
-&gt; end while;
-&gt; END$$
mysql&gt; delimiter ;

```

<br> ====================**IN**==========================

```
mysql&gt; create procedure autoinsert2(IN a int)
-&gt; BEGIN
-&gt; declare i int default 1;
-&gt; while(i&lt;=a)do
-&gt; insert into school.t1 values(i,md5(i));
-&gt; set i=i+1;
-&gt; end while;
-&gt; END$$
Query OK, 0 rows affected (0.00 sec)

mysql&gt; call autoinsert1(10);
Query OK, 1 row affected (1.10 sec)

mysql&gt; set @num=20;
mysql&gt; select @num;
+------+
| @num |
+------+
| 20 |
+------+
1 row in set (0.00 sec)

mysql&gt; call autoinsert1(@num);
```

<br><br><br> ====================**OUT**=======================

```
mysql&gt; delimiter $$
mysql&gt; CREATE PROCEDURE p2 (OUT param1 INT)
-&gt; BEGIN
-&gt; SELECT COUNT(*) INTO param1 FROM t1;
-&gt; END$$
Query OK, 0 rows affected (0.00 sec)

mysql&gt; delimiter ;

mysql&gt; select @a;
+------+
| @a |
+------+
| NULL |
+------+
1 row in set (0.00 sec)

mysql&gt; CALL p2(@a);
Query OK, 0 rows affected (0.00 sec)

mysql&gt; SELECT @a;
+------+
| @a |
+------+
| 3 |
+------+

```

<br> ===================**IN 和 OUT**=====================

### 作用：统计指定部门的员工数

 

```
mysql&gt; create procedure count_num(IN p1 varchar(50), OUT p2 int)
-&gt; BEGIN
-&gt; select count(*) into p2 from employee
-&gt; where post=p1;
-&gt; END$$
Query OK, 0 rows affected (0.00 sec)
mysql&gt; \d ;


mysql&gt; call count_num('hr',@a);

mysql&gt;select @a;
```

<br><br>  

### 作用：统计指定部门工资超过例如5000的总人数

 

```
mysql&gt; create procedure count_num(IN p1 varchar(50), IN p2 float(10,2), OUT p3 int)
-&gt; BEGIN
-&gt; select count(*) into p3 from employee
-&gt; where post=p1 and salary=&gt;p2;
-&gt; END$$
Query OK, 0 rows affected (0.00 sec)
mysql&gt; \d ;

mysql&gt; call count_num('hr',5000,@a);


```

<br> ====================**INOUT**======================

```
mysql&gt; create procedure proce_param_inout(inout p1 int)
-&gt; begin
-&gt; if (p1 is not null) then
-&gt; set p1=p1+1;
-&gt; else
-&gt; select 100 into p1;
-&gt; end if;
-&gt; end$$
Query OK, 0 rows affected (0.00 sec)


mysql&gt; select @h;
+------+
| @h |
+------+
| NULL |
+------+
1 row in set (0.00 sec)

mysql&gt; call proce_param_inout(@h);
Query OK, 1 row affected (0.00 sec)

mysql&gt; select @h;
+------+
| @h |
+------+
| 100 |
+------+begin
1 row in set (0.00 sec)

mysql&gt; call proce_param_inout(@h);
Query OK, 0 rows affected (0.00 sec)

mysql&gt; select @h;
+------+
| @h |
+------+
| 101 |
+------+
1 row in set (0.00 sec)


```

<br>  

# FUNCTION函数

<br> =================================================

```
mysql&gt; CREATE FUNCTION hello (s CHAR(20))
-&gt; RETURNS CHAR(50) RETURN CONCAT('Hello, ',s,'!');
Query OK, 0 rows affected (0.00 sec)

mysql&gt; select hello('localhost');
+------------------+
| hello('localhost') |
+------------------+
| Hello, localhost! |
+------------------+

root@(company)&gt; select hello('localhost') return1;
+-----------------+
| return1 |
+-----------------+
| Hello, localhost! |
+-----------------+
1 row in set (0.00 sec)


mysql&gt; create function name_from_employee(x int)
-&gt; returns varchar(50)
-&gt; BEGIN
-&gt; return (select emp_name from employee
-&gt; where emp_id=x);
-&gt; END$$
Query OK, 0 rows affected (0.00 sec)

mysql&gt; select name_from_employee(3);

mysql&gt; select * from employee where emp_name=name_from_employee(1);
+--------+----------+------+------------+------------+-----------------+---------+--------+--------+
| emp_id | emp_name | sex | hire_date | post | job_description | salary | office | dep_id |
+--------+----------+------+------------+------------+-----------------+---------+--------+--------+
| 1 | jack | male | 2013-02-02 | instructor | teach | 5000.00 | 501 | 100 |
+--------+----------+------+------------+------------+-----------------+---------+--------+--------+
1 row in set (0.00 sec)


```

<br><br><br> ==============================================<br> 创建函数的语法：<br> create function 函数名(参数列表) returns 返回值类型<br> [特性...] 函数体<br> 函数的参数形式：参数名 类型<br><br> delimiter $$<br> create function 函数名(参数列表) returns 返回值类型<br> begin<br> 有效的SQL语句<br> end$$<br> delimiter ;<br> 调用：<br> select 函数名(实参列表)<br><br> delimiter $$<br> create function fun1(str char(20)) returns char(50)<br> return concat("hello",str,"!");<br> $$<br> delimiter ;<br><br> select fun1(' function');<br><br> 存储过程与函数的维护：<br> show create procedure pr1 \G;<br> show create function pr1 \G;<br><br> show {procedure|function} status {like 'pattern'}<br><br> drop {procedure|function} {if exists} sp_name<br><br><br> mysql变量的术语分类：<br> 1.用户变量：以"@"开始，形式为"@变量名"，由客户端定义的变量。<br> 用户变量跟mysql客户端是绑定的，设置的变量只对当前用户使用的客户端生效，当用户断开连接时，所有变量会自动释放。<br> 2.全局变量：定义时如下两种形式，set GLOBAL 变量名  或者  set @@global.变量名<br> 对所有客户端生效，但只有具有super权限才可以设置全局变量。<br> 3.会话变量：只对连接的客户端有效。<br> 4.局部变量：设置并作用于begin...end语句块之间的变量。<br> declare语句专门用于定义局部变量。而set语句是设置不同类型的变量，包括会话变量和全局变量<br> 语法：declare 变量名[...] 变量类型 [default 值]<br> declare定义的变量必须写在复合语句的开头，并且在任何其它语句的前面。<br><br> 变量的赋值：<br> 直接赋值： set 变量名=表达式值或常量值[...];<br><br> 用户变量的赋值：<br> 1、set 变量名=表达式或常量值;<br> 2、也可以将查询结果赋值给变量(要求查询返回的结果只能有一行)<br> 例：set 列名 into 变量名 from 表名 where 条件;<br> 3、select 值 into @变量名；<br> 客户端变量不能相互共享。<br>  

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

<br>  

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

<br>  

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

<br>  

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

 
