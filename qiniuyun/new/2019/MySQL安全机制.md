---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-18 23:55:30
description: 安全机制权限表用户管理权限管理一、权限表用户字段权限字段安全字段资源控制字段、用户字段权限字段二、用户管理登录和退出示例：指定主机名服务器端口指定用户名指定登录密码此处为指定登录的数据库接语句查看用户。。。。。。。
image: http://image.ownit.top/4kdongman/81.jpg
tags:
- 技术记录
title: MySQL安全机制
---

<!--more-->

**MySQL安全机制**  
  
\========================================================  
MySQL权限表  
MySQL用户管理  
MySQL权限管理  
  
  
一、MySQL权限表  
mysql.user Global level  
用户字段  
权限字段  
安全字段  
资源控制字段  
mysql.db、mysql.host Database level  
用户字段  
权限字段  
mysql.tables\_priv Table level  
mysql.columns\_priv Column level  
mysql.procs\_priv  
  
  
二、MySQL用户管理  
1\. 登录和退出MySQL  
示例：  
mysql \-h192.168.5.240 \-P 3306 \-u root \-p123 mysql \-e ‘select user,host from user’  
\-h 指定主机名  
\-P MySQL服务器端口  
\-u 指定用户名  
\-p 指定登录密码  
此处mysql为指定登录的数据库  
\-e 接SQL语句

查看用户表

用户管理

```
mysql>use mysql;
```

查看

```
mysql> select host,user,password from user ;
```

