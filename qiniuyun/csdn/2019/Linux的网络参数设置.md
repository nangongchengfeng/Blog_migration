---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-28 16:08:55
description: 前面讲解了的组成，下面就讲一下的网络设置和数据传递。其实这地方对运维的人员来说，不会要精通，但还是要了解。必要时刻还会用到的电脑之间数据的传递：数据的传递要分为下面几层。七层模型应用层表示层会话层传输。。。。。。。
image: ../../title_pic/20.jpg
slug: '201901281608'
tags:
- linux
title: Linux的网络参数设置
---

<!--more-->

  
**前面讲解了lLinux 的IP组成，下面就讲一下Linux的网络设置和数据传递。**

**其实这地方对运维的人员来说，不会要精通，但还是要了解。必要时刻还会用到的**

 

**电脑之间数据的传递：**

**数据的传递要分为下面几层。**

**OSI七层模型  
       
    应用层  表示层  会话层  传输层  网络层  数据链路层  物理层  
      
数据封装过程：  
                                                  
    MAC帧头+IP报头+TCP/UDP报头+数据  
      
            TCP/UDP报头:  
                  
                端口号  Port  区分不同的应用程序  
                取值范围：1---65535  基于ip地址**  
 

**数据解包，则反之。            **

 

  
**centos 7 提供network ，NetworkManager服务实现网络参数**

**基于network服务**

**1.查看操作**

**（1）查看网卡IP地址**

**\# ifconfig**

**\# ip addr show**

![](../../image/20190128160215859.png)

**（2）查看网关**

**\#  route \-n **

**\# ip route**

![](../../image/20190128160308293.png)

**（3）查看DNS服务地址**

**\# cat /etc/resolv.conf**

```
[root@wei ~]# cat /etc/resolv.conf
```

![](../../image/20190128160340332.png)

 

**修改网卡TCP/IP参数**

**配置文件地方 /etc/sysconfig/network-scripts/ifcfg-ens33 **

  
**内容:  
DEVICE=网卡名称  
NANE=网卡配置文件名称  
ONBOOT=yes                //设置开机自动启动网卡  
BOOTPROTO=none           //手动指定IP  
IPADDR=192.168.196.131   //IP地址   
NETMASK=255.255.255.0    //子网掩码  或者PREFIX=24  
GATEWAY=192.168.196.2    //网关  
DNS1=8.8.8.8             //dns服务地址  
DNS2=8.8.4.4**

**示例：**

**   为eth0网卡配置多个IP地址   10.1.1.1/24  
     
临时生效：**

**\[root\@wei \~\]# ifconfig ens33:0 10.1.1.1/24**

**\[root\@wei \~\]# ip addr dev ens33 10.1.1.1/24**

**永久生效：**

**\[root\@wei \~\]# vim /etc/sysconfig/network-scripts/ifcfg-ens33:0**

  
**DEVICE=en33s:0  
NANE=ens33:0  
ONBOOT=yes                  
BOOTPROTO=none             
IPADDR=192.168.196.131     
NETMASK=255.255.255.0   **

  
**\[root\@wei \~\]# systemctl restart NetworkManager  
\[root\@wei \~\]# systemctl restart network**

**临时禁用网卡**

**\# ifdown 网卡名称**

**启用网卡**

**\# if 网卡名称**

  
**端口号（port）：**

**（1）查看TCP端口**

**\[root\@wei csdn\]# ss \-antp**

**        a: all  全部  
        n：number  数据  
        p：port   端口号：  
        t：tcp    协议  
          
\[root\@wei csdn\]# netstat \-antp**

![](../../image/20190128160543333.png)  
**（2）查看UDP端口**

**\[root\@wei csdn\]# ss \-anup**

**\[root\@wei csdn\]# netstat \-anup**

![](../../image/20190128160640176.png)

  
**（3）查看所有的UDP和TCP的端口**

  
**\[root\@wei csdn\]# netstat \-anutp  
          
\[root\@wei csdn\]# ss \-anutp**

![](../../image/2019012816075689.png)