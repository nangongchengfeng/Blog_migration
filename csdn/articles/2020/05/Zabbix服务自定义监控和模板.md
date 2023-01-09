+++
author = "南宫乘风"
title = "Zabbix服务自定义监控和模板"
date = "2020-05-13 17:22:05"
tags=['linux', 'zabbix', 'mysql', '监控']
categories=['Zabbix监控']
image = "post/4kdongman/35.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/106101006](https://blog.csdn.net/heian_99/article/details/106101006)

**目录**

 

[前言](#%E5%89%8D%E8%A8%80)

[如何入手监控](#%E5%A6%82%E4%BD%95%E5%85%A5%E6%89%8B%E7%9B%91%E6%8E%A7)

[一、zabbix 快速监控主机](#%E4%B8%80%E3%80%81zabbix%20%E5%BF%AB%E9%80%9F%E7%9B%91%E6%8E%A7%E4%B8%BB%E6%9C%BA)

[1.安装zabbix-agent](#1.%E5%AE%89%E8%A3%85zabbix-agent)

[2.配置zabbix-agent(修改配置)](#2.%E9%85%8D%E7%BD%AEzabbix-agent%28%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE%29)

[3.启动zabbix-agent并检查](#3.%E5%90%AF%E5%8A%A8zabbix-agent%E5%B9%B6%E6%A3%80%E6%9F%A5)

[4.zabbix-web界面，添加主机](#4.zabbix-web%E7%95%8C%E9%9D%A2%EF%BC%8C%E6%B7%BB%E5%8A%A0%E4%B8%BB%E6%9C%BA)

[二、自定义监控主机小试身手](#%E4%BA%8C%E3%80%81%E8%87%AA%E5%AE%9A%E4%B9%89%E7%9B%91%E6%8E%A7%E4%B8%BB%E6%9C%BA%E5%B0%8F%E8%AF%95%E8%BA%AB%E6%89%8B)

[1.监控需求](#1.%E7%9B%91%E6%8E%A7%E9%9C%80%E6%B1%82)

[2.命令行实现](#2.%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%AE%9E%E7%8E%B0)

[3.编写zabbix监控文件(传参形式)](#3.%E7%BC%96%E5%86%99zabbix%E7%9B%91%E6%8E%A7%E6%96%87%E4%BB%B6%28%E4%BC%A0%E5%8F%82%E5%BD%A2%E5%BC%8F%29)

[4.server端进行测试](#4.server%E7%AB%AF%E8%BF%9B%E8%A1%8C%E6%B5%8B%E8%AF%95)

         [5.web端添加](#5.web%E7%AB%AF%E6%B7%BB%E5%8A%A0)

## 前言

**[Centos7安装Zabbix服务端、Zabbix客户端和Win客户端配置（源码编译安装）](https://blog.csdn.net/heian_99/article/details/106023595)**

前面介绍怎么源码编译安装Zabbix和主机添加。下面要介绍怎么添加模板和自定义监控

## 如何入手监控

>  
 1.硬件监控 路由器、交换机、防火墙<br> 2.系统监控 CPU、内存、磁盘、网络、进程、 TCP<br> 3.服务监控 nginx、 php、 tomcat、 redis、 memcache、 mysql<br> 4.WEB 监控 请求时间、响应时间、加载时间、<br> 5.日志监控 ELk（收集、存储、分析、展示） 日志易<br> 6.安全监控 Firewalld、 WAF(Nginx+lua)、安全宝、牛盾云、安全狗<br> 7.网络监控 smokeping 多机房<br> 8.业务监控 活动引入多少流量、产生多少注册量、带来多大价值 


## 一、zabbix 快速监控主机

### **1.安装zabbix-agent**

```
rpm -ivh https://mirror.tuna.tsinghua.edu.cn/zabbix/zabbix/4.0/rhel/7/x86_64/zabbix-agent-4.0.4-1.el7.x86_64.rpm
```

### **2.配置zabbix-agent(修改配置)**

```
[root@kvm zabbix]# grep "^[a-Z]" /etc/zabbix/zabbix_agentd.conf
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server=192.168.1.10
ServerActive=192.168.1.10
Hostname=Zabbix_kvm
Include=/etc/zabbix/zabbix_agentd.d/*.conf

```

### **3.启动zabbix-agent并检查**

![20200513165443770.png](https://img-blog.csdnimg.cn/20200513165443770.png)

### **4.zabbix-web界面，添加主机**

![20200513165608707.png](https://img-blog.csdnimg.cn/20200513165608707.png)

![20200513165718476.png](https://img-blog.csdnimg.cn/20200513165718476.png)

![2020051316595198.png](https://img-blog.csdnimg.cn/2020051316595198.png)

**这边配置自动发现和自动注册（可以自动发现和添加主机和模板）**

![20200513170035522.png](https://img-blog.csdnimg.cn/20200513170035522.png)

## 二、自定义监控主机小试身手

### 1.监控需求

监控TCP3种状态集

### 2.命令行实现

```
[root@kvm zabbix]#  netstat -ant|grep -c TIME_WAIT
1
[root@kvm zabbix]#  netstat -ant|grep -c LISTEN
13

```

### 3.编写zabbix监控文件(传参形式)

```
[root@kvm zabbix]# cat /etc/zabbix/zabbix_agentd.d/tcp_status.conf
UserParameter=tcp_state[*],netstat -ant|grep -c $1
[root@kvm zabbix]# systemctl restart zabbix-agent.service 

```

### 4.server端进行测试

```
[root@master zabbix]# /data/zabbix/bin/zabbix_get -s 192.168.1.100  -k tcp_state[TIME_WAIT]
6
[root@master zabbix]# /data/zabbix/bin/zabbix_get -s 192.168.1.100  -k tcp_state[LISTEN]
13

```

### 5.web端添加

![20200513171340178.png](https://img-blog.csdnimg.cn/20200513171340178.png)

![20200513171350962.png](https://img-blog.csdnimg.cn/20200513171350962.png)

![20200513171406244.png](https://img-blog.csdnimg.cn/20200513171406244.png)

![20200513171440577.png](https://img-blog.csdnimg.cn/20200513171440577.png)

数据出来了

![20200513171552382.png](https://img-blog.csdnimg.cn/20200513171552382.png)

![20200513171924500.png](https://img-blog.csdnimg.cn/20200513171924500.png)

 

 
