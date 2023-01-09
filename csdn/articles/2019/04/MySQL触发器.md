+++
author = "南宫乘风"
title = "MySQL触发器"
date = "2019-04-18 20:02:46"
tags=[]
categories=['MySQL']
image = "post/4kdongman/50.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89383210](https://blog.csdn.net/heian_99/article/details/89383210)

**MySQL触发器Triggers**<br><br> ========================================================<br> 触发器简介<br> 创建触发器<br> 查看触发器<br> 删除触发器<br> 触发器案例

### <br> 一、触发器简介

<br> 触发器（trigger）是一个特殊的存储过程，它的执行不是由程序调用，也不是手工启动，而是由事件来触发，<br> 比如当对一个表进行操作（ insert，delete， update）时就会激活它执行。触发器经常用于加强数据的完整<br> 性约束和业务规则等。<br><br> 例如，当学生表中增加了一个学生的信息时，学生的总数就应该同时改变。因此可以针对学生表创建一个触发<br> 器，每次增加一个学生记录时，就执行一次学生总数的计算操作，从而保证学生总数与记录数的一致性。

### <br> 二、创建Trigger

<br>语法：<br> CREATE TRIGGER 触发器名称 BEFORE|AFTER 触发事件<br> ON 表名 FOR EACH ROW<br> BEGIN<br> 触发器程序体;<br> END<br><br>**&lt;触发器名称&gt;** 最多64个字符，它和MySQL中其他对象的命名方式一样<br>**{ BEFORE | AFTER }** 触发器时机<br>**{ INSERT | UPDATE | DELETE }**触发的事件<br>**ON &lt;表名称&gt;** 标识建立触发器的表名，即在哪张表上建立触发器<br>**FOR EACH ROW** 触发器的执行间隔：FOR EACH ROW子句通知触发器 每隔一行<br> 执行一次动作，而不是对整个表执行一次<br>**&lt;触发器程序体&gt; ** 要触发的SQL语句：可用顺序，判断，循环等语句实现一般程序需要的逻辑功能<br>  

## 触发器示例<br> 1. 创建表

```
mysql&gt; create table student(
-&gt; id int unsigned auto_increment primary key not null,
-&gt; name varchar(50)
-&gt; );
mysql&gt; insert into student(name) values('wei');

mysql&gt; create table student_total(total int);
mysql&gt; insert into student_total values(1);

```

![20190418171344804.png](https://img-blog.csdnimg.cn/20190418171344804.png)

### <br> 2. 创建触发器student_insert_trigger

### 创建触发器，实现添加学生信息，数量自动增加

```
mysql&gt; \d  $$
mysql&gt; create trigger student_insert_tigger after insert
		on student for each row 
		begin update nummber set count=count+1; 
		end$$
Query OK, 0 rows affected (0.00 sec)

mysql&gt; \d ;
```

### ![20190418195155866.png](https://img-blog.csdnimg.cn/20190418195155866.png)

### 创建触发器，删除学生信息，数量自动减少

```
mysql&gt; \d $  # 修改mysql结束符
mysql&gt; create trigger student_delete_trigger after delete
    -&gt; on student for each row
    -&gt; begin
    -&gt; update number set count=count-1;
    -&gt; end$
Query OK, 0 rows affected (0.01 sec)

mysql&gt; \d ;  


```

### 删除一个学生信息

```
mysql&gt; delete from student wheree id="2";
```

查看学生信息

### ![20190418195455665.png](https://img-blog.csdnimg.cn/20190418195455665.png)<br> 三、查看触发器

<br> 1. 通过SHOW TRIGGERS语句查看

```
mysql&gt; show triggers\G;
```

<br>![20190418195633646.png](https://img-blog.csdnimg.cn/20190418195633646.png)

2. 通过系统表triggers查看

<br> USE information_schema<br> SELECT * FROM triggers\G<br> SELECT * FROM triggers WHERE TRIGGER_NAME='触发器名称'\G

### ![20190418195914784.png](https://img-blog.csdnimg.cn/20190418195914784.png)<br> 四、删除触发器

<br> 1. 通过DROP TRIGGERS语句删除<br> DROP TRIGGER 解发器名称

```
mysql&gt; drop trigger student_delete_trigger;
Query OK, 0 rows affected (0.00 sec)

```

![20190418200217998.png](https://img-blog.csdnimg.cn/20190418200217998.png)

 

 
