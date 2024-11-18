---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-26 17:04:22
description: 前面介绍了软件的管理的方式。但有个缺点，不能解决依赖。下面介绍的软件管理。可以完美的解决这个问题。使用的方式管理软件优势：自动解决软件的依赖关系前提条件：配置仓库源源类型：本地源源源配置的地方：阿里云。。。。。。。
image: ../../title_pic/54.jpg
slug: '201901261704'
tags:
- linux
title: Linux的yum管理
---

<!--more-->

 

**前面介绍了软件的管理的方式rpm。但有个缺点，rpm不能解决依赖。**

**下面介绍的yum软件管理。可以完美的解决这个问题。**

  
**使用yum的方式管理rpm软件  
     
    优势：自动解决软件的依赖关系  
      
前提条件：配置yum仓库/yum源**

# **yum源类型：**

## **     1.本地yum源  
     2.ftp源  
     3.http源  
     **

###   
**    配置yum的地方：**

  
**        阿里云镜像：     https://mirrors.aliyun.com  
          
        网易云镜像：     http://mirrors.163.com/  
          
        epel源          Centos官网 ：http://vault.centos.org         # yum install epel-release   安装epel源  
        **

**yum源/yum仓库的配置文件  
   
     /etc/yum.repos.d/\*.repo  
       
       
示例：配置本地yum源**

```
[root@wei yum.repos.d]# mount /dev/sr0 /mnt/
mount: /dev/sr0 写保护，将以只读方式挂载
[root@wei yum.repos.d]# ls /mnt/
CentOS_BuildTag  EULA  images    LiveOS    repodata              RPM-GPG-KEY-CentOS-Testing-7
EFI              GPL   isolinux  Packages  RPM-GPG-KEY-CentOS-7  TRANS.TBL
[root@wei yum.repos.d]# mkdir /etc/yum.repos.d/beifeng
[root@wei yum.repos.d]# mv /etc/yum.repos.d/CentOS-* /etc/yum.repos.d/beifeng/
[root@wei yum.repos.d]# ls
beifeng  mysql-community.repo  mysql-community-source.repo
[root@wei yum.repos.d]# vim centos.repo
[root@wei yum.repos.d]# ls
beifeng  centos.repo  mysql-community.repo  mysql-community-source.repo

配置内容：
[centos7.2]
name=centos7.2
baseurl=file:///mnt
enable=1
gpgcheck=0
```

  
**清除yum缓存：**

```
[root@wei yum.repos.d]# yum clean all
```

  
**生成yum缓存：**

```
[root@wei yum.repos.d]# yum makecache
```

**查看yum的列表**

```
[root@wei yum.repos.d]# yum repolist
```

#   
**yum常规操作**

## **（1）yum安装软件**

 

**\# yum install 软件名**

 

**\# yum install \-y 软件名**

 

**（2）显示yum中所有软件**

```
[root@wei ~]# yum list all
```

 

**（3）显示所有的软件组**

```
[root@wei ~]# yum grouplist
```

**（4）安装软件组**

**\# yum groupinstall \-y 软件组的名称**

**\(英文组，要用“”括起来\)**

**（5）查询文件所属的软件名称**

**\# yum provides “\*bin/passwd”**

 

# **源码软件管理安装**

## **    1.配置安装参数  
    2.编译  
    3.安装**

 

**前提：gcc编译环境（自己安装yum install gcc）**

**示例：编译安装htop软件**

**htop软件源码：**<https://www.lanzous.com/i2zs97g>

  
**解压  
\[root\@wei \~\]# tar zxf htop-1.0.2.tar.gz **

**切入htop-1.0.2目录**

**\[root\@wei \~\]#cd htop-1.0.2**

**查看配置**

**\[root\@wei htop-1.0.2\]# ./configure \--help |less**

**配置参数**

**\[root\@wei htop-1.0.2\]# ./configure \--prefix=/usr/local/htop**

**编译**

**\[root\@wei htop-1.0.2\]# make**

**安装**

**\[root\@wei htop-1.0.2\]# make install**

**启动（已经安装成功接界面）**

**\[root\@wei share\]# /usr/local/htop/bin/htop **

![](../../image/20190126170137238.png)

  
**出现错误：**

**configure: error: You may want to use \--disable-unicode or install libncursesw.**

**解决办法：  
\[root\@wei htop-1.0.2\]# yum install \-y ncurses-devel **