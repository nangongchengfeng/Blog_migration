+++
author = "南宫乘风"
title = "MySQL的rpm安装教程"
date = "2019-04-16 09:47:25"
tags=[]
categories=['MySQL']
image = "post/4kdongman/57.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89326404](https://blog.csdn.net/heian_99/article/details/89326404)

## Linux 上安装 MySQL

Linux平台上推荐使用RPM包来安装Mysql,MySQL AB提供了以下RPM包的下载地址：
- **MySQL** - MySQL服务器。你需要该选项，除非你只想连接运行在另一台机器上的MySQL服务器。- **MySQL-client** - MySQL 客户端程序，用于连接并操作Mysql服务器。- **MySQL-devel** - 库和包含文件，如果你想要编译其它MySQL客户端，例如Perl模块，则需要安装该RPM包。- **MySQL-shared** - 该软件包包含某些语言和应用程序需要动态装载的共享库(libmysqlclient.so*)，使用MySQL。- **MySQL-bench** - MySQL数据库服务器的基准和性能测试工具。
安装前，我们可以检测系统是否自带安装 MySQL:

```
rpm -qa | grep mysql
```

如果你系统有安装，那可以选择进行卸载:

```
rpm -e mysql　　// 普通删除模式
rpm -e --nodeps mysql　　// 强力删除模式，如果使用上面命令删除时，提示有依赖的其它文件，则用该命令可以对其进行强力删除
```

接下来我们在 Centos7 系统下使用 yum 命令安装 MySQL，需要注意的是 CentOS 7 版本中 MySQL数据库已从默认的程序列表中移除，所以在安装前我们需要先去官网下载 Yum 资源包，下载地址为：[https://dev.mysql.com/downloads/repo/yum/](https://dev.mysql.com/downloads/repo/yum/)

注意：没安装wget的朋友，需要先安装wget

```
[root@wei ~]# yum install wget

```

### 下载安装包

```
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
```

### 安装rpm包

```
rpm -ivh mysql-community-release-el7-5.noarch.rpm
```

### 安装mysql-server服务

```
yum install mysql-server
```

 

### 权限设置：

```
chown mysql:mysql -R /var/lib/mysql
```

### 初始化 MySQL：

```
mysqld --initialize
```

### 启动 MySQL：

```
systemctl start mysqld
```

### 查看 MySQL 运行状态：

```
systemctl status mysqld
```

### 设置为开机自启

```
systemctl enable mysqld

```

## 验证 MySQL 安装

```
[root@wei ~]# mysqladmin --version
mysqladmin  Ver 8.42 Distrib 5.6.42, for Linux on x86_64 ##显示这个信息表示成功
```

#  注意：

**设置密码 <br> 当第一次启动MySQL服务器时，为MySQL根用户生成一个临时密码。 您可以通过运行以下命令找到密码：**

```
[root@wei ~]# grep  'temporary password' /var/log/mysqld.log

```

<img alt="" class="has" height="124" src="https://img-blog.csdnimg.cn/20190416092547812.jpg" width="750">

**localhost：后边的就是临时密码，先复制下来 **

**注意：如果没有查到，就是不需要，登陆时，回车即可登陆**

**进入mysql，在Enter password：复制粘贴先前的密码就进去了**

```
mysql -u root -p

```

![20190416092811232.png](https://img-blog.csdnimg.cn/20190416092811232.png)

# **修改密码方式**

```
[root@wei ~]# mysqladmin -u root -p password
Enter password:        #旧密码
New password:         #新密码
Confirm new password:    #再输入一次

```

# **注意：**在输入密码时，密码是不会显示了，你正确输入即可。

 
