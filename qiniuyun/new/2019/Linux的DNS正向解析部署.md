---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-03-05 19:20:34
description: 前面介绍了的作用及其相关的结果。服务之介绍下面开始有关的服务部署。正向解析示例工具：虚拟机配置：要求：准备工作：可以看前期教程关闭，防火墙配置源容易犯错的地方：查看确保你的是否正确正向解析安装软件编辑。。。。。。。
image: http://image.ownit.top/4kdongman/42.jpg
tags:
- linux
title: Linux的DNS正向解析部署
---

<!--more-->

前面介绍了DNS的作用及其相关的结果。[Linux服务之DNS介绍](https://blog.csdn.net/heian_99/article/details/88195866)

下面开始有关DNS的服务部署。\<DNS正向解析示例>

工具：虚拟机

          centos7 

配置：Linux   IP 192.168.196.132

                      DSN   192.168.196.132

要求：

          web.wei.com      192.168.1.1  
          ftp.wei.com      192.168.1.2      
          mail.wei.com     192.168.1.3  
         

准备工作：（可以看前期教程）  
     关闭SElinux，防火墙  
     配置yum源

# 容易犯错的地方：查看/etc/resolv.conf 确保你的DNS是否正确

# ![](http://image.ownit.top/csdn/20190305192006505.png)

 

# DNS正向解析

（1）安装软件 bind  bind-chroot

```
[root@wei csdn]# yum install -y bind bind-chroot
```

2.编辑DNS的主配置文件，创建区域wei.com

新建named.conf

```
[root@wei named]# vim /var/named/chroot/etc/named.conf 
```

 填写内容

```
options{
   directory “/var/named";
};
zone "wei.com"{
  type master;
  file "wei.com.zone"
}:
```

 ![](http://image.ownit.top/csdn/20190305190515255.png)

 3.复制记录文件的模板，并编辑

模板：/usr/share/doc/bind-9.9.4/sample/var/named/named.localhost

```
[root@wei named]# cd /usr/share/doc/bind-9.9.4/sample/var/named/

[root@wei named]# cp named.localhost /var/named/chroot/var/named/wei.com.zone 	
```

 

```
$TTL 1D
@       IN SOA  wei.com. 123456.qq.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      dns01.wei.com.
dns01   A       192.168.196.132
web     A       192.168.1.1
ftp     A       192.168.1.2
        MX  10  mail.wei.com.
mail    A       192.168.1.3
```

 

 

![](http://image.ownit.top/csdn/20190305190809177.png)

 

4.启动named服务

```
[root@wei named]# systemctl start named-chroot

[root@wei named]# systemctl start named
```

开机自启

```
[root@wei named]# systemctl enable named-chroot

[root@wei named]# systemctl enable named
```

查看端口53

![](http://image.ownit.top/csdn/20190305191001671.png)

 

5.测试

（1）nslookup

![](http://image.ownit.top/csdn/20190305191444361.png)

  
（2）dig

\[root\@wei named\]# dig \-t A web.wei.com

![](http://image.ownit.top/csdn/20190305191749596.png)