![](http://image.ownit.top/csdn/20190418231408187.png)  
2\. 创建用户  
方法一：CREATE USER语句创建

```
CREATE USER zhang@localhost IDENTIFIED BY "zhang";
```

刷新表

```
 flush privileges;
```

![](http://image.ownit.top/csdn/20190418232909974.png)  
方法二： INSERT语句创建

```
Imysql> INSERT INTO mysql.user(user,host, password,ssl_cipher,x509_issuer,x509_subject)
    ->  VALUES("user2","localhost",password("123456"),"","","");
Query OK, 1 row affected (0.00 sec)
```

```
 flush privileges;
```

![](http://image.ownit.top/csdn/20190418233619983.png)

方法三： GRANT语句创建

```
mysql> GRANT SELECT ON *.* TO user3@"localhost" IDENTIFIED BY "123456";
Query OK, 0 rows affected (0.00 sec)
```

```
mysql> FLUSH PRIVILEGES;
```

![](http://image.ownit.top/csdn/20190418233745506.png)  
  
3\. 删除用户  
方法一：DROP USER语句删除

```
mysql> DROP USER user1@"localhost";
Query OK, 0 rows affected (0.00 sec)
```

  
![](http://image.ownit.top/csdn/20190418233935933.png)  
方法二：DELETE语句删除

```
mysql> delete from user
    -> where user="user2" and host="localhost";
Query OK, 1 row affected (0.00 sec)
```

 

```
mysql> flush privileges;
```

![](http://image.ownit.top/csdn/20190418234240966.png)  
  
  
4\. 修改用户密码  
＝＝＝root修改自己密码  
方法一：

```
# mysqladmin -uroot -p123 password 'new_password' //123为旧密码
```

  
  
方法二：

```
UPDATE mysql.user SET password=password(‘new_password’)
WHERE user=’root’ AND host=’localhost’;
FLUSH PRIVILEGES;
```

  
  
方法三：

```
SET PASSWORD=password(‘new_password’);
FLUSH PRIVILEGES;
```

  
  
  
\==root修改其他用户密码  
方法一：

```
SET PASSWORD FOR user3@’localhost’=password(‘new_password’);
FLUSH PRIVILEGES;
```

  
  
方法二：

```
UPDATE mysql.user SET password=password(‘new_password’)
WHERE user=’user3’ AND host=’localhost’;
FLUSH PRIVILEGES;
```

  
方法三：

```
GRANT SELECT ON *.* TO user3@’localhost’ IDENTIFIED BY ‘localhost’;
FLUSH PRIVILEGES;
```

  
  
＝＝＝普通用户修改自己密码  
方法一：

```
SET password=password(‘new_password’);
```

  
  
方法二：

```
# mysqladmin -uzhuzhu -p123 password 'new_password' //123为旧密码
```

  
＝＝＝丢失root用户密码

```
# vim /etc/my.cnf
[mysqld]
skip-grant-tables
# service mysqld restart
# mysql -uroot
mysql> UPDATE mysql.user SET password=password(‘new_password’)
WHERE user=’root’ AND host=’localhost’;
mysql> FLUSH PRIVILEGES;

```

  
三、MySQL权限管理  
权限应用的顺序：  
user \(Y|N\) ==> db ==> tables\_priv ==> columns\_priv

**查看用户权限**

```
mysql> select Host,User,select_priv,insert_priv,update_priv,delete_priv from user;
```

![](http://image.ownit.top/csdn/20190418234838303.png)  
  
语法格式：  
grant 权限列表 on 库名.表名 to 用户名\@'客户端主机' \[identified by '密码' with option参数\];  
\==权限列表 all 所有权限（不包括授权权限）  
select,update  
  
\==数据库.表名 \*.\* 所有库下的所有表 Global level  
web.\* web库下的所有表 Database level  
web.stu\_info web库下的stu\_info表 Table level  
SELECT \(col1\), INSERT \(col1,col2\) ON mydb.mytbl Column level  
  
\==客户端主机 \% 所有主机  
192.168.2.\% 192.168.2.0网段的所有主机  
192.168.2.168 指定主机  
localhost 指定主机  
  
with\_option参数  
GRANT OPTION： 授权选项  
MAX\_QUERIES\_PER\_HOUR： 定义每小时允许执行的查询数  
MAX\_UPDATES\_PER\_HOUR： 定义每小时允许执行的更新数  
MAX\_CONNECTIONS\_PER\_HOUR： 定义每小时可以建立的连接数  
MAX\_USER\_CONNECTIONS： 定义单个用户同时可以建立的连接数

 

**grant 普通数据用户，查询、插入、更新、删除 数据库中所有表数据的权利。**

- grant select on testdb.\* to common\_user\@’\%’
- grant insert on testdb.\* to common\_user\@’\%’
- grant update on testdb.\* to common\_user\@’\%’
- grant delete on testdb.\* to common\_user\@’\%’

** MySQL 命令来替代：**

- grant select, insert, update, delete on testdb.\* to common\_user\@’\%’

grant 数据库开发人员，创建表、索引、视图、存储过程、函数。。。等权限。

**grant 创建、修改、删除 MySQL 数据表结构权限。**

- grant create on testdb.\* to developer\@’192.168.0.\%’;
- grant alter on testdb.\* to developer\@’192.168.0.\%’;
- grant drop on testdb.\* to developer\@’192.168.0.\%’;

**grant 操作 MySQL 外键权限。**

- grant references on testdb.\* to developer\@’192.168.0.\%’;

**grant 操作 MySQL 临时表权限。**

- grant create temporary tables on testdb.\* to developer\@’192.168.0.\%’;

**grant 操作 MySQL 索引权限。**

- grant index on testdb.\* to developer\@’192.168.0.\%’;

**grant 操作 MySQL 视图、查看视图源代码 权限**。

- grant create view on testdb.\* to developer\@’192.168.0.\%’;
- grant show view on testdb.\* to developer\@’192.168.0.\%’;

**grant 操作 MySQL 存储过程、函数 权限。**

- grant create routine on testdb.\* to developer\@’192.168.0.\%’; -- now, can show procedure status
- grant alter routine on testdb.\* to developer\@’192.168.0.\%’; -- now, you can drop a procedure
- grant execute on testdb.\* to developer\@’192.168.0.\%’;

**grant 普通 DBA 管理某个 MySQL 数据库的权限**。

- grant all privileges on testdb to dba\@’localhost’

 

**grant 高级 DBA 管理 MySQL 中所有数据库的权限。**

- grant all on \*.\* to dba\@’localhost’

### **MySQL grant 权限，分别可以作用在多个层次上。**

**1\. grant 作用在整个 MySQL 服务器上：**

- grant select on \*.\* to dba\@localhost; -- dba 可以查询 MySQL 中所有数据库中的表。
- grant all on \*.\* to dba\@localhost; -- dba 可以管理 MySQL 中的所有数据库

**2\. grant 作用在单个数据库上：**

- grant select on testdb.\* to dba\@localhost; -- dba 可以查询 testdb 中的表。

**3\. grant 作用在单个数据表上：**

- grant select, insert, update, delete on testdb.orders to dba\@localhost;

**4\. grant 作用在表中的列上：**

- grant select\(id, se, rank\) on testdb.apache\_log to dba\@localhost;

**5\. grant 作用在存储过程、函数上：**

- grant execute on procedure testdb.pr\_add to ’dba’\@’localhost’
- grant execute on function testdb.fn\_add to ’dba’\@’localhost’

**注意：修改完权限以后 一定要刷新服务，或者重启服务，刷新服务用：FLUSH PRIVILEGES。**

Grant示例：  
GRANT ALL ON \*.\* TO admin1\@'\%' IDENTIFIED BY 'localhost';  
  
GRANT ALL ON \*.\* TO admin2\@'\%' IDENTIFIED BY 'localhost' WITH GRANT OPTION;  
  
GRANT ALL ON bbs.\* TO admin3\@'\%' IDENTIFIED BY 'localhost';  
  
GRANT ALL ON bbs.user TO admin4\@'\%' IDENTIFIED BY 'localhost';  
  
GRANT SELECT\(col1\),INSERT\(col2,col3\) ON bbs.user TO admin5\@'\%' IDENTIFIED BY 'localhost';  
  
  
回收权限REVOKE  
查看权限  
SHOW GRANTS\\G  
SHOW GRANTS FOR admin1\@'\%'\\G  
  
回收权限REVOKE  
语法：  
REVOKE 权限列表 ON 数据库名 FROM 用户名\@‘客户端主机’  
  
示例：  
REVOKE DELETE ON \*.\* FROM admin1\@’\%’; //回收部分权限  
REVOKE ALL PRIVILEGES ON \*.\* FROM admin2\@’\%’; //回收所有权限  
REVOKE ALL PRIVILEGES,GRANT OPTION ON \*.\* FROM 'admin2'\@'\%';  
\========================================================