+++
author = "南宫乘风"
title = "Centos7使用脚本搭建LVS的DR模式。"
date = "2020-02-20 23:23:23"
tags=['运维', 'ipvs', 'ipvsadm', 'DR', '负载均衡']
categories=['Linux Shell']
image = "post/4kdongman/42.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104420466](https://blog.csdn.net/heian_99/article/details/104420466)

<img alt="" src="https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy85OTY3NTk1LTgxZDY1OGFjM2M3MTBlMGEucG5n?x-oss-process=image/format,png">

<img alt="" src="https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy85OTY3NTk1LWIyNWJhNDE4MjliYTUzZDQucG5n?x-oss-process=image/format,png">

环境准备：三台虚拟机

1）此环境是针对内部服务的LVS架构，如数据库，缓存，共享存储等业务。
<td style="vertical-align:top;">虚拟机角色</td><td style="vertical-align:top;">IP地址</td><td style="vertical-align:top;">备注</td>
<td style="vertical-align:top;">LVS负载均衡器</td><td style="vertical-align:top;">192.168.116.129</td><td style="vertical-align:top;">VIP地址：192.168.116.100</td>
<td style="vertical-align:top;">http服务器RS1</td><td style="vertical-align:top;">192.168.116.130</td><td style="vertical-align:top;"> </td>
<td style="vertical-align:top;">http服务器RS2</td><td style="vertical-align:top;">192.168.116.131</td><td style="vertical-align:top;"> </td>

 

### **LVS负载均衡器**

```
 vim /usr/local/sbin/lvs_dr.sh

#!/bin/bash   
 yum install -y net-tools ipvsadm                                                                          
 echo 1 &gt; /proc/sys/net/ipv4/ip_forward
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

```
 vim /usr/local/sbin/lvs_dr.sh

#/bin/bash  
 yum install -y net-tools                                                                         
 vip=192.168.116.100
 #把vip绑定在lo上，是为了实现rs直接把结果返回给客户端
 ifconfig lo:0 $vip broadcast $vip netmask 255.255.255.255 up
 route add -host $vip lo:0
 #以下操作为更改arp内核参数，目的是为了让rs顺利发送mac地址给客户端
 echo "1" &gt;/proc/sys/net/ipv4/conf/lo/arp_ignore
 echo "2" &gt;/proc/sys/net/ipv4/conf/lo/arp_announce
 echo "1" &gt;/proc/sys/net/ipv4/conf/all/arp_ignore
 echo "2" &gt;/proc/sys/net/ipv4/conf/all/arp_announce
```

 

# **运行脚本**

```
bash /usr/local/sbin/lvs_dr_rs.sh

```

**在httpd服务器创建文件测试**

```
yum install -y httpd &amp;&amp; echo "this is one" &gt;&gt; /var/www/html/index.html &amp;&amp; systemctl restart httpd

```

![20200220231947152.png](https://img-blog.csdnimg.cn/20200220231947152.png)

![20200221105747161.png](https://img-blog.csdnimg.cn/20200221105747161.png)
