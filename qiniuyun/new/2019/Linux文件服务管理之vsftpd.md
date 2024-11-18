---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-02-03 21:07:37
description: 简介是的缩写，是一个完全免费，开源的服务器软件。特点小巧轻快，安全易用，支持虚拟用户、支持带宽限制等功能。文件传输协议协议的连接模式：主动连接被动连接软件：配置文件：服务：端口：命令连接端口数据连接端。。。。。。。
image: http://image.ownit.top/4kdongman/75.jpg
tags:
- linux
title: Linux文件服务管理之vsftpd
---

<!--more-->

简介

vsftpd是 “very secure FTP deamon”的缩写，是一个完全免费，开源的[ftp服务器](https://www.baidu.com/s?wd=ftp%E6%9C%8D%E5%8A%A1%E5%99%A8&tn=24004469_oem_dg&rsv_dl=gh_pl_sl_csd)软件。

 

特点

小巧轻快，安全易用，支持虚拟用户、支持带宽限制等功能。

FTP    \------------File Transfer Protocol  文件传输协议

FTP协议的连接模式：  
         主动连接  
         被动连接  
           
软件：vsftpd  
配置文件：/etc/vsftpd/vsftpd.conf  
服务：vsftpd  
端口：21/tcp  命令连接端口  
      20/tcp  数据连接端口（主动）  
        
FTP根目录：  
      用户宿主目录  
      
访问方式：  
     匿名用户访问（ftp）  
     用户认证的访问  
       
示例：搭建匿名访问的FTP服务器

（1）安装vsftpd软件

```
[root@wei csdn]# yum install -y vsftpd
```

  
（2）开启服务，开机自启

```
[root@wei ftp]# systemctl start vsftpd
[root@wei ftp]# systemctl enable vsftpd
```

已经成功，默认的共享目录是/var/ftp/pub路径

![](http://image.ownit.top/csdn/20190203205019511.png)  
示例：允许匿名用户上传文件

```
[root@wei ~]# chmod o+w /var/ftp/pub/

[root@wei ~]# vim /etc/vsftpd/vsftpd.conf 
```

  
anon\_upload\_enable=YES             >>>>允许上传文件  
anon\_mkdir\_write\_enable=YES        >>>>允许上传目录

  
anon\_umask=022                    >>>>允许其他用户能下载匿名用户文件

anon\_other\_write\_enable=YES        >>>>允许修改文件名称，删除文件

anon\_root=/comapng                        >>>>共享目录修改

![](http://image.ownit.top/csdn/20190203205353620.png)

## **注意：圈住的是匿名用户访问时的权限，可根据上面代码修改权限**

重启vsftpd软件

```
[root@wei ~]# systemctl restart vsftpd
```

 

  
访问方式：

linux客户端：

```
[root@zhang hei]# lftp 192.168.196.131
lftp 192.168.196.131:~> ls
drwxr-xr-x    5 0        0             111 Oct 30 19:45 pub
```

 

windows客户端：

           [ftp://192.168.196.131](ftp://192.168.196.131/)

![](http://image.ownit.top/csdn/20190203205631866.png)

 

 

# **本地用户认证的FTP服务**

在普通用户家目录创建文件，可以访问这些文件

示例：

创建文件

```
[root@wei ~]# ls /home/hei/
[root@wei ~]# touch /home/hei/{1..4}.txt
```

  
访问方式：

linux客户端：

```
[root@zhang hei]# lftp 192.168.196.131 -u hei

```

![](http://image.ownit.top/csdn/20190203210354197.png)

windows客户端：

           [ftp://192.168.196.131](ftp://192.168.196.131/)

![](http://image.ownit.top/csdn/20190203210540434.png)

![](http://image.ownit.top/csdn/20190203210637446.png)

![](http://image.ownit.top/csdn/20190203210652617.png)

 

由此可见，可以访问用户家目录下的文件。