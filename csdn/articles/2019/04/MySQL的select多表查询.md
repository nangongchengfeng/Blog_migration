+++
author = "南宫乘风"
title = "MySQL的select多表查询"
date = "2019-04-17 16:31:24"
tags=['linux', 'mysql']
categories=['MySQL']
image = "post/4kdongman/68.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89358160](https://blog.csdn.net/heian_99/article/details/89358160)

# **select 语句：**

### **select 语句一般用法为: select 字段名 from tb_name where 条件 ;**

## **select 查询语句类型一般分为三种： <br> 单表查询，多表查询，子查询**

**最简单的单表查询 : select * from tb_name; <br> *表示，所有字段**

**查询特定字段(投影)： <br> select 字段名1，字段名2， from tb_name;**

**where 语句过滤查询(选择)**

**select * from tb_name where 条件 ;**

 

**使用SELECT子句进行多表查询**

SELECT 字段名 FROM 表1，表2 … WHERE 表1.字段 = 表2.字段 AND 其它查询条件

<br> SELECT a.id,a.name,a.address,a.date,b.math,b.english,b.chinese FROM tb_demo065_tel AS b,tb_demo065 AS a WHERE a.id=b.id<br> 注:在上面的的代码中，以两张表的id字段信息相同作为条件建立两表关联，但在实际开发中不应该这样使用，最好用主外键约束来实现

# 首先创建一个数据库

![20190417163020735.png](https://img-blog.csdnimg.cn/20190417163020735.png)

### 学生人数表

![20190417160835662.png](https://img-blog.csdnimg.cn/20190417160835662.png)

## **学生成绩表**

![20190417160900426.png](https://img-blog.csdnimg.cn/20190417160900426.png)

## 显示每个学生的对应的成绩

**方法一：**

```
mysql&gt; select students.number,students.name,students.sex,course.math,course.english,course.chinese 
    -&gt; from students inner join course
    -&gt; on students.number=course.number;

```

![20190417161313710.png](https://img-blog.csdnimg.cn/20190417161313710.png)

**方法二：**

```
mysql&gt; select students.number,students.name,students.sex,course.math,course.english,course.chinese
    -&gt; from students,course
    -&gt; where students.number=course.number;

```

![20190417161639262.png](https://img-blog.csdnimg.cn/20190417161639262.png)

 

## 根据学号排名升序输出成绩

```
mysql&gt; select students.number as 学号,students.name as 姓名,course.math as 数学,course.english as 英语,course.chinese as 语文 from students,course where students.number=course.number  order by students.number;


```

 

![2019041716215157.png](https://img-blog.csdnimg.cn/2019041716215157.png)

## 求学生的总成绩，并显示出来，成绩按降序排列

```
mysql&gt; select students.number as 学号,students.name as 姓名,(course.math+course.english +course.chinese) as 总成绩 from students,course where students.number=course.number  order by 总成绩 desc;

```

![20190417162912243.png](https://img-blog.csdnimg.cn/20190417162912243.png)

 

 
