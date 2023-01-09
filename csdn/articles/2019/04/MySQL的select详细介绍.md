+++
author = "南宫乘风"
title = "MySQL的select详细介绍"
date = "2019-04-16 23:50:12"
tags=[]
categories=['MySQL']
image = "post/4kdongman/32.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89342729](https://blog.csdn.net/heian_99/article/details/89342729)

# MySQL 查询数据

MySQL 数据库使用SQL SELECT语句来查询数据。

你可以通过 mysql&gt; 命令提示窗口中在数据库中查询数据

### 语法

以下为在MySQL数据库中查询数据通用的 SELECT 语法：

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

<br> 插入如下数据： <br>  

```
insert into student values(1,'李明',89,78,90); 
insert into student values(2,'乘风',67,89,56); 
insert into student values(3,'南宫流云',87,78,77); 
insert into student values(4,'南宫皓月',88,98,90); 
insert into student values(5,'南宫紫月',82,84,67); 
insert into student values(6,'萧炎',55,85,45); 
insert into student values(7,'林动',75,65,30);

```

![20190416215956815.png](https://img-blog.csdnimg.cn/20190416215956815.png)

### 1、指定查询列

```
mysql&gt; select id,name,chinese from student;

```

![20190416220159527.png](https://img-blog.csdnimg.cn/20190416220159527.png)

### 2、去重查询

用distinct关键字， 如果结果中有完全相同的行，就去除重复行

```
mysql&gt; select distinct math from student;

```

![20190416220343424.png](https://img-blog.csdnimg.cn/20190416220343424.png)

### 3、select语句中进行运算

查询学生总成绩 

```
mysql&gt; select id,name,(chinese+math+english) as 总成绩 from student;
```

![20190416220512845.png](https://img-blog.csdnimg.cn/20190416220512845.png)

## **查询所有姓南宫人的总成绩。** 

```
mysql&gt; select id,name,(chinese+math+english) as 总成绩 from student  
    -&gt; where name like '南宫%';

```

![20190416220807102.png](https://img-blog.csdnimg.cn/20190416220807102.png)

### 4、where查询过滤

在where子句中有很多经常使用的运算符，如下： 

<img alt="è¿éåå¾çæè¿°" class="has" src="https://img-blog.csdn.net/20180526155434349?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhaWR1XzM3OTY0MDcx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70">

（1）查询所有英语成绩大于90的同学成绩： 

```
mysql&gt; select id,name,english as 英语 from student
    -&gt; where english &gt; 90;
```

![20190416221041984.png](https://img-blog.csdnimg.cn/20190416221041984.png)

（2）查询所有总分大于200分的同学 

注意：**where子句后不能用别名** <br> 因为数据库中先执行where子句，再执行select子句。 

```
mysql&gt; select id,name,(chinese+math+english) as 总成绩 from student
    -&gt; where (chinese+math+english) &gt; 200;
```

![20190416231905681.png](https://img-blog.csdnimg.cn/20190416231905681.png)

 

（3）查询姓林并且id大于6的学生信息 

```
mysql&gt; select id,name from student
    -&gt; where name like '林%' and id &gt;6;
```

![20190416232118591.png](https://img-blog.csdnimg.cn/20190416232118591.png)

（4）查询英语成绩大于语文成绩的同学 

```
mysql&gt; select id,name from student
    -&gt; where english &gt; chinese;
```

![20190416232251100.png](https://img-blog.csdnimg.cn/20190416232251100.png)

（5）查询所有总分大于200并且数学成绩小于语文成绩的学生信息 

```
mysql&gt; select id,name from student
    -&gt; where (chinese+math+english) &gt;200 and math &lt; chinese;
```

![20190416232442576.png](https://img-blog.csdnimg.cn/20190416232442576.png)

（6）查询所有英语成绩在80到90分的同学 <br> 方法一： 

```
mysql&gt; select id,name,english from student
    -&gt; where english &gt;=80 and english &lt;= 90;
```

![20190416232722872.png](https://img-blog.csdnimg.cn/20190416232722872.png)

方法二： 

**注意：between是闭区间**

```
mysql&gt; select id,name,english from student
    -&gt; where english between 80 and 90;
```

![20190416232943203.png](https://img-blog.csdnimg.cn/20190416232943203.png)

（7）查询数学成绩为89,90,91的同学信息 <br> or: 

```
mysql&gt; select id,name,math from student
    -&gt; where math=89 or math=90 or math=91;
```

![20190416233143636.png](https://img-blog.csdnimg.cn/20190416233143636.png)

 

in: 

```
mysql&gt; select id,name,math from student
    -&gt; where math in(89,90,91);
```

![20190416233535455.png](https://img-blog.csdnimg.cn/20190416233535455.png)

### 5、order by排序语句

**asc升序(默认)，desc降序 **<br> order by 子句应该位于select语句的结尾 <br> eg：对数学成绩进行排序 <br> 默认升序： 

```
mysql&gt; select id,name,math from student
    -&gt; order by math;
```

![20190416233714121.png](https://img-blog.csdnimg.cn/20190416233714121.png)

降序： 

```
mysql&gt; select id,name,math from student
    -&gt; order by math desc;
```

![20190416233809519.png](https://img-blog.csdnimg.cn/20190416233809519.png)

对总分进行从高到低输出 <br>  

```
mysql&gt; select (chinese+math+english) as 总成绩 from student
    -&gt; order by 总成绩 desc;
```

![20190416234113731.png](https://img-blog.csdnimg.cn/20190416234113731.png)

### 6、常用函数

（1)count(） <br>**count(*)统计null值 count(列名)排除null值** <br> eg :统计当前student表中一共有多少学生 

```
mysql&gt; select count(*) as 人数 from student;
```

![20190416234234676.png](https://img-blog.csdnimg.cn/20190416234234676.png)

 

(2)sum() <br> eg：统计一个班数学总成绩 

```
mysql&gt; select sum(math) as 数学总成绩 from student;
```

![20190416234431711.png](https://img-blog.csdnimg.cn/20190416234431711.png)

（3）平均值：avg（） 

求数学的平均值

```
mysql&gt; select sum(math)/count(*) as 数学平均值 from student;
```

![2019041623475797.png](https://img-blog.csdnimg.cn/2019041623475797.png)

```
mysql&gt; select avg(math) as 数学平均值 from student;
```

![20190416234929331.png](https://img-blog.csdnimg.cn/20190416234929331.png)

7、group by 子句的使用<br> 假设有一个职工信息表， <br> EMP:表名 ；部门：depton；sal：工资；job：工作 <br> 我们设想： <br> （1）显示每个部门的平均工资和最高工资 <br> select deptno,avg(sal),max(sal) from EMP group by deptno; <br> （2）显示每个部门的每种岗位的平均工资和最低工资 <br> select avg(sal),min(sal),job, deptno from EMP group by deptno, job; <br> 补充：首先按照deptno分组，然后各组再按照job进行分组。 <br> （3）显示平均工资低于2000的部门和它的平均工资 <br> 解题思路： <br> 1. 统计各个部门的平均工资 <br> select avg(sal) from EMP group by deptno <br> 2. having往往和group by配合使用，对group by结果进行过滤 <br> select avg(sal) as myavg from EMP group by deptno having myavg&lt;2000;

 
