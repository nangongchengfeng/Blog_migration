---
author: 南宫乘风
categories:
- Linux实战操作
date: 2022-02-09 15:29:30
description: 服务简介：域名系统是因特网的一项服务。它作为将域名和地址相互映射的一个分布式数据库，能够使人更方便地访问互联网。是一个应用层的协议使用和端口。是一个分布式数据库命名系统采用层次的逻辑结构如同一颗倒置的。。。。。。。
image: ../../title_pic/10.jpg
slug: '202202091529'
tags:
- 网络
- 网络协议
- DNS
title: 内网DNS重要使用作用
---

<!--more-->

## DNS服务简介：

DNS\(Domain Name System–域名系统\),是因特网的一项服务。它作为将域名和IP地址相互映射的一个分布式数据库，能够使人更方便地访问互联网。是一个应用层的协议DNS使用TCP和UDP端口53。

DNS是一个分布式数据库,命名系统采用层次的逻辑结构,如同一颗倒置的树,这个逻辑的树形结构称为域名空间,由于DNS划分了域名空间,所以各机构可以使用自己的域名空间创建DNS信息.

> 注:DNS域名空间中,树的最大深度不得超过127层,树中每个节点最长可以存储63个字符.

以上是在公网中的使用

更详细介绍：[DNS服务器搭建与配置 | 曹世宏的博客](https://cshihong.github.io/2018/10/15/DNS%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%90%AD%E5%BB%BA%E4%B8%8E%E9%85%8D%E7%BD%AE/ "DNS服务器搭建与配置 | 曹世宏的博客")

## DNS内网使用

首先，我们纯内网中，是不能过连接外网的环境的。

但是纯内网也会有许多的IP和服务，我们该怎么来区分，总不能记录所有IP，所以我们需要自建内网的DNS，达到内网域名解析的效果。

## DNS使用作用

**WHAT**：DNS（域名系统）说白了，就是把一个域和IP地址做了一下绑定，如你在里机器里面输入 nslookup <www.qq.com>，出来的Address是一堆IP，IP是不容易记的，所以DNS让IP和域名做一下绑定，这样你输入域名就可以了

**WHY**：我们要用ingress，在K8S里要做7层调度，而且无论如何都要用域名（如之前的那个百度页面的域名，那个是host的方式），但是问题是我们怎么给K8S里的容器绑host，所以我们必须做一个DNS，然后容器服从我们的DNS解析调度

我们会在10.4.7.11 安装dns主服务，10.4.7.12作为备用dns服务

也可以走一层keepalive虚拟IP。

![](../../image/5cc0cd46983c450a8dd5b52fd96b095d.png)

可以简单理解成：

11机器：反向代理

12机器：反向代理

21机器：主控+运算节点（即服务群都是跑在21和22上）

22机器：主控+运算节点（生产上我们会把主控和运算分开）

200机器：运维主机（放各种文件资源）

这样控节点有两个，运算节点有两个，就是小型的分布式，现在你可能没办法理解这些内容，我们接着做下去，慢慢的，你就理解了

![](../../image/9d341b2245e44548b910418e45e37d27.png) ![](../../image/f95bc2b3fd604742ad3f46a9e0a990d5.png)

## 初始化

```bash
# 查看enforce是否关闭，确保disabled状态，当然可能没有这个命令
~]# getforce
# 查看内核版本，确保在3.8以上版本
~]# uname -a
# 关闭firewalld
~]# systemctl stop firewalld
# 安装epel源及相关工具
~]# yum install epel-release -y
~]# yum install wget net-tools telnet tree nmap sysstat lrzsz dos2unix bind-utils -y
```

 

> **uname**:显示系统信息
> 
> - **\-a/-all**：显示全部
> 
> **yum**：提供了查找、安装、删除某一个、一组甚至全部软件包的命令
> 
> - **install**：安装
> 
> - **\-y**：当安装过程提示选择全部为"yes"

## 安装步骤 

```bash
# 在11机器：
~]# yum install bind -y
~]# rpm -qa bind
# out: bind-9.11.4-9.P2.el7.x86_64
# 配置主配置文件，11机器
~]# vi /etc/named.conf
listen-on port 53 { 10.4.7.11; };  # 原本是127.0.0.1
# listen-on-v6 port 53 { ::1; };  # 需要删掉
allow-query     { any; };  # 原本是locall
forwarders      { 10.4.7.254; };  #另外添加的
dnssec-enable no;  # 原本是yes
dnssec-validation no;  # 原本是yes

# 检查修改情况，没有报错即可（即没有信息）
~]# named-checkconf
```

![](../../image/fa3f75b9297c4bda9446a5eea96eb746.png)

 

 

> **rpm**：软件包管理器
> 
> - **\-qa**：查看已安装的所有软件包
> 
> **rpm和yum安装的区别**：前者不检查相依性问题，后者检查（即相关依赖包）
> 
> **named.conf文件内容解析：**
> 
> - **listen-on**：监听端口，改为监听在内网，这样其它机器也可以用
> 
> - **allow-query**：哪些客户端能通过自建的DNS查
> 
> - **forwarders**：上级DNS是什么

```bash
# 11机器，经验：主机域一定得跟业务是一点关系都没有，如host.com，而业务用的是od.com，因为业务随时可能变
# 区域配置文件，加在最下面
~]# vi /etc/named.rfc1912.zones
zone "host.com" IN {
        type  master;
        file  "host.com.zone";
        allow-update { 10.4.7.11; };
};

zone "od.com" IN {
        type  master;
        file  "od.com.zone";
        allow-update { 10.4.7.11; };
};
```

![](../../image/3c2e103f1907498f9301f785637e95b1.png)

 

```bash
# 11机器：
# 注意serial行的时间，代表今天的时间+第一条记录：20200112+01
7-11 ~]# vi /var/named/host.com.zone
$ORIGIN host.com.
$TTL 600	; 10 minutes
@       IN SOA	dns.host.com. dnsadmin.host.com. (
				2020011201 ; serial
				10800      ; refresh (3 hours)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				86400      ; minimum (1 day)
				)
			NS   dns.host.com.
$TTL 60	; 1 minute
dns                A    10.4.7.11
HDSS7-11           A    10.4.7.11
HDSS7-12           A    10.4.7.12
HDSS7-21           A    10.4.7.21
HDSS7-22           A    10.4.7.22
HDSS7-200          A    10.4.7.200

7-11 ~]# vi /var/named/od.com.zone
$ORIGIN od.com.
$TTL 600	; 10 minutes
@   		IN SOA	dns.od.com. dnsadmin.od.com. (
				2020011201 ; serial
				10800      ; refresh (3 hours)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				86400      ; minimum (1 day)
				)
				NS   dns.od.com.
$TTL 60	; 1 minute
dns                A    10.4.7.11

# 看一下有没有报错
7-11 ~]# named-checkconf
7-11 ~]# systemctl start named
7-11 ~]# netstat -luntp|grep 53
```

> **TTL 600**：指定IP包被路由器丢弃之前允许通过的最大网段数量
> 
> - **10 minutes**：过期时间10分钟
> 
> **SOA**：一个域权威记录的相关信息，后面有5组参数分别设定了该域相关部分
> 
> - **dnsadmin.od.com.** 一个假的邮箱
> 
> - **serial**：记录的时间
> 
> **\$ORIGIN**：即下列的域名自动补充od.com，如dns，外面看来是dns.od.com
> 
> **netstat \-luntp**：显示 tcp,udp 的端口和进程等相关情况

![](../../image/e5d8352ea8014b0b84d145575825706d.png) 

```bash
# 11机器，检查主机域是否解析
7-11 ~]# dig -t A hdss7-21.host.com @10.4.7.11 +short
# 配置linux客户端和win客户端都能使用这个服务，修改
7-11 ~]# vi /etc/sysconfig/network-scripts/ifcfg-eth0
DNS1=10.4.7.11
7-11 ~]# systemctl restart network
7-11 ~]# ping www.baidu.com
7-11 ~]# ping hdss7-21.host.com
```

 

> **dig \-t A**：指的是找DNS里标记为A的相关记录，而后面会带上相关的域，如上面的hdss7-21.host.com，为什么外面配了HDSS7-21后面还会自动接上.host.com就是因为\$ORIGIN，后面则是对应的IP
> 
> - **+short**：表示只返回IP

 ![](../../image/0b53fb98062c468c880f505207de3f2b.png)

```bash
# 在所有机器添加search... ，即可使用短域名（我的是自带的）
~]# vi /etc/resolv.conf
~]# ping hdss7-200
```

 ![](../../image/52aa54db0528485583b7f66995f97f15.png)

 

```bash
# 在非11机器上，全部改成11
~]# vi /etc/sysconfig/network-scripts/ifcfg-eth0
DNS1=10.4.7.11

~]# systemctl restart network
# 试下网络是否正常
~]# ping baidu.com
# 其它机器尝试ping7-11机器
7-12 ~]# ping hdss7-11.host.com
```

让其它机器的DNS全部改成11机器的好处是，全部的机器访问外网就只有通过11端口，更好控制

![](../../image/7208f6e3d88e4f079787fa0e8f65b45f.png) # 修改window网络，并ping

 ![](../../image/2bb3f7059f2a46998441b414dbae5b89.png)

 ![](../../image/421efbcdb8414ce390d8a738af3505f3.png)

 

## 后续域名解析

```
[root@hdss7-11 ~]# cat /var/named/od.com.zone 
$ORIGIN od.com.
$TTL 600	; 10 minutes
@   		IN SOA	dns.od.com. dnsadmin.od.com. (
				2020011523 ; serial  #这个需要每次增加1
				10800      ; refresh (3 hours)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				86400      ; minimum (1 day)
				)
				NS   dns.od.com.
$TTL 60	; 1 minute
dns                A    10.4.7.11
harbor             A    10.4.7.200
k8s-yaml           A    10.4.7.200
traefik            A    10.4.7.10
dashboard          A    10.4.7.10
zk1                A   10.4.7.11
zk2                A   10.4.7.12
zk3                A   10.4.7.21
jenkins            A   10.4.7.10
gitlab             A    10.4.7.200
dubbo-monitor      A    10.4.7.10
demo               A    10.4.7.10
config             A    10.4.7.10
mysql              A    10.4.7.11
portal             A    10.4.7.10
zk-test            A    10.4.7.11
zk-prod            A    10.4.7.12
config-test        A    10.4.7.10
config-prod        A    10.4.7.10
demo-test          A    10.4.7.10
demo-prod          A    10.4.7.10
blackbox           A    10.4.7.10
prometheus         A    10.4.7.10
grafana            A    10.4.7.10
km                 A    10.4.7.10
kibana             A    10.4.7.10
```

![](../../image/d513383889f24a618bd3dd6eb59f0504.png)