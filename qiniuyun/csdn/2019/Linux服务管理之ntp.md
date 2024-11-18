---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-02-02 19:50:02
description: 是网络时间协议，它是用来同步网络中各个计算机的时间的协议。在计算机的世界里，时间非常地重要，例如对于火箭发射这种科研活动，对时间的统一性和准确性要求就非常地高，是按照这台计算机的时间，还是按照这台计算。。。。。。。
image: ../../title_pic/12.jpg
slug: '201902021950'
tags:
- linux
title: Linux服务管理之ntp
---

<!--more-->

 

NTP是网络时间协议\(Network Time Protocol\)，它是用来同步网络中各个计算机的时间的协议。

在计算机的世界里，时间非常地重要，例如对于火箭发射这种科研活动，对时间的统一性和准确性要求就非常地高，是按照A这台计算机的时间，还是按照B这台计算机的时间？NTP就是用来解决这个问题的，NTP（Network Time Protocol，网络时间协议）是用来使网络中的各个计算机时间同步的一种协议。它的用途是把计算机的时钟同步到[世界协调时](https://baike.baidu.com/item/%E4%B8%96%E7%95%8C%E5%8D%8F%E8%B0%83%E6%97%B6)UTC，其精度在局域网内可达0.1ms，在互联网上绝大多数的地方其精度可以达到1-50ms。

它可以使计算机对其服务器或时钟源（如石英钟，GPS等等）进行时间同步，它可以提供高精准度的时间校正，而且可以使用加密确认的方式来防止病毒的协议攻击。

NTP服务器

       NTP \----------- Network Time Protocol 网络时间协议  
         
         
       软件：ntp  
       配置文件： /etc/ntp.conf  
       服务：ntp  
       端口：123/udp  
         
示例：配置ntp时间服务器

1.安装ntp软件

```
[root@wei ~]# yum install ntp -y
```

  
2.编辑ntp配置文件

```
[root@wei ~]# vim /etc/ntp.conf
```

添加下面的代码

restrict 192.168.196.0 mask 255.255.255.0 nomodify notrap

         
 server 127.127.1.0 iburst  
 27 fudge 127.127.1.0 stratum 10       

  
   ![](../../image/20190202194217860.png)      
3.重启ntpd服务

```
[root@wei ~]# systemctl start ntpd     #启动服务
[root@wei ~]# systemctl enable ntpd    #设置为开机启动
Created symlink from /etc/systemd/system/multi-user.target.wants/ntpd.service to /usr/lib/systemd/system/ntpd.service.       
```

         
         
         
在客户端输入：  
              
      

```
     [root@zhang csdn]# ntpdate 192.168.196.131
```

![](../../image/20190202194615451.png)

 

即可同步时间

  
同步网络时间：   
              
      

```
      [root@wei ~]# /usr/sbin/ntpdate time.windows.com
```

![](../../image/20190202194954821.png)