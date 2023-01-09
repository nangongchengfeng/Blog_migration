+++
author = "南宫乘风"
title = "MySQL安全机制"
date = "2019-04-18 23:55:30"
tags=[]
categories=['MySQL']
image = "post/4kdongman/98.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89390371](https://blog.csdn.net/heian_99/article/details/89390371)

**MySQL安全机制**<br><br> ========================================================<br>MySQL权限表<br> MySQL用户管理<br> MySQL权限管理<br><br><br> 一、MySQL权限表<br> mysql.user Global level<br> 用户字段<br> 权限字段<br> 安全字段<br> 资源控制字段<br> mysql.db、mysql.host Database level<br> 用户字段<br> 权限字段<br> mysql.tables_priv Table level<br> mysql.columns_priv Column level<br> mysql.procs_priv<br><br><br> 二、MySQL用户管理<br> 1. 登录和退出MySQL<br> 示例：<br> mysql -h192.168.5.240 -P 3306 -u root -p123 mysql -e ‘select user,host from user’<br> -h 指定主机名<br> -P MySQL服务器端口<br> -u 指定用户名<br> -p 指定登录密码<br> 此处mysql为指定登录的数据库<br> -e 接SQL语句

查看用户表

用户管理

```
mysql&gt;use mysql;
```

查看

```
mysql&gt; select host,user,password from user ;
```

