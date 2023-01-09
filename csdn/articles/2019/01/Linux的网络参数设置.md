+++
author = "南宫乘风"
title = "Linux的网络参数设置"
date = "2019-01-28 16:08:55"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/96.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86678634](https://blog.csdn.net/heian_99/article/details/86678634)

<br>**前面讲解了lLinux 的IP组成，下面就讲一下Linux的网络设置和数据传递。**

**其实这地方对运维的人员来说，不会要精通，但还是要了解。必要时刻还会用到的**

 

**电脑之间数据的传递：**

**数据的传递要分为下面几层。**

**OSI七层模型<br>      <br>     应用层  表示层  会话层  传输层  网络层  数据链路层  物理层<br>     <br> 数据封装过程：<br>                                                 <br>     MAC帧头+IP报头+TCP/UDP报头+数据<br>     <br>             TCP/UDP报头:<br>                 <br>                 端口号  Port  区分不同的应用程序<br>                 取值范围：1---65535  基于ip地址**<br>  

**数据解包，则反之。            **

 

<br>**centos 7 提供network ，NetworkManager服务实现网络参数**

**基于network服务**

**1.查看操作**

**（1）查看网卡IP地址**

**# ifconfig**

**# ip addr show**

![20190128160215859.png](https://img-blog.csdnimg.cn/20190128160215859.png)

**（2）查看网关**

**#  route -n **

**# ip route**

![20190128160308293.png](https://img-blog.csdnimg.cn/20190128160308293.png)

**（3）查看DNS服务地址**

**# cat /etc/resolv.conf**

```
[root@wei ~]# cat /etc/resolv.conf
```

![20190128160340332.png](https://img-blog.csdnimg.cn/20190128160340332.png)

 

**修改网卡TCP/IP参数**

**配置文件地方 /etc/sysconfig/network-scripts/ifcfg-ens33 **

<br>**内容:<br> DEVICE=网卡名称<br> NANE=网卡配置文件名称<br> ONBOOT=yes                //设置开机自动启动网卡<br> BOOTPROTO=none           //手动指定IP<br> IPADDR=192.168.196.131   //IP地址 <br> NETMASK=255.255.255.0    //子网掩码  或者PREFIX=24<br> GATEWAY=192.168.196.2    //网关<br> DNS1=8.8.8.8             //dns服务地址<br> DNS2=8.8.4.4**

**示例：**

**   为eth0网卡配置多个IP地址   10.1.1.1/24<br>    <br> 临时生效：**

**[root@wei ~]# ifconfig ens33:0 10.1.1.1/24**

**[root@wei ~]# ip addr dev ens33 10.1.1.1/24**

**永久生效：**

**[root@wei ~]# vim /etc/sysconfig/network-scripts/ifcfg-ens33:0**

<br>**DEVICE=en33s:0<br> NANE=ens33:0<br> ONBOOT=yes                <br> BOOTPROTO=none           <br> IPADDR=192.168.196.131   <br> NETMASK=255.255.255.0   **

<br>**[root@wei ~]# systemctl restart NetworkManager<br> [root@wei ~]# systemctl restart network**

**临时禁用网卡**

**# ifdown 网卡名称**

**启用网卡**

**# if 网卡名称**

<br>**端口号（port）：**

**（1）查看TCP端口**

**[root@wei csdn]# ss -antp**

**        a: all  全部<br>         n：number  数据<br>         p：port   端口号：<br>         t：tcp    协议<br>         <br> [root@wei csdn]# netstat -antp**

![20190128160543333.png](https://img-blog.csdnimg.cn/20190128160543333.png)<br>**（2）查看UDP端口**

**[root@wei csdn]# ss -anup**

**[root@wei csdn]# netstat -anup**

![20190128160640176.png](https://img-blog.csdnimg.cn/20190128160640176.png)

<br>**（3）查看所有的UDP和TCP的端口**

<br>**[root@wei csdn]# netstat -anutp<br>         <br> [root@wei csdn]# ss -anutp**

![2019012816075689.png](https://img-blog.csdnimg.cn/2019012816075689.png)

**            **
