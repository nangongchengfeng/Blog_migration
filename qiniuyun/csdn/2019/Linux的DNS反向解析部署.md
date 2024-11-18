---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-03-05 21:19:25
description: 下面的部署是在的正向解析示例上进行修改的。如果有什么问题或者错误，可以访问上篇帖子下面开始有关的服务部署。反向解析工具：虚拟机配置：建立反向区域，实现反向解析编辑主配置文件添加下面的代码建立反向区域可。。。。。。。
image: ../../title_pic/69.jpg
slug: '201903052119'
tags:
- linux
title: Linux的DNS反向解析部署
---

<!--more-->

下面的部署是在[Linux的DNS正向解析示例](https://blog.csdn.net/heian_99/article/details/88196569)上进行修改的。

如果有什么问题或者错误，可以访问上篇帖子

下面开始有关DNS的服务部署。\<DNS反向解析>

工具：虚拟机

          centos7 

配置：Linux   IP 192.168.196.132

                      DSN   192.168.196.132

 

建立DAS反向区域，实现反向解析

（1）编辑主配置文件named.conf

```
[root@wei named]# vim /var/named/chroot/etc/named.conf 
```

  
添加下面的代码

```
zone "1.168.192.in-addr.arpa" {
      type master;
      file "192.168.1.zone";  
};  
```

![](../../image/20190305211607230.png)

（2）建立反向区域

可以复制正向解析的文件作为模板

```
[root@wei named]# cp /var/named/chroot/var/named/wei.com.zone /var/named/chroot/var/named/192.168.1.zone
```

修改192.168.1.zone脚本

```
[root@wei named]# vim /var/named/chroot/var/named/192.168.1.zone
```

```
$TTL 1D
@       IN SOA  wei.com. 123456.qq.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      dns01.wei.com.
dns01   A       192.168.196.132
1       PTR     web.wei.com.
11      PTR     web.wei.com.
2       PTR     ftp.wei.com.
3       PTR     mail.wei.com.
```

（3）重启服务  
 

```
[root@wei named]# systemctl restart named-chroot

[root@wei named]# systemctl restart named
```

（4）使用nslookup测试查看

![](../../image/20190305211902801.png)