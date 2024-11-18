---
author: 南宫乘风
categories:
- Linux实战操作
date: 2019-09-24 10:47:15
description: 目录下安装与部署介绍介绍安装与部署、临时关闭、永久关闭、安装环境、安装环境、安装下安装与部署介绍是一个基于界面的提供分布式系统监视以及网络监视功能的企业级的开源解决方案。能监视各种网络参数，保证服务器。。。。。。。
image: ../../title_pic/36.jpg
slug: '201909241047'
tags:
- 技术记录
title: Centos7下zabbix安装与部署
---

<!--more-->

**目录**

 

[Centos7下zabbix安装与部署](#Centos7%E4%B8%8Bzabbix%E5%AE%89%E8%A3%85%E4%B8%8E%E9%83%A8%E7%BD%B2)

[1.Zabbix介绍](#1.Zabbix%E4%BB%8B%E7%BB%8D)

[2.LAMP/LNMP介绍](#2.LAMP%2FLNMP%E4%BB%8B%E7%BB%8D)

[3.Zabbix安装与部署](#3.Zabbix%E5%AE%89%E8%A3%85%E4%B8%8E%E9%83%A8%E7%BD%B2)

[1、临时关闭](#1%E3%80%81%E4%B8%B4%E6%97%B6%E5%85%B3%E9%97%AD)

[2、永久关闭](#2%E3%80%81%E6%B0%B8%E4%B9%85%E5%85%B3%E9%97%AD)

[3 、安装环境](<#3 、安装环境>)

[4、安装zabbix](#4%E3%80%81%E5%AE%89%E8%A3%85zabbix)

 

# Centos7下zabbix安装与部署

![](format,png)

 

## 1.Zabbix介绍

![](format,png)

- zabbix是一个基于WEB界面的提供分布式系统监视以及网络监视功能的企业级的开源解决方案。

- zabbix能监视各种网络参数，保证服务器系统的安全运营；并提供灵活的通知机制以让系统管理员快速定位/解决存在的各种问题。

- zabbix由2部分构成，zabbix server与可选组件zabbix agent。

- zabbix server可以通过SNMP，zabbix agent，ping，端口监视等方法提供对远程服务器/网络状态的监视，数据收集等功能，它可以运行在Linux，Solaris，HP-UX，AIX，Free BSD，Open BSD，OS X等平台上。

 

## 2.LAMP/LNMP介绍

- LAMP：Linux+Apache+Mysql/MariaDB+Perl/PHP/Python一组常用来搭建动态网站或者服务器的开源软件，本身都是各自独立的程序，但是因为常被放在一起使用，拥有了越来越高的兼容度，共同组成了一个强大的Web应用程序平台。

- LNMP：LNMP指的是一个基于CentOS/Debian编写的Nginx、PHP、MySQL、phpMyAdmin、eAccelerator一键安装包。可以在VPS、独立主机上轻松的安装LNMP生产环境。
- L：linux

- A：apache

- N：nginx

- M：mysql,mariaDB

- P：php,python,perl

 

 

## 3.Zabbix安装与部署

Zabbix的安装

```html
关闭SeLinux

临时关闭：setenforce 0
```

![](format,png)

```html
永久关闭：vi /etc/selinux/config
```

![](format,png)

关闭防火墙

### 1、临时关闭

```html
systemctl stop firewalld.service
```

![](format,png)

### 2、永久关闭

```html
systemctl disable firewalld.service
```

![](format,png)

### 3 、安装环境

LAMP 

大家可以看下面的博客，安装LAMP环境

[Linux\(Centos7\)搭建LAMP\(Apache+PHP+Mysql环境\)](https://blog.csdn.net/heian_99/article/details/101203824)

 

 

### 4、安装zabbix

\(1\)下载包

```
rpm -ivh http://repo.zabbix.com/zabbix/3.4/rhel/7/x86_64/zabbix-release-3.4-2.el7.noarch.rpm
```

![](../../image/20190924100954220.png)

\(2\)安装zabbix的包

```
yum install -y zabbix-server-mysql zabbix-get zabbix-web zabbix-web-mysql zabbix-agent zabbix-sender
```

![](../../image/20190924101027169.png)

4、创建一个zabbix库并设置为utf8的字符编码格式

```
create database zabbix character set utf8 collate utf8_bin;
```

![](../../image/20190924101126621.png)

![](../../image/20190924101400438.png)

创建账户并且授权设置密码

```
grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';
```

给来自loclhost的用户zabbxi分配可对数据库zabbix所有表进行所有操作的权限，并且设定密码为zabbix

![](../../image/20190924101441698.png)

刷新

```html
flush privileges;
```

![](../../image/20190924101452792.png)

exit退出

5、导入表

切换到此目录下

```
cd /usr/share/doc/zabbix-server-mysql-3.2.10/
```

![](../../image/20190924101533563.png)

进行解压

```html
gunzip create.sql.gz
```

![](../../image/20190924101622255.png)

对表进行导入

```
[root@wei zabbix-server-mysql-3.4.15]# mysql -u zabbix -p zabbix
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 5.6.45 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| zabbix             |
+--------------------+
2 rows in set (0.00 sec)

mysql> use zabbix;
Database changed
mysql> source create.sql
```

![](../../image/20190924102103971.png)

6、配置zabbix server配置文件

配置文件目录

```
cd /etc/zabbix
```

 

对zabbix\_server.conf进行配置

![](../../image/20190924102153566.png)

![](../../image/20190924102728969.png)

运行zabbix-server服务

开机自启zabbix-server服务

![](../../image/20190924102933145.png)

7、配置php

```
cd /etc/httpd/conf.d
```

![](../../image/20190924103011857.png)

配置时间

```
vim zabbix.conf
```

![](../../image/20190924103139266.png)

```
Systemctl restart httpd
```

![](../../image/20190924103306743.png)

8、登陆zabbix网址设置

192.168.85.11/zabbix

 ![](../../image/20190924103349762.png)

![](../../image/2019092410341084.png)

password是我们设置的数据库密码zabbix

![](../../image/20190924103431161.png)

![](../../image/20190924103503374.png)

![](../../image/20190924103518782.png)

![](../../image/20190924103533263.png)

**登陆账户是Admin**

**密码是zabbix**

![](../../image/20190924103554857.png)

9、设置中文

![](../../image/20190924103618782.png)

 

![](../../image/20190924103718245.png)

![](../../image/20190924103738136.png)

10、对服务器自身进行监控

![](../../image/20190924103858939.png)

11、解决中文乱码无法显示的问题

![](../../image/2019092410410690.png)

![](format,png)

从我们电脑win7里面找到黑体右键复制到桌面然后拉到zabbix服务器上面

直接修改字体名字

切换到这个目录下面: /usr/share/zabbix/fonts

![](format,png)

现在的中文字体是显示正常的了

![](../../image/20190924104635322.png)