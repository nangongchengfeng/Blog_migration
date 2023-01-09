+++
author = "南宫乘风"
title = "MySQL二进制安装（版本：5.7.26）"
date = "2020-06-09 16:28:58"
tags=['mysql', 'linux', '数据库', '二进制', '5.7.26']
categories=['MySQL']
image = "post/4kdongman/23.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/106644755](https://blog.csdn.net/heian_99/article/details/106644755)

 

**目录**

[1、用户的创建处理原始环境](#1%E3%80%81%E7%94%A8%E6%88%B7%E7%9A%84%E5%88%9B%E5%BB%BA%E5%A4%84%E7%90%86%E5%8E%9F%E5%A7%8B%E7%8E%AF%E5%A2%83)

[2、下载，上传文件](#2%E3%80%81%E4%B8%8B%E8%BD%BD%EF%BC%8C%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6)

[3、解压二进制包](#3%E3%80%81%E8%A7%A3%E5%8E%8B%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%8C%85)

[4、添加一个磁盘，挂载/data数据](#4%E3%80%81%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA%E7%A3%81%E7%9B%98%EF%BC%8C%E6%8C%82%E8%BD%BD%2Fdata%E6%95%B0%E6%8D%AE)

[5、创建数据路径并授权](#5%E3%80%81%E5%88%9B%E5%BB%BA%E6%95%B0%E6%8D%AE%E8%B7%AF%E5%BE%84%E5%B9%B6%E6%8E%88%E6%9D%83)

[6、设置环境变量](#6%E3%80%81%E8%AE%BE%E7%BD%AE%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)

[7、Mysql账号授权相应的文件](#7%E3%80%81Mysql%E8%B4%A6%E5%8F%B7%E6%8E%88%E6%9D%83%E7%9B%B8%E5%BA%94%E7%9A%84%E6%96%87%E4%BB%B6)

[8、数据库初始化 ](#8%E3%80%81%E6%95%B0%E6%8D%AE%E5%BA%93%E5%88%9D%E5%A7%8B%E5%8C%96%C2%A0)

[9、配置文件的准备](#9%E3%80%81%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E7%9A%84%E5%87%86%E5%A4%87)

[10、启动数据库](#10%E3%80%81%E5%90%AF%E5%8A%A8%E6%95%B0%E6%8D%AE%E5%BA%93)

[11、如何分析处理MySQL数据库无法启动](#11%E3%80%81%E5%A6%82%E4%BD%95%E5%88%86%E6%9E%90%E5%A4%84%E7%90%86MySQL%E6%95%B0%E6%8D%AE%E5%BA%93%E6%97%A0%E6%B3%95%E5%90%AF%E5%8A%A8)

[12、管理员密码的设定（root@localhost）](#12%E3%80%81%E7%AE%A1%E7%90%86%E5%91%98%E5%AF%86%E7%A0%81%E7%9A%84%E8%AE%BE%E5%AE%9A%EF%BC%88root%40localhost%EF%BC%89)

[13、管理员用户密码忘记了？](#13%E3%80%81%E7%AE%A1%E7%90%86%E5%91%98%E7%94%A8%E6%88%B7%E5%AF%86%E7%A0%81%E5%BF%98%E8%AE%B0%E4%BA%86%EF%BC%9F)

[14、启动数据库到维护模式](#14%E3%80%81%E5%90%AF%E5%8A%A8%E6%95%B0%E6%8D%AE%E5%BA%93%E5%88%B0%E7%BB%B4%E6%8A%A4%E6%A8%A1%E5%BC%8F)

>  
 RDBMS : 关系型数据库 管理系统 
 NoSQL : 非关系型的 
 NewSQL : 新型的分布式解决方案 




### 1、用户的创建处理原始环境



```
[root@db01 ~]# yum remove mariadb-libs-5.5.60-1.el7_5.x86_64 -y
[root@db01 ~]# rpm -qa |grep mariadb
[root@db01 ~]# useradd -s /sbin/nologin mysql
```

MySQL 5.7.26 二进制版本安装

[https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz](https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz)



### 2、下载，上传文件

```
[root@db01 ~]# mkdir -p /server/tools
[root@db01 ~]# cd /server/tools/
[root@db01 /server/tools]# yum install -y lrzsz
[root@db01 /server/tools]# ls
mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
```

![20200609161515666.png](https://img-blog.csdnimg.cn/20200609161515666.png)



### 3、解压二进制包

```
[root@db01 /server/tools]# tar xf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz 
[root@db01 ~]# mkdir /application
[root@db01 /server/tools]# mv mysql-5.7.26-linux-glibc2.12-x86_64  /application/mysql
```

 

**基本思路**：把软件存放位置和数据存放位置分开，确保数据安全

![20200609161557901.png](https://img-blog.csdnimg.cn/20200609161557901.png)

### 4、添加一个磁盘，挂载/data数据



![20200609161751738.png](https://img-blog.csdnimg.cn/20200609161751738.png)

![20200609161809689.png](https://img-blog.csdnimg.cn/20200609161809689.png)

### 5、创建数据路径并授权

```
[root@db01 ~]# mkfs.xfs /dev/sdc
[root@db01 ~]# mkdir /mysql
[root@db01 ~]# blkid
[root@db01 ~]# vim /etc/fstab 
[root@db01 ~]# UUID="7d7814c3-1ad2-4622-a435-7086d05d6c55" /mysql xfs defaults 0 0
[root@db01 ~]# mount -a
[root@db01 ~]# df -h
```

![20200609161923453.png](https://img-blog.csdnimg.cn/20200609161923453.png)

![20200609161932212.png](https://img-blog.csdnimg.cn/20200609161932212.png)

![20200609161940465.png](https://img-blog.csdnimg.cn/20200609161940465.png)

### 

### 6、设置环境变量



```
vim /etc/profile
export PATH=/application/mysql/bin:$PATH
[root@db01 ~]# source /etc/profile
[root@db01 ~]# mysql -V
mysql  Ver 14.14 Distrib 5.7.26, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```

![20200609161839500.png](https://img-blog.csdnimg.cn/20200609161839500.png)

### 7、Mysql账号授权相应的文件

```
授权 
 chown -R mysql.mysql /application/*
 chown -R mysql.mysql /mysql
```

### 8、数据库初始化 

```
5.6 版本 初始化命令  /application/mysql/scripts/mysql_install_db 
# 5.7 版本
[root@db01 ~]# mkdir /mysql/mysql/data -p 
[root@db01 ~]# chown -R mysql.mysql /mysql
[root@db01 ~]# mysqld --initialize --user=mysql --basedir=/application/mysql --datadir=/mysql/mysql/data 
```

![20200609162239455.png](https://img-blog.csdnimg.cn/20200609162239455.png)

 

**说明：**



**--initialize 参数：**
- 1. 对于密码复杂度进行定制：12位，4种- 2. 密码过期时间：180- 3. 给root@localhost用户设置临时密码
**--initialize-insecure 参数：**

无限制，无临时密码



```
[root@db01 /data/mysql/data]# \rm -rf /data/mysql/data/*
[root@db01 ~]# mysqld --initialize-insecure --user=mysql --basedir=/application/mysql --datadir=/mysql/mysql/data
```

没有密码

![20200609162224248.png](https://img-blog.csdnimg.cn/20200609162224248.png)

### 9、配置文件的准备



```
cat &gt;/etc/my.cnf &lt;&lt;EOF
[mysqld]
user=mysql
basedir=/application/mysql
datadir=/mysql/mysql/data
socket=/tmp/mysql.sock
server_id=6
port=3306
[mysql]
socket=/tmp/mysql.sock
EOF
```

### 10、启动数据库



**1. sys-v**

```
[root@db01 /etc/init.d]# cp /application/mysql/support-files/mysql.server  /etc/init.d/mysqld 
[root@db01 /etc/init.d]# service mysqld restart
```

![20200609162358130.png](https://img-blog.csdnimg.cn/20200609162358130.png)

**2. systemd**



注意： sysv方式启动过的话，需要先提前关闭，才能以下方式登录

```
cat &gt;/etc/systemd/system/mysqld.service &lt;&lt;EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/etc/my.cnf
LimitNOFILE = 5000
EOF
```

![20200609162443134.png](https://img-blog.csdnimg.cn/20200609162443134.png)

### 11、如何分析处理MySQL数据库无法启动



without updating PID 类似错误

**查看日志：**

>  
 在哪？ 
 /data/mysql/data/主机名.err 
 [ERROR] 上下文 


**可能情况：**

>  
 /etc/my.cnf 路径不对等 
 /tmp/mysql.sock文件修改过 或 删除过 
 数据目录权限不是mysql 
 参数改错了 




### 12、管理员密码的设定（root@localhost）



```
[root@db01 ~]# mysqladmin -uroot -p password oldboy123
Enter password: 
```

### 13、管理员用户密码忘记了？



```
--skip-grant-tables  #跳过授权表
--skip-networking    #跳过远程登录
```

### 14、启动数据库到维护模式



```
[root@db01 ~]# mysqld_safe --skip-grant-tables --skip-networking &amp;
```

登录并修改密码



```
mysql&gt; alter user root@'localhost' identified by '1';
ERROR 1290 (HY000): The MySQL server is running with the --skip-grant-tables option so it cannot execute this statement
mysql&gt; flush privileges;
mysql&gt; alter user root@'localhost' identified by '1';
Query OK, 0 rows affected (0.01 sec)
```

![20200609162657818.png](https://img-blog.csdnimg.cn/20200609162657818.png)

关闭数据库，正常启动验证



 


