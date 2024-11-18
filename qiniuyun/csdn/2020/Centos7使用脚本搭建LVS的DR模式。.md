---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2020-02-20 23:23:23
description: 环境准备：三台虚拟机此环境是针对内部服务的架构，如数据库，缓存，共享存储等业务。虚拟机角色地址备注负载均衡器地址：服务器服务器负载均衡器注意这里的网卡名字服务器、服务器把绑定在上，是为了实现直接把结果。。。。。。。
image: ../../title_pic/31.jpg
slug: '202002202323'
tags:
- 运维
- ipvs
- ipvsadm
- DR
- 负载均衡
title: Centos7使用脚本搭建LVS的DR模式。
---

<!--more-->

![](format,png)

![](format,png)

环境准备：三台虚拟机

1）此环境是针对内部服务的LVS架构，如数据库，缓存，共享存储等业务。

<table border="1"><tbody><tr><td style="vertical-align:top;">虚拟机角色</td><td style="vertical-align:top;">IP地址</td><td style="vertical-align:top;">备注</td></tr><tr><td style="vertical-align:top;">LVS负载均衡器</td><td style="vertical-align:top;">192.168.116.129</td><td style="vertical-align:top;">VIP地址：192.168.116.100</td></tr><tr><td style="vertical-align:top;">http服务器RS1</td><td style="vertical-align:top;">192.168.116.130</td><td style="vertical-align:top;">&nbsp;</td></tr><tr><td style="vertical-align:top;">http服务器RS2</td><td style="vertical-align:top;">192.168.116.131</td><td style="vertical-align:top;">&nbsp;</td></tr></tbody></table>
 

### **LVS负载均衡器**

```bash
 vim /usr/local/sbin/lvs_dr.sh

#!/bin/bash   
 yum install -y net-tools ipvsadm                                                                          
 echo 1 > /proc/sys/net/ipv4/ip_forward
 ipv=/usr/sbin/ipvsadm
 vip=192.168.116.100
 rs1=192.168.116.130
 rs2=192.168.116.131
 #注意这里的网卡名字
 ifconfig ens33:2 $vip broadcast $vip netmask 255.255.255.255 up
 route add -host $vip dev ens33:2
 $ipv -C
 $ipv -A -t $vip:80 -s wrr
 $ipv -a -t $vip:80 -r $rs1:80 -g -w 1
 $ipv -a -t $vip:80 -r $rs2:80 -g -w 1
```

 

### **http服务器RS1、http服务器RS2**

```bash
 vim /usr/local/sbin/lvs_dr.sh

#/bin/bash  
 yum install -y net-tools                                                                         
 vip=192.168.116.100
 #把vip绑定在lo上，是为了实现rs直接把结果返回给客户端
 ifconfig lo:0 $vip broadcast $vip netmask 255.255.255.255 up
 route add -host $vip lo:0
 #以下操作为更改arp内核参数，目的是为了让rs顺利发送mac地址给客户端
 echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
 echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
 echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
 echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
```

 

# **运行脚本**

```bash
bash /usr/local/sbin/lvs_dr_rs.sh
```

**在httpd服务器创建文件测试**

```bash
yum install -y httpd && echo "this is one" >> /var/www/html/index.html && systemctl restart httpd
```

![](../../image/20200220231947152.png)

![](../../image/20200221105747161.png)