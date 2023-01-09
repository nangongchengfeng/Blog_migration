+++
author = "南宫乘风"
title = "Docker安装MySQL集群【读写分离】"
date = "2019-12-19 11:16:59"
tags=['docker', 'mysql', '集群', '容器', '主从']
categories=['Docker', 'MySQL']
image = "post/4kdongman/70.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103609082](https://blog.csdn.net/heian_99/article/details/103609082)

## [Centos7系统Docker安装](https://blog.csdn.net/heian_99/article/details/103452223)

**目录**

[Centos7系统Docker安装](#Centos7%E7%B3%BB%E7%BB%9FDocker%E5%AE%89%E8%A3%85)

**目录**

[Centos7系统Docker安装](#Centos7%E7%B3%BB%E7%BB%9FDocker%E5%AE%89%E8%A3%85)

[1、下载mysql镜像](#1%E3%80%81%E4%B8%8B%E8%BD%BDmysql%E9%95%9C%E5%83%8F)

[2、创建Master实例并启动](#2%E3%80%81%E5%88%9B%E5%BB%BAMaster%E5%AE%9E%E4%BE%8B%E5%B9%B6%E5%90%AF%E5%8A%A8)

[参数说明](#%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E)

[3、创建Slave实例并启动](#3%E3%80%81%E5%88%9B%E5%BB%BASlave%E5%AE%9E%E4%BE%8B%E5%B9%B6%E5%90%AF%E5%8A%A8)

[4、添加master主从复制部分配置](#4%E3%80%81%E6%B7%BB%E5%8A%A0master%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6%E9%83%A8%E5%88%86%E9%85%8D%E7%BD%AE)

[5、添加Slave主从复制部分配置](#5%E3%80%81%E6%B7%BB%E5%8A%A0master%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6%E9%83%A8%E5%88%86%E9%85%8D%E7%BD%AE)

[6、为master授权用户来他的同步数据](#6%E3%80%81%E4%B8%BAmaster%E6%8E%88%E6%9D%83%E7%94%A8%E6%88%B7%E6%9D%A5%E4%BB%96%E7%9A%84%E5%90%8C%E6%AD%A5%E6%95%B0%E6%8D%AE)

![20191219104313635.png](https://img-blog.csdnimg.cn/20191219104313635.png)

## 1、下载mysql镜像

```
 docker search mysql

```

![20191219094601685.png](https://img-blog.csdnimg.cn/20191219094601685.png)

```
 docker pull mysql:5.7

```

![20191219094626809.png](https://img-blog.csdnimg.cn/20191219094626809.png)

```
docker images

```

![20191219094647232.png](https://img-blog.csdnimg.cn/20191219094647232.png)

## 2、创建Master实例并启动

```
docker run -p 3307:3306 --name mysql-master \
-v /mydata/mysql/master/log:/var/log/mysql \
-v /mydata/mysql/master/data:/var/lib/mysql \
-v /mydata/mysql/master/conf:/etc/mysql \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:5.7 
```

### **参数说明**
1.        -p 3307:3306：将容器的3306端口映射到主机的3307端口1.        -v /mydata/mysql/master/conf:/etc/mysql：将配置文件夹挂在到主机1.        -v /mydata/mysql/master/log:/var/log/mysql：将日志文件夹挂载到主机1.        -v /mydata/mysql/master/data:/var/lib/mysql/：将配置文件夹挂载到主机1.        -e MYSQL_ROOT_PASSWORD=root：初始化root用户的密码
![20191219095018294.png](https://img-blog.csdnimg.cn/20191219095018294.png)

****修改master********基本配置****

```
vim /mydata/mysql/master/conf/my.cnf
```

```
[client]
default-character-set=utf8
 
[mysql]
default-character-set=utf8
 
[mysqld]
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake
skip-name-resolve

```

**注意：skip-name-resolve一定要加，不然连接mysql会超级慢**

![20191219102412144.png](https://img-blog.csdnimg.cn/20191219102412144.png)

## 3、创建Slave实例并启动

```
docker run -p 3316:3306 --name mysql-slaver-01 \
-v /mydata/mysql/slaver/log:/var/log/mysql \
-v /mydata/mysql/slaver/data:/var/lib/mysql \
-v /mydata/mysql/slaver/conf:/etc/mysql \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:5.7 

```

****修改slave********基本配置****

```
vim /mydata/mysql/slaver/conf/my.cnf
```

```
[client]
default-character-set=utf8
 
[mysql]
default-character-set=utf8
 
[mysqld]
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake
skip-name-resolve

```

![20191219103328724.png](https://img-blog.csdnimg.cn/20191219103328724.png)

## ****4、添加master********主从复制部分配置****

```
vim /mydata/mysql/master/conf/my.cnf
```

```
server_id=1
log-bin=mysql-bin
read-only=0
binlog-do-db=gmall_ums
binlog-do-db=gmall_pms
binlog-do-db=gmall_oms
binlog-do-db=gmall_sms
binlog-do-db=gmall_cms


replicate-ignore-db=mysql
replicate-ignore-db=sys
replicate-ignore-db=information_schema
replicate-ignore-db=performance_schema

```

![20191219104122584.png](https://img-blog.csdnimg.cn/20191219104122584.png)

**重启容器**

## ****5、添加****Slave****主从复制部分配置****

```
server_id=2
log-bin=mysql-bin
read-only=1
binlog-do-db=gmall_ums
binlog-do-db=gmall_pms
binlog-do-db=gmall_oms
binlog-do-db=gmall_sms
binlog-do-db=gmall_cms


replicate-ignore-db=mysql
replicate-ignore-db=sys
replicate-ignore-db=information_schema
replicate-ignore-db=performance_schema

```

![20191219104517664.png](https://img-blog.csdnimg.cn/20191219104517664.png)

**重启容器**

![20191219104749895.png](https://img-blog.csdnimg.cn/20191219104749895.png)

## 6、为master授权用户来他的同步数据

![20191219104926649.png](https://img-blog.csdnimg.cn/20191219104926649.png)

**1、进入主库**

```
docker exec -it 4fdd7f265228 /bin/bash

```

![20191219105108322.png](https://img-blog.csdnimg.cn/20191219105108322.png)

**2、进入主库mysql数据库**

```
 mysql -u root -p

```

![20191219105224448.png](https://img-blog.csdnimg.cn/20191219105224448.png)
- ** 1）、授权root可以远程访问（ 主从无关，为了方便我们远程连接mysql）**
```
grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;
```

```
flush privileges;
```

![20191219110012867.png](https://img-blog.csdnimg.cn/20191219110012867.png)
- **   2）、添加用来同步的用户**
```
   GRANT REPLICATION SLAVE ON *.* to 'backup'@'%' identified by '123456';
```

![20191219110220461.png](https://img-blog.csdnimg.cn/20191219110220461.png)
- **3）、查看数据库的状态**
```
   show master status\G;
```

![20191219110417347.png](https://img-blog.csdnimg.cn/20191219110417347.png)

**3、进入从库mysql数据库**

![20191219105407554.png](https://img-blog.csdnimg.cn/20191219105407554.png)
- ** 1）、授权root可以远程访问（ 主从无关，为了方便我们远程连接mysql）**
```
grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;
```

```
flush privileges;
```

![20191219110012867.png](https://img-blog.csdnimg.cn/20191219110012867.png)

 
- ** 2）、设置主库连接**
```
change master to master_host='192.168.116.129',master_user='backup',master_password='123456',master_log_file='mysql-bin.000001',master_log_pos=0,master_port=3307;
```

![20191219110811621.png](https://img-blog.csdnimg.cn/20191219110811621.png)
- **  3）、启动从库同步**
```
start slave;
```

![2019121911090798.png](https://img-blog.csdnimg.cn/2019121911090798.png)
- **  4）、查看从库状态**
```
     show slave status\G;
```

 

![20191219110953235.png](https://img-blog.csdnimg.cn/20191219110953235.png)

至此主从配置完成；

**总结：**

**         1）、主从数据库在自己配置文件中声明需要同步哪个数据库，忽略哪个数据库等信息。并且server-id不能一样**

**         2）、主库授权某个账号密码来同步自己的数据**

**         3）、从库使用这个账号密码连接主库来同步数据**

**演示效果**

![20191219111351514.png](https://img-blog.csdnimg.cn/20191219111351514.png)

 
