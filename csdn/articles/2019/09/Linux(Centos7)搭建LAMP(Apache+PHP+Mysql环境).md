+++
author = "南宫乘风"
title = "Linux(Centos7)搭建LAMP(Apache+PHP+Mysql环境)"
date = "2019-09-23 15:09:01"
tags=[]
categories=[' Linux实战操作']
image = "post/4kdongman/66.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/101203824](https://blog.csdn.net/heian_99/article/details/101203824)

**目录**

 

 

 

[Linux搭建LAMP(Apache+PHP+Mysql环境)Centos7](#Linux%E6%90%AD%E5%BB%BALAMP%28Apache%2BPHP%2BMysql%E7%8E%AF%E5%A2%83%29Centos7)

[一、 检查系统环境](#%E4%B8%80%E3%80%81%20%E6%A3%80%E6%9F%A5%E7%B3%BB%E7%BB%9F%E7%8E%AF%E5%A2%83)

[1、确认centos版本](#1%E3%80%81%E7%A1%AE%E8%AE%A4centos%E7%89%88%E6%9C%AC)

[2、检查是否安装过apache](#2%E3%80%81%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%AE%89%E8%A3%85%E8%BF%87apache)

[3、检查是否安装过Mysql](#3%E3%80%81%E6%A3%80%E6%9F%A5%E6%98%AF%E5%90%A6%E5%AE%89%E8%A3%85%E8%BF%87Mysql)

[4、清理Mysql痕迹](#4%E3%80%81%E6%B8%85%E7%90%86Mysql%E7%97%95%E8%BF%B9)

[5、卸载Apache包](#5%E3%80%81%E5%8D%B8%E8%BD%BDApache%E5%8C%85)

[二、安装Apache、PHP、Mysql](#%E4%BA%8C%E3%80%81%E5%AE%89%E8%A3%85Apache%E3%80%81PHP%E3%80%81Mysql)

[1、安装apache](#1%E3%80%81%E5%AE%89%E8%A3%85apache)

[2、安装Php](#2%E3%80%81%E5%AE%89%E8%A3%85Php)

[3、安装php-fpm](#3%E3%80%81%E5%AE%89%E8%A3%85php-fpm)

[4、安装Mysql](#4%E3%80%81%E5%AE%89%E8%A3%85Mysql)

[5、安装 mysql-server](#5%E3%80%81%E5%AE%89%E8%A3%85%20mysql-server)

[6、安装 php-mysql](#6%E3%80%81%E5%AE%89%E8%A3%85%20php-mysql)

[三、安装基本常用扩展包](#%E4%B8%89%E3%80%81%E5%AE%89%E8%A3%85%E5%9F%BA%E6%9C%AC%E5%B8%B8%E7%94%A8%E6%89%A9%E5%B1%95%E5%8C%85)

[1、安装Apache扩展包](#1%E3%80%81%E5%AE%89%E8%A3%85Apache%E6%89%A9%E5%B1%95%E5%8C%85)

[2、安装PHP扩展包](#2%E3%80%81%E5%AE%89%E8%A3%85PHP%E6%89%A9%E5%B1%95%E5%8C%85)

[3、安装Mysql扩展包](#3%E3%80%81%E5%AE%89%E8%A3%85Mysql%E6%89%A9%E5%B1%95%E5%8C%85)

[四、配置Apache、mysql开机启动](#%E5%9B%9B%E3%80%81%E9%85%8D%E7%BD%AEApache%E3%80%81mysql%E5%BC%80%E6%9C%BA%E5%90%AF%E5%8A%A8)

[五、配置Mysql](#%E4%BA%94%E3%80%81%E9%85%8D%E7%BD%AEMysql)

[六、测试环境](#%E5%85%AD%E3%80%81%E6%B5%8B%E8%AF%95%E7%8E%AF%E5%A2%83)

 

#  

#  

# Linux搭建LAMP(Apache+PHP+Mysql环境)Centos7

 

**LAMP**是指一组通常一起使用来运行动态网站或者服务器的[自由软件](https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E8%BD%AF%E4%BB%B6)名称首字母缩写：
-  [**L**inux](https://baike.baidu.com/item/Linux)，[操作系统](https://baike.baidu.com/item/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F) -  [**A**pache](https://baike.baidu.com/item/Apache)，网页服务器 -  [**M**ariaDB](https://baike.baidu.com/item/MariaDB)或[**M**ySQL](https://baike.baidu.com/item/MySQL)，[数据库管理系统](https://baike.baidu.com/item/%E6%95%B0%E6%8D%AE%E5%BA%93%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F)（或者[数据库服务器](https://baike.baidu.com/item/%E6%95%B0%E6%8D%AE%E5%BA%93%E6%9C%8D%E5%8A%A1%E5%99%A8)） -  [**P**HP](https://baike.baidu.com/item/PHP)、[**P**erl](https://baike.baidu.com/item/Perl)或[**P**ython](https://baike.baidu.com/item/Python)，[脚本语言](https://baike.baidu.com/item/%E8%84%9A%E6%9C%AC%E8%AF%AD%E8%A8%80) 
 

## 一、 检查系统环境

### <br> 1、确认centos版本

```
[root@wei ~]# cat /etc/redhat-release 
CentOS Linux release 7.4.1708 (Core) 
```

![20190923142303573.png](https://img-blog.csdnimg.cn/20190923142303573.png)

### <br> 2、检查是否安装过apache

```

[root@wei ~]# rpm -qa |grep httpd

```

<br> 或者：

apachectl -v<br> 或者：

httpd -v 

### <br> 3、检查是否安装过Mysql

```

[root@wei ~]# rpm -qa | mysql

```

### <br><br> 4、清理Mysql痕迹

```
[root@wei ~]# yum remove mysql
已加载插件：fastestmirror
参数 mysql 没有匹配
不删除任何软件包
[root@wei ~]# rm -rf /etc/my.cnf

```

### <br> 5、卸载Apache包

```
[root@wei ~]# rpm -e httpd --nodeps


```

<br>注意：如果是新的系统或者你从来没有尝试安装过，则以上步骤省略。

 

## 二、安装Apache、PHP、Mysql

### <br> 1、安装apache

```
[root@wei ~]# yum install httpd -y 


```

<br> 直到返回

安装完成

![20190923143215324.png](https://img-blog.csdnimg.cn/20190923143215324.png)<br>  <br> 查看安装httpd

```
[root@wei ~]# rpm -qa |grep httpd
httpd-tools-2.4.6-90.el7.centos.x86_64
httpd-2.4.6-90.el7.centos.x86_64

```

<br> 表示安装成功！

### <br> 2、安装Php

 

[root@localhost ~]# yum -y install php<br> 直到返回：

![20190923143401301.png](https://img-blog.csdnimg.cn/20190923143401301.png)<br>  <br> 查看安装php的软件

```
[root@wei ~]# rpm -qa |grep php
php-common-5.4.16-46.el7.x86_64
php-5.4.16-46.el7.x86_64
php-cli-5.4.16-46.el7.x86_64

```

### <br> 3、安装php-fpm

```
[root@wei ~]# yum -y install php-fpm
```

<br> 直到返回：

![20190923143517305.png](https://img-blog.csdnimg.cn/20190923143517305.png)

### 4、安装Mysql

```
[root@wei ~]# yum -y install mysql

```

<br> 直到返回：

>  
 ![20190923143654589.png](https://img-blog.csdnimg.cn/20190923143654589.png)                               <br>  <br>Complete!<br> 7.2版本的Centos已经把mysql更名为mariadb，表示安装成功！ 


### 5、安装 mysql-server

```
[root@wei ~]# yum -y install mysql-server
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirrors.aliyun.com
 * extras: mirrors.aliyun.com
 * updates: mirrors.tuna.tsinghua.edu.cn
没有可用软件包 mysql-server。
错误：无须任何处理

```

<br>返回错误！！！<br>分析解决方案

 

>  
 - CentOS 7+ 版本将MySQL数据库软件从默认的程序列表中移除，用mariadb代替了，entos7配置教程上，大多都是安装mariadb，因为centos7默认将mariadb视作mysql。- 因为mysql被oracle收购后，原作者担心mysql闭源，所以又写了一个mariadb，这个数据库可以理解为mysql的分支。如果需要安装mariadb，只需通过yum就可。


有两种解决方案：

>  
 一是安装mariadb 
 [root@localhost ~]# yum install -y mariadb  
   
 二是从官网下载mysql-server 


**采用第二种方案：**

```
[root@wei ~]# wget http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
```

```
[root@wei ~]# rpm -ivh mysql-community-release-el7-5.noarch.rpm 

```

```
[root@wei ~]# yum -y install wget
```

**下载中.......**

![20190923144254472.png](https://img-blog.csdnimg.cn/20190923144254472.png)<br><br>**安装成功！！！**

![20190923144604448.png](https://img-blog.csdnimg.cn/20190923144604448.png)

### <br> 6、安装 php-mysql

```
[root@wei ~]# yum -y install php-mysql

```

<br> 直到返回：

![2019092314464018.png](https://img-blog.csdnimg.cn/2019092314464018.png)<br> 安装成功！！！

## 三、安装基本常用扩展包

### <br> 1、安装Apache扩展包

```
[root@wei ~]# yum -y install httpd-manual mod_ssl mod_perl mod_auth_mysql 

```

![20190923144740866.png](https://img-blog.csdnimg.cn/20190923144740866.png)<br> 安装成功！！！

### <br> 2、安装PHP扩展包

```
[root@wei ~]# yum -y install php-gd php-xml php-mbstring php-ldap php-pear php-xmlrpc php-devel

```

![20190923144817774.png](https://img-blog.csdnimg.cn/20190923144817774.png)<br> 安装成功！！！

### 3、安装Mysql扩展包

```
[root@wei ~]# yum -y install mysql-connector-odbc mysql-devel libdbi-dbd-mysql

```

![20190923144847427.png](https://img-blog.csdnimg.cn/20190923144847427.png)<br> 安装成功！！！

## 四、配置Apache、mysql开机启动

<br> 重启Apache、mysql服务(注意这里和centos6有区别,Cenots7+不能使用6的方式)

systemctl start httpd.service #启动apache<br> systemctl stop httpd.service #停止apache<br> systemctl restart httpd.service #重启apache<br> systemctl enable httpd.service #设置apache开机启动<br> 如果是采用方法一安装的mariadb,安装完成以后使用下面的命令开启数据库服务：

#启动MariaDB

```
[root@wei~]# systemctl start mariadb.service   
```

#停止MariaDB

```
[root@wei~]# systemctl stop mariadb.service   
```

#重启MariaDB

```
[root@wei~]# systemctl restart mariadb.service  
```

#设置开机启动

 

```
[root@wei~]# systemctl enable mariadb.service  
```

<br> 重启对应服务

service mysqld restart<br>  <br> service php-fpm start<br>  <br> service httpd restart

## <br> 五、配置Mysql

**注意：要启动mysql才能进去**<br> 初次安装mysql是没有密码的,我们要设置密码，mysql的默认账户为root

设置 MySQL 数据 root 账户的密码：

```
[root@wei etc]# mysql -u root -p

```

![20190923145806809.png](https://img-blog.csdnimg.cn/20190923145806809.png)

## 六、测试环境

**注意：要启动httpd才能进去**

![20190923150046879.png](https://img-blog.csdnimg.cn/20190923150046879.png)<br>**1、我们在浏览器地址栏输入http://localhost/如下图，说明我们的apache测试成功**

![20190923150114452.png](https://img-blog.csdnimg.cn/20190923150114452.png)

**2、测试PHP**

<br> 进入apache的web根目录：/var/www/html 中写一个最简单的php测试页面

```
[root@wei ~]# cd /var/www/html/
[root@wei html]# vi phpinfo.php

```

<br>  <br> 3、进入到了控制模式之后按键盘字母 i 进入到编辑模式，将如下代码输入到文件中

```
&lt;?php
echo "&lt;title&gt;Phpinfo Test.php&lt;/title&gt;";
phpinfo()
?&gt;
```

<br> 按 esc 退出编辑模式，回到控制模式，输入 :wq 然后回车，

重启apache服务器

```
[root@wei html]# systemctl restart httpd

```

在浏览器中输入服地址http://localhost/phpinfo.php

出现下图则成功。

![2019092315073758.png](https://img-blog.csdnimg.cn/2019092315073758.png)

##  
