---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-29 23:43:33
description: 环境：工具：，，目的：熟练掌握服务器搭建和个服务器之间的配合。有兴趣的朋友可以来实践一下，我会提供各种源码进行搭建。网络家园和论坛源码：准备一台服务器，我是在虚拟机搭建的关闭防火墙和等关闭防火墙和搭建。。。。。。。
image: http://image.ownit.top/4kdongman/77.jpg
tags:
- 技术记录
title: Centos7服务器搭建网络家园和论坛
---

<!--more-->

**环境：Centos7**

**工具：mysql，php，httpd**

**目的：熟练掌握httpd服务器搭建和个服务器之间的配合。**

**有兴趣的朋友可以来实践一下，我会提供各种源码进行搭建。**

**网络家园和论坛****源码：**<https://www.lanzous.com/i3yqq3c>

![](http://image.ownit.top/csdn/20190429234212223.png)

![](http://image.ownit.top/csdn/20190429233953663.png)

**（1）准备一台centos服务器，我是在虚拟机搭建的centos7.**

**（2）关闭防火墙和selinux等（[centos7关闭防火墙和selinux](https://blog.csdn.net/heian_99/article/details/85624511)）**

**（3）搭建myql数据库（[MySQL的rpm安装教程](https://blog.csdn.net/heian_99/article/details/89326404)）**

**（4）搭建httpd服务器（centos7自带httpd，只需要启动即可用）**

**![](http://image.ownit.top/csdn/20190429225305121.png)**

**（5）安装PHP服务器**

 1.     **安装**

```
[root@wei ~]#  yum install php –y
```

**安装php-mysql**

```
[root@wei ~]# yum install php-mysql –y
```

**2.测试php和apache协同**

**测试协同**

```
[root@localhost ~]# cd /var/www/html/
```

```
[root@localhost html]# vim phpinfo.php



<?php

  phpinfo();

?>
```

**              测试： <http://IP/phpinfo.php>**

**![](http://image.ownit.top/csdn/20190429230546718.png)**

 1.     测试php和MySQL协同

```
[root@localhost html]# vim php_mysql.php

<?php
$servername = "localhost";
$username = "admin";
$password = "123456";

// 创建连接
//$con = mysql_connect($servername,$username,$password);
$conn = new mysqli($servername, $username, $password);

// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}
echo "连接成功";
?>
```

**           测试： [http://IP/php\_mysql.php](http://IP/phpinfo.php)**

![](http://image.ownit.top/csdn/20190429231114300.png)

**（6）部署应用**

**1.上传代码（代码在上面）（代码上传到/var/www/html/目录）**

![](http://image.ownit.top/csdn/20190429231400136.png)

 

2.解压

安装解压软件：

```
[root@localhost html]# yum install unzip –y
```

3.配置

改名：

```
[root@wei html]# mv upload/ farm
```

![](http://image.ownit.top/csdn/2019042923185067.png)

 

# 在线安装：

[http://192.168.196.131/farm/install/index.php](http://192.168.217.131/farm/install/index.php)

1.问题一

![](http://image.ownit.top/csdn/20190429231932442.png)

修改/etc/php.ini， 将short\_open\_tag = On

```
vim /etc/php.ini
```

![](http://image.ownit.top/csdn/20190429232102396.png)

修改完毕，重启httpd服务。

```
[root@wei html]# systemctl restart httpd
```

2.问题二

![](http://image.ownit.top/csdn/20190429232256597.png)

修改目录权限：

```
[root@localhost html]# chmod -R 777 farm
```

 

让后进项下面步骤，进行在线安装

步骤一：

![](http://image.ownit.top/csdn/20190429232647400.png)

步骤二：

创建farm数据库和用户

```
[root@wei html]# mysql -u root -proot ##登录数据库
Warning: Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 6
Server version: 5.6.44 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> create database farm;   ##创建farm数据库
Query OK, 1 row affected (0.00 sec)

mysql> grant all on farm.* to farm@'localhost' identified by 'farm';  #创建用户，进行授权
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;  ##刷新权限表
Query OK, 0 rows affected (0.00 sec)

```

![](http://image.ownit.top/csdn/20190429233500759.png)

步骤三：

进行安装

![](http://image.ownit.top/csdn/20190429233551411.png)

![](http://image.ownit.top/csdn/20190429233605856.png)

 

![](http://image.ownit.top/csdn/20190429233635619.png)

步骤四：

进行测试

<http://192.168.196.131/farm/bbs/>

![](http://image.ownit.top/csdn/20190429233730909.png)

 

<http://192.168.196.131/farm/>

![](http://image.ownit.top/csdn/20190429233805515.png)

<http://192.168.196.131/farm/home/space.php?do=home>

![](http://image.ownit.top/csdn/20190429234306190.png)