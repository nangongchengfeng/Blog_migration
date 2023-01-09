+++
author = "南宫乘风"
title = "MySQL基础理论"
date = "2019-04-15 23:27:50"
tags=[]
categories=['MySQL']
image = "post/4kdongman/04.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89323383](https://blog.csdn.net/heian_99/article/details/89323383)

# **MySQL数据库**

**以文本的形式存储数据的劣势:**
- **      1、数据冗余(一个文件中出现n次相同的数据)和数据不一致性**- **      2、数据访问困难**- **      3、数据孤立**- **      4、数据完整性问题**- **      5、原子性(多个相关联的操作必须要同时完成**- **      6、并发访问异常**- **      7、安全性问题**
**DBMS----DataBase Management System数据库管理系统**

**      以关系(表)的形式存储数据**

**      记录Record              表中的每一-行数据;<br>       字段(属性) column      表中的每一列名字**

**      数据库<br>         表<br>       <br> 软件:**

**      MySQL, oracle, MariaDB (https:/ /www.percona.com/)，DB2， SQL Server<br>       MongeDB**

**约束  Constraint**

**      域约束:数据类型约束<br>             保证某字段的数据类型一致**

**      外键约束:引用完整性约束(InnoDB)<br>             一个表中某字段的数据必须在与之相关的其他表的相关联字段中存在**

**      主键约束<br>             某字段能惟一标识此字段所属的实体，并且不允许为空，<br>             一个表只能有一个主键**

**      惟一键约束<br>             某字段能惟一标识此字段所属的实体，可以为空 <br>             一个表可以有多个惟一键**

**      检查性约束<br>             保证某字段中不能出现违反常理的数据，例如年龄**

# **MySQL基础应用**

**一、数据库特点:结构化,无有害,无重复;**

**二、数据库优点:按一定的数据模型组织,描述和储存;可为各种用户共享,冗余度小,节省储存空间易扩展,编写有关数据应用程序。**

**三、常用Dos操作指令:**
1. **安装数据库:mysqld -install,**1. **开启/关闭数据库:start mysql/net stop,**1. **监听端口信息:netstat -a,**1. **登陆数据库:mysql -uroot -p,**1. **显示默认数据库:use dbname,**1. **显示所有数据库:show databases,**1. **显示默认数据库中的所有表:show tables,**1. **放弃正在输入的指令:\c,**1. **显示命令清单:\h,**1. **退出mysql程序:\q,**1. **查看mysql服务器状态信息:\s,**1. **mysql版本信息:SELECT version(),**1. **打开表结构:desc table。**
**四、数据库语法组成:**

**1.DDM(Data Definition Language数据库定义语言):create table,drop table,alter table等**

**2.DCL(Data Control Language数据控制语言):grant,revoke等;**

**3.DML(Data Manipulation Language数据操作语言)查询SELECT、插入insert、update修改、删除delete;**

**五、MYSQL三种常用的数据类型:文本:char,varchar,text;数字,日期和时间类型;**

**![993601-20160731132726059-281428318.png](https://images2015.cnblogs.com/blog/993601/201607/993601-20160731132726059-281428318.png)**

**六、常用操作**
- **显示表结构:DESC 表名;**- **删除表操作:drop table 表名**- **除数据库操作:drop database 数据库名**- **更改表结构操作:alter table 表名 action;(action可以是以下操作)**- **add 列名 建表语句[first/after]--在表中添加列,制定其位置;**- **add primary key (列名)-- 添加一个主键,如果主键已存在,会报错;**- **add foreign key (列名) reference 表名 （列名）;-- 为表添加一个外键;**- **alter列名 set default 默认值;-- 更改指定列的默认值**- **drop 列名 -- 删除一列**- **drop primary key -- 删除主键**- **engine 类型名 -- 改变表的类型**- **rename as 新表名 -- 改变表名**- **change 旧列名 新列名 [first /after]-- 更改列的类型和名称**- **modify 和change相同;**
 
