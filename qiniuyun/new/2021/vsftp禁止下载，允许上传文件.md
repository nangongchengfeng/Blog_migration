---
author: 南宫乘风
categories:
- Linux实战操作
date: 2021-08-10 21:58:25
description: 问题需求公司有台业务服务器，上面有多个用户，但是这台机器无法使用，，和等传输工具因为安全问题，不能对外公开传输数据渠道但是，这些功能禁用后，怎么往上面传输文件，偶尔有些用户需要往上面传程序，这个就是很。。。。。。。
image: http://image.ownit.top/4kdongman/14.jpg
tags:
- 技术记录
title: vsftp禁止下载，允许上传文件
---

<!--more-->

## 问题需求

公司有台业务服务器，上面有多个用户，但是这台机器无法使用scp ，sftp ，和ftp等传输工具（因为安全问题，不能对外公开传输数据渠道）

但是，这些功能禁用后，怎么往上面传输文件，偶尔有些用户需要往上面传程序，这个就是很头疼的问题。

## 解决方案：

采用vsftp工具，构建本机用户登录，使用白名单，对特定用户使用，运行上传，不能下载

## 实现方法：

环境是纯内网：首先找vsftp安装包

```
yum install yum-utils -y
#下载rpm包的工具
yumdownloader vsftpd --resolve --destdir=/root/rpm
#使用这个下载vsftp包和依赖
```

下载完成，上传服务器直接安装

```bash
rpm -ivh vsftpd-3.0.2-29.el7_9.x86_64.rpm
```

```bash
主配置文件：/etc/vsftpd/vsftpd.conf
配置文件目录：/etc/vsftpd/*.conf
服务启动脚本：/etc/rc.d/init.d/vsftpd
用户认证配置文件：/etc/pam.d/vsftpd
```

**配置参数**

常用配置参数都为主配置文件，/etc/vsftpd/vsftpd.conf 的常用配置。

**通用基础配置**

```
listen=[YES|NO]         #是否以独立运行的方式监听服务
listen_address=IP地址   #设置要监听的 IP 地址
listen_port=21        #设置 FTP 服务的监听端口
download_enable＝[YES|NO] #是否允许下载文件
max_clients=0   #最大客户端连接数，0 为不限制
max_per_ip=0   #同一 IP 地址的最大连接数，0 为不限制
chown_uploads=[YES|NO] #是否允许改变上传文件的属主
chown_username=whoever #改变上传文件的属主为 whoever
pam_service_name=vsftpd #让 vsftpd 使用 pam 完成用户认证，使用的文件为/etc/pam.d/vsftpd
```

**系统用户的配置**

```
anonymous_enable=NO    #禁止匿名访问模式
local_enable=[YES|NO]  #是否允许本地用户登录 FTP
write_enable=[YES|NO]  #是否开放本地用户的其他写入权限
local_umask=022        #本地用户上传文件的 umask 值
local_root=/var/ftp    #本地用户的 FTP 根目录
local_max_rate=0      #本地用户最大传输速率（字节/秒），0 为不限制
userlist_enable=[YES|NO] #开启用户作用名单文件功能
userlist_deny=[YES|NO]   #启用禁止用户名单，名单文件为 ftpusers 和/etc/vsftpd/user_list
chroot_local_user=[YES|NO] #是否将用户权限禁锢在 FTP 家目录中，以确保安全
chroot_list_enable=[YES|NO] #禁锢文件中指定的 FTP 本地用户于其家目录中
chroot_list_file=/etc/vsftpd/chroot_list #指定禁锢文件位置，需要和 chroot_list_enable 一同
```

## vsftp配置

我这边为了实现对应功能，配置如下

```bash
anonymous_enable=NO #禁止匿名用户登录
local_enable=YES #本地用户
write_enable=YES
download_enable=NO
local_umask=022
chroot_list_enable=YES
chroot_local_user=yes #固定传输文件在家目录
allow_writeable_chroot=YES
userlist_enable=YES
userlist_deny=NO
userlist_file=/etc/vsftpd/user_list #登录白名单
dirmessage_enable=YES
connect_from_port_20=YES
listen=NO
listen_ipv6=YES
pam_service_name=vsftpd
userlist_enable=YES
tcp_wrappers=YES
xferlog_enable=YES
xferlog_std_format=YES
```

 /etc/vsftpd/user\_list 这个文件里面写入允许登录的用户即可

（1）允许特定用户登录

（2）允许上传，禁止下载

（3）禁止跳转目录，只允许自己家目录

![](http://image.ownit.top/csdn/20210810215742972.png)

 参考地址：

<https://zhuanlan.zhihu.com/p/354583347>

<https://blog.csdn.net/weixin_30514745/article/details/98155033>

<https://www.huaweicloud.com/articles/2cc1b07fa2841e3874e7b4f430b038af.html>