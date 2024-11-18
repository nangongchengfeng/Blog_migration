---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-02-02 20:00:04
description: 、服务简介，动态主机配置协议是一个局域网的网络协议，使用协议工作，主要有两个用途给内部网络或网络服务供应商自动分配地址，给用户或者内部网络管理员作为对所有计算机作中央管理的手段，在中有详细的描述。有个。。。。。。。
image: ../../title_pic/60.jpg
slug: '201902022000'
tags:
- linux
title: Linux服务管理之DHCP
---

<!--more-->

## 1、DHCP服务简介

**DHCP\(Dynamic Host Configuration Protocol，动态主机配置协议\)是一个**[**局域网**](https://baike.so.com/doc/3165868-3336420.html)**的**[**网络协议**](https://baike.so.com/doc/5403497-5641193.html)**，使用**[**UDP**](https://baike.so.com/doc/5418284-5656447.html)**协议工作， 主要有两个用途:给内部网络或**[**网络服务**](https://baike.so.com/doc/520018-550563.html)**供应商自动分配IP地址，给用户或者内部网络管理员作为对所有**[**计算机**](https://baike.so.com/doc/3435270-3615253.html)**作中央管理的手段，在RFC 2131中有详细的描述。DHCP有3个端口，其中UDP67和UDP68为正常的DHCP服务端口，分别作为DHCP Server和DHCP Client的服务端口;546号端口用于DHCPv6 Client，而不用于DHCPv4，是为DHCP failover服务，这是需要特别开启的服务，DHCP failover是用来做"双机热备"的。**

## 2、DHCP服务作用

**为大量客户机自动分配地址，提供集中管理**

**减轻管理和维护成本、提高网络配置效率  
         
       原理：  
            1.客户端发送DHCP Discovery探索DHCP服务器   
            2.DHCP服务器发送DHCP Offer \(IP/NETMASK/GATEWAY/DNS\)  
            3.客户端发送DHCP Request  
            4.DHCP服务器发送DHCP ACK  
            5.客户端发送Gratuation ARP用于检测IP地址是否冲突  
            **![](../../image/20190202195928715.png)  
**软件：dhcp  
配置文件：/etc/dhcp/dhcpd.conf  
服务：dhcpd  
端口：67/udp（DHCP服务端口） ,68/udp（DHCP客户端端口）**