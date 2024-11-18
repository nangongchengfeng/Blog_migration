---
author: 南宫乘风
categories:
- Prometheus监控
date: 2020-01-13 10:40:01
description: 相关博文：、安装普罗米修斯监控系统完整版、普罗米修斯监控数据库、普罗米修斯安装可视化图形工具、的图形显示监控数据、普罗米修斯的实现报警功能目录一、普罗米修斯概述二、时间序列数据、什么是序列数据、时间序。。。。。。。
image: http://image.ownit.top/4kdongman/76.jpg
tags:
- 普罗米修斯
- 监控
- Promethus
title: Centos7安装Promethus(普罗米修斯）监控系统完整版
---

<!--more-->

# 相关博文：

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)

**目录**

 

[一、普罗米修斯概述](#%E4%B8%80%E3%80%81%E6%99%AE%E7%BD%97%E7%B1%B3%E4%BF%AE%E6%96%AF%E6%A6%82%E8%BF%B0)

[二、时间序列数据](#%E4%BA%8C%E3%80%81%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E6%95%B0%E6%8D%AE)

[1、什么是序列数据](#1%E3%80%81%E4%BB%80%E4%B9%88%E6%98%AF%E5%BA%8F%E5%88%97%E6%95%B0%E6%8D%AE)

[2、时间序列数据特点](#2%E3%80%81%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E6%95%B0%E6%8D%AE%E7%89%B9%E7%82%B9)

[3、Prometheus的主要特征](#3%E3%80%81Prometheus%E7%9A%84%E4%B8%BB%E8%A6%81%E7%89%B9%E5%BE%81)

[4、普罗米修斯原理架构图](#4%E3%80%81%E6%99%AE%E7%BD%97%E7%B1%B3%E4%BF%AE%E6%96%AF%E5%8E%9F%E7%90%86%E6%9E%B6%E6%9E%84%E5%9B%BE)

[三、实验环境准备](#%E4%B8%89%E3%80%81%E5%AE%9E%E9%AA%8C%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87)

[1、安装prometheus](#1%E3%80%81%E5%AE%89%E8%A3%85prometheus)

[2、prometheus界面](#2%E3%80%81prometheus%E7%95%8C%E9%9D%A2)

[3、主机数据展示](#3%E3%80%81%E4%B8%BB%E6%9C%BA%E6%95%B0%E6%8D%AE%E5%B1%95%E7%A4%BA)

[4、监控远程Linux主机](#4%E3%80%81%E7%9B%91%E6%8E%A7%E8%BF%9C%E7%A8%8BLinux%E4%B8%BB%E6%9C%BA)

---

# 一、普罗米修斯概述

Prometheus\(由go语言\(golang\)开发\)是一套开源的监控\&报警\&时间序列数 据库的组合。适合监控docker容器。因为kubernetes\(俗称k8s\)的流行带动 了prometheus的发展。  
<https://prometheus.io/docs/introduction/overview/>

# 二、时间序列数据

## 1、什么是序列数据

**时间序列数据**\(TimeSeries Data\) : 按照时间顺序记录系统、设备状态变化 的数据被称为时序数据。  
应用的场景很多, 如：

- 无人驾驶车辆运行中要记录的经度，纬度，速度，方向，旁边物体的距 离等等。每时每刻都要将数据记录下来做分析。
- 某一个地区的各车辆的行驶轨迹数据
- 传统证券行业实时交易数据
- 实时运维监控数据等

## 2、时间序列数据特点

- 性能好

关系型数据库对于大规模数据的处理性能糟糕。NOSQL可以比较好的处理 大规模数据，让依然比不上时间序列数据库。

- 存储成本低

高效的压缩算法，节省存储空间，有效降低IO  
Prometheus有着非常高效的时间序列数据存储方法，每个采样数据仅仅占 用3.5byte左右空间，上百万条时间序列，30秒间隔，保留60天，大概花了 200多G（来自官方数据\)

## 3、Prometheus的主要特征

多维度数据模型 灵活的查询语言 不依赖分布式存储，单个服务器节点是自主的 以HTTP方式，通过pull模型拉去时间序列数据        也可以通过中间网关支持push模型 通过服务发现或者静态配置，来发现目标服务对象 支持多种多样的图表和界面展示

## 4、普罗米修斯原理架构图

![](http://image.ownit.top/csdn/20200113095930827.png)

 

# 三、实验环境准备

<table border="1" cellpadding="1" cellspacing="1" style="width:500px;"><tbody><tr><td>服务器</td><td>IP地址</td></tr><tr><td>Prometneus服务器</td><td>192.168.116.129</td></tr><tr><td>被监控服务器</td><td>192.168.116.130</td></tr><tr><td>grafana服务器</td><td>192.168.116.131</td></tr></tbody></table>
 

教程使用的软件：链接: <https://pan.baidu.com/s/1QV4KYZksyIp65UsScioq4Q> 提取码: vcej

失效可联系我

1\. 静态ip\(要求能上外网\)

2\. 主机名

```bash
各自配置好主机名 
# hostnamectl set-hostname --static server.cluster.com 
三台都互相绑定IP与主机名 
# vim /etc/hosts            
192.168.116.129  master
192.168.116.130  node1
192.168.116.131  node2
```

```
echo "192.168.116.129 master
192.168.116.130 node1
192.168.116.131 node2">>/etc/hosts
```

3\. 时间同步\(时间同步一定要确认一下\)

```
 yum install -y  ntpdate && ntpdate time.windows.com
```

4\. 关闭防火墙,selinux

```
# systemctl stop firewalld 
# systemctl disable firewalld 
# iptables -F
```

## 1、安装prometheus

从 [https://prometheus.io/download/]() 下载相应版本，安装到服务器上  
官网提供的是二进制版，解压就能用，不需要编译

上传prometheus-2.5.0.linux-amd64.tar.gz

![](http://image.ownit.top/csdn/20200113101351305.png)

```
tar -zxvf prometheus-2.5.0.linux-amd64.tar.gz -C /usr/local/
mv /usr/local/prometheus-2.5.0.linux-amd64/  /usr/local/prometheus
```

![](http://image.ownit.top/csdn/20200113101544140.png)

直接使用默认配置文件启动

```bash
/usr/local/prometheus/prometheus --config.file="/usr/local/prometheus/prometheus.yml" &
```

确认端口\(9090\)

```
ss -anltp | grep 9090
```

![](http://image.ownit.top/csdn/20200113101750160.png)

## 2、prometheus界面

通过浏览器访问http://服务器IP:9090就可以访问到prometheus的主界面

![](http://image.ownit.top/csdn/20200113101851876.png)

默认只监控了本机一台，点Status \--》点Targets \--》可以看到只监控了本 机

![](http://image.ownit.top/csdn/2020011310193370.png)

## 3、主机数据展示

通过http://服务器IP:9090/metrics可以查看到监控的数据

![](http://image.ownit.top/csdn/20200113102009365.png)

在web主界面可以通过关键字查询监控项

![](http://image.ownit.top/csdn/20200113102110196.png)

## 4、监控远程Linux主机

① 在远程linux主机\(被监控端agent1\)上安装node\_exporter组件  
下载地址: <https://prometheus.io/download/>

上传node\_exporter-0.16.0.linux-amd64.tar.gz

![](http://image.ownit.top/csdn/20200113102232475.png)

```
tar -zxvf node_exporter-0.16.0.linux-amd64.tar.gz -C /usr/local/
mv /usr/local/node_exporter-0.16.0.linux-amd64/ /usr/local/node_exporter
```

里面就一个启动命令node\_exporter,可以直接使用此命令启动

```
nohup /usr/local/node_exporter/node_exporter & 
```

![](http://image.ownit.top/csdn/2020011310252095.png)

确认端口\(9100\)

![](http://image.ownit.top/csdn/20200113102549361.png)

**扩展: nohup命令: 如果把启动node\_exporter的终端给关闭,那么进程也会 随之关闭。nohup命令会帮你解决这个问题。**

 

② 通过浏览器访问http://被监控端IP:9100/metrics就可以查看到 node\_exporter在被监控端收集的监控信息

![](http://image.ownit.top/csdn/20200113102712354.png)

③ 回到prometheus服务器的配置文件里添加被监控机器的配置段

在主配置文件最后加上下面三行

```
vim /usr/local/prometheus/prometheus.yml 
```

```bash
  - job_name: 'node1'
    static_configs:
    - targets: ['192.168.116.130:9100']
```

![](http://image.ownit.top/csdn/20200113103626972.png)

```bash
- job_name: 'agent1'                   # 取一个job名称来代 表被监控的机器   
  static_configs:   
  - targets: ['10.1.1.14:9100']        # 这里改成被监控机器 的IP，后面端口接9100
```

改完配置文件后,重启服务

```
 pkill prometheus 
```

确认端口没有进程占用

![](http://image.ownit.top/csdn/20200113103154560.png)

```
/usr/local/prometheus/prometheus --config.file="/usr/local/prometheus/prometheus.yml" &
```

 确认端口被占用，说 明重启成功

![](http://image.ownit.top/csdn/20200113103316583.png)

④ 回到web管理界面 \--》点Status \--》点Targets \--》可以看到多了一台监 控目标

![](http://image.ownit.top/csdn/20200113103730436.png)

练习: 加上本机prometheus的监控  
答: 在本机安装node\_exporter，也使用上面的方式监控起来。

# 相关博文：

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)