![20190418231408187.png](https://img-blog.csdnimg.cn/20190418231408187.png)<br> 2. 创建用户<br> 方法一：CREATE USER语句创建

```
CREATE USER zhang@localhost IDENTIFIED BY "zhang";

```

刷新表

```
 flush privileges;

```

![20190418232909974.png](https://img-blog.csdnimg.cn/20190418232909974.png)<br> 方法二： INSERT语句创建

```
Imysql&gt; INSERT INTO mysql.user(user,host, password,ssl_cipher,x509_issuer,x509_subject)
    -&gt;  VALUES("user2","localhost",password("123456"),"","","");
Query OK, 1 row affected (0.00 sec)
```

```
 flush privileges;
```

![20190418233619983.png](https://img-blog.csdnimg.cn/20190418233619983.png)

方法三： GRANT语句创建

```
mysql&gt; GRANT SELECT ON *.* TO user3@"localhost" IDENTIFIED BY "123456";
Query OK, 0 rows affected (0.00 sec)

```

```
mysql&gt; FLUSH PRIVILEGES;

```

![20190418233745506.png](https://img-blog.csdnimg.cn/20190418233745506.png)<br><br> 3. 删除用户<br> 方法一：DROP USER语句删除

```
mysql&gt; DROP USER user1@"localhost";
Query OK, 0 rows affected (0.00 sec)

```

<br>![20190418233935933.png](https://img-blog.csdnimg.cn/20190418233935933.png)<br> 方法二：DELETE语句删除

```
mysql&gt; delete from user
    -&gt; where user="user2" and host="localhost";
Query OK, 1 row affected (0.00 sec)
```

 

```
mysql&gt; flush privileges;

```

![20190418234240966.png](https://img-blog.csdnimg.cn/20190418234240966.png)<br><br><br> 4. 修改用户密码<br> ＝＝＝root修改自己密码<br> 方法一：

```
# mysqladmin -uroot -p123 password 'new_password' //123为旧密码
```

<br><br> 方法二：

```
UPDATE mysql.user SET password=password(‘new_password’)
WHERE user=’root’ AND host=’localhost’;
FLUSH PRIVILEGES;
```

<br><br> 方法三：

```
SET PASSWORD=password(‘new_password’);
FLUSH PRIVILEGES;
```

<br><br><br> ==root修改其他用户密码<br> 方法一：

```
SET PASSWORD FOR user3@’localhost’=password(‘new_password’);
FLUSH PRIVILEGES;
```

<br><br> 方法二：

```
UPDATE mysql.user SET password=password(‘new_password’)
WHERE user=’user3’ AND host=’localhost’;
FLUSH PRIVILEGES;

```

<br> 方法三：

```
GRANT SELECT ON *.* TO user3@’localhost’ IDENTIFIED BY ‘localhost’;
FLUSH PRIVILEGES;

```

<br><br> ＝＝＝普通用户修改自己密码<br> 方法一：

```
SET password=password(‘new_password’);
```

<br><br> 方法二：

```
# mysqladmin -uzhuzhu -p123 password 'new_password' //123为旧密码

```

<br> ＝＝＝丢失root用户密码

```
# vim /etc/my.cnf
[mysqld]
skip-grant-tables
# service mysqld restart
# mysql -uroot
mysql&gt; UPDATE mysql.user SET password=password(‘new_password’)
WHERE user=’root’ AND host=’localhost’;
mysql&gt; FLUSH PRIVILEGES;


```

<br> 三、MySQL权限管理<br> 权限应用的顺序：<br> user (Y|N) ==&gt; db ==&gt; tables_priv ==&gt; columns_priv

**查看用户权限**

```
mysql&gt; select Host,User,select_priv,insert_priv,update_priv,delete_priv from user;
```

![20190418234838303.png](https://img-blog.csdnimg.cn/20190418234838303.png)<br><br> 语法格式：<br> grant 权限列表 on 库名.表名 to 用户名@'客户端主机' [identified by '密码' with option参数];<br> ==权限列表 all 所有权限（不包括授权权限）<br> select,update<br><br> ==数据库.表名 *.* 所有库下的所有表 Global level<br> web.* web库下的所有表 Database level<br> web.stu_info web库下的stu_info表 Table level<br> SELECT (col1), INSERT (col1,col2) ON mydb.mytbl Column level<br><br> ==客户端主机 % 所有主机<br> 192.168.2.% 192.168.2.0网段的所有主机<br> 192.168.2.168 指定主机<br> localhost 指定主机<br><br> with_option参数<br> GRANT OPTION： 授权选项<br> MAX_QUERIES_PER_HOUR： 定义每小时允许执行的查询数<br> MAX_UPDATES_PER_HOUR： 定义每小时允许执行的更新数<br> MAX_CONNECTIONS_PER_HOUR： 定义每小时可以建立的连接数<br> MAX_USER_CONNECTIONS： 定义单个用户同时可以建立的连接数

 

**grant 普通数据用户，查询、插入、更新、删除 数据库中所有表数据的权利。**
- grant select on testdb.* to common_user@’%’- grant insert on testdb.* to common_user@’%’- grant update on testdb.* to common_user@’%’- grant delete on testdb.* to common_user@’%’
** MySQL 命令来替代：**
- grant select, insert, update, delete on testdb.* to common_user@’%’
grant 数据库开发人员，创建表、索引、视图、存储过程、函数。。。等权限。

**grant 创建、修改、删除 MySQL 数据表结构权限。**
- grant create on testdb.* to developer@’192.168.0.%’;- grant alter on testdb.* to developer@’192.168.0.%’;- grant drop on testdb.* to developer@’192.168.0.%’;
**grant 操作 MySQL 外键权限。**
- grant references on testdb.* to developer@’192.168.0.%’;
**grant 操作 MySQL 临时表权限。**
- grant create temporary tables on testdb.* to developer@’192.168.0.%’;
**grant 操作 MySQL 索引权限。**
- grant index on testdb.* to developer@’192.168.0.%’;
**grant 操作 MySQL 视图、查看视图源代码 权限**。
- grant create view on testdb.* to developer@’192.168.0.%’;- grant show view on testdb.* to developer@’192.168.0.%’;
**grant 操作 MySQL 存储过程、函数 权限。**
- grant create routine on testdb.* to developer@’192.168.0.%’; -- now, can show procedure status- grant alter routine on testdb.* to developer@’192.168.0.%’; -- now, you can drop a procedure- grant execute on testdb.* to developer@’192.168.0.%’;
**grant 普通 DBA 管理某个 MySQL 数据库的权限**。
- grant all privileges on testdb to dba@’localhost’
 

**grant 高级 DBA 管理 MySQL 中所有数据库的权限。**
- grant all on *.* to dba@’localhost’
### **MySQL grant 权限，分别可以作用在多个层次上。**

**1. grant 作用在整个 MySQL 服务器上：**
- grant select on *.* to dba@localhost; -- dba 可以查询 MySQL 中所有数据库中的表。- grant all on *.* to dba@localhost; -- dba 可以管理 MySQL 中的所有数据库
**2. grant 作用在单个数据库上：**
- grant select on testdb.* to dba@localhost; -- dba 可以查询 testdb 中的表。
**3. grant 作用在单个数据表上：**
- grant select, insert, update, delete on testdb.orders to dba@localhost;
**4. grant 作用在表中的列上：**
- grant select(id, se, rank) on testdb.apache_log to dba@localhost;
**5. grant 作用在存储过程、函数上：**
- grant execute on procedure testdb.pr_add to ’dba’@’localhost’- grant execute on function testdb.fn_add to ’dba’@’localhost’
**注意：修改完权限以后 一定要刷新服务，或者重启服务，刷新服务用：FLUSH PRIVILEGES。**

Grant示例：<br> GRANT ALL ON *.* TO admin1@'%' IDENTIFIED BY 'localhost';<br><br> GRANT ALL ON *.* TO admin2@'%' IDENTIFIED BY 'localhost' WITH GRANT OPTION;<br><br> GRANT ALL ON bbs.* TO admin3@'%' IDENTIFIED BY 'localhost';<br><br> GRANT ALL ON bbs.user TO admin4@'%' IDENTIFIED BY 'localhost';<br><br> GRANT SELECT(col1),INSERT(col2,col3) ON bbs.user TO admin5@'%' IDENTIFIED BY 'localhost';<br><br><br> 回收权限REVOKE<br> 查看权限<br> SHOW GRANTS\G<br> SHOW GRANTS FOR admin1@'%'\G<br><br> 回收权限REVOKE<br> 语法：<br> REVOKE 权限列表 ON 数据库名 FROM 用户名@‘客户端主机’<br><br> 示例：<br> REVOKE DELETE ON *.* FROM admin1@’%’; //回收部分权限<br> REVOKE ALL PRIVILEGES ON *.* FROM admin2@’%’; //回收所有权限<br> REVOKE ALL PRIVILEGES,GRANT OPTION ON *.* FROM 'admin2'@'%';<br> ========================================================
