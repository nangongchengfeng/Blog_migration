---
author: 南宫乘风
categories:
- Nginx
date: 2019-11-26 20:42:29
description: 、简介介绍的应用场景和具体可以做什么事情介绍什么是反向代理介绍什么是负载均衡介绍什么是动静分离、安装介绍在系统中如何进行安装、常用的命令和配置文件介绍启动、关闭、重新加载命令介绍的配置文件概述是一个高。。。。。。。
image: ../../title_pic/14.jpg
slug: '201911262042'
tags:
- 技术记录
title: Nginx 简介与安装、常用的命令和配置文件
---

<!--more-->

 

## 1、nginx 简介

**（1）介绍 nginx 的应用场景和具体可以做什么事情**

**（2）介绍什么是反向代理**

**（3）介绍什么是负载均衡**

**（4）介绍什么是动静分离**

## 2、nginx 安装

**（1）介绍 nginx 在 linux 系统中如何进行安装**

## 3、nginx 常用的命令和配置文件

**（1）介绍 nginx 启动、关闭、重新加载命令**

**（2）介绍 nginx 的配置文件**

 

### 1.1 Nginx 概述

Nginx \("engine x"\) 是一个高性能的 HTTP 和反向代理服务器,特点是占有内存少，并发能 力强，事实上 nginx 的并发能力确实在同类型的网页服务器中表现较好，中国大陆使用 nginx 网站用户有：百度、京东、新浪、网易、腾讯、淘宝等

### 1.2 Nginx 作为 web 服务器

**Nginx 可以作为静态页面的 web 服务器，同时还支持 CGI 协议的动态语言，比如 perl、php 等。但是不支持 java。Java 程序只能通过与 tomcat 配合完成。Nginx 专为性能优化而开发， 性能是其最重要的考量,实现上非常注重效率 ，能经受高负载的考验,有报告表明能支持高 达 50,000 个并发连接数。 https://lnmp.org/nginx.html**

### 1.3 正向代理

**Nginx 不仅可以做反向代理，实现负载均衡。还能用作正向代理来进行上网等功能。 正向代理：如果把局域网外的 Internet 想象成一个巨大的资源库，则局域网中的客户端要访 问 Internet，则需要通过代理服务器来访问，这种代理服务就称为正向代理。**

![](../../image/20191126202429129.png)

### 1.4 反向代理

**反向代理，其实客户端对代理是无感知的，因为客户端不需要任何配置就可以访问，我们只 需要将请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据后，在返 回给客户端，此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器 地址，隐藏了真实服务器 IP 地址。**

![](../../image/20191126202505208.png)

### 1.5 负载均衡

       客户端发送多个请求到服务器，服务器处理请求，有一些可能要与数据库进行交互，服 务器处理完毕后，再将结果返回给客户端。

        这种架构模式对于早期的系统相对单一，并发请求相对较少的情况下是比较适合的，成 本也低。但是随着信息数量的不断增长，访问量和数据量的飞速增长，以及系统业务的复杂 度增加，这种架构会造成服务器相应客户端的请求日益缓慢，并发量特别大的时候，还容易 造成服务器直接崩溃。很明显这是由于服务器性能的瓶颈造成的问题，那么如何解决这种情 况呢？

        我们首先想到的可能是升级服务器的配置，比如提高 CPU 执行频率，加大内存等提高机 器的物理性能来解决此问题，但是我们知道摩尔定律的日益失效，硬件的性能提升已经不能 满足日益提升的需求了。最明显的一个例子，天猫双十一当天，某个热销商品的瞬时访问量 是极其庞大的，那么类似上面的系统架构，将机器都增加到现有的顶级物理配置，都是不能 够满足需求的。那么怎么办呢？

          上面的分析我们去掉了增加服务器物理配置来解决问题的办法，也就是说纵向解决问题 的办法行不通了，那么横向增加服务器的数量呢？这时候集群的概念产生了，单个服务器解 决不了，我们增加服务器的数量，然后将请求分发到各个服务器上，将原先请求集中到单个 java 课程系列服务器上的情况改为将请求分发到多个服务器上，将负载分发到不同的服务器，也就是我们 所说的负载均衡

![](../../image/20191126202642739.png)

### 1.6 动静分离

**为了加快网站的解析速度，可以把动态页面和静态页面由不同的服务器来解析，加快解析速 度。降低原来单个服务器的压力。**

![](../../image/20191126202715313.png)

## 第 2 章 Nginx 安装

### 2.1 进入 nginx 官网，下载

<http://nginx.org/>

![](../../image/2019112620300673.png)

### 2.2 安装 nginx

**第一步，安装 pcre**  
 

```bash
wget http://downloads.sourceforge.net/project/pcre/pcre/8.37/pcre-8.37.tar.gz
```

- 解压文件，
- ./configure 完成后，回到 pcre 目录下执行 make，
- 再执行 make install

**第二步，安装 openssl**

**第三步，安装 zlib**

```
yum -y install make zlib zlib-devel gcc-c++ libtool openssl openssl-devel
```

**第四步，安装 nginx**

- **1、 解压缩 nginx-xx.tar.gz 包。**
- **2、 进入解压缩目录，执行./configure。**
- **3、 make \&\& make install**

**查看开放的端口号**

- firewall-cmd --list-all

**设置开放的端口号**

- firewall-cmd --add-service=http –permanent
- sudo firewall-cmd --add-port=80/tcp --permanent

**重启防火墙**

- firewall-cmd –reload

## 第 3 章 nginx 常用的命令和配置文件

### 3.1 nginx 常用的命令：

**（1）启动命令**

**在/usr/local/nginx/sbin 目录下执行 ./nginx**

**（2）关闭命令**

**在/usr/local/nginx/sbin 目录下执行 ./nginx \-s stop**

（3）重新加载命令

**在/usr/local/nginx/sbin 目录下执行 ./nginx \-s reload**

### 3.2 nginx.conf 配置文件

**nginx 安装目录下，其默认的配置文件都放在这个目录的 conf 目录下，而主配置文件 nginx.conf 也在其中，后续对 nginx 的使用基本上都是对此配置文件进行相应的修改**

![](../../image/20191126203613627.png)

**配置文件中有很多#， 开头的表示注释内容，我们去掉所有以 # 开头的段落，精简之后的 内容如下：**

![](../../image/20191126203700973.png)

### 根据上述文件，我们可以很明显的将 nginx.conf 配置文件分为三部分：

### 第一部分：全局块

          **从配置文件开始到 events 块之间的内容，主要会设置一些影响 nginx 服务器整体运行的配置指令，主要包括配 置运行 Nginx 服务器的用户（组）、允许生成的 worker process 数，进程 PID 存放路径、日志存放路径和类型以 及配置文件的引入等。**

比如上面第一行配置的：

```
worker_processes  1;
```

**这是 Nginx 服务器并发处理服务的关键配置，worker\_processes 值越大，可以支持的并发处理量也越多，但是 会受到硬件、软件等设备的制约**

### 第二部分：events 块

比如上面的配置：

```
events {
    worker_connections  1024;
}
```

**events 块涉及的指令主要影响 Nginx 服务器与用户的网络连接，常用的设置包括是否开启对多 work process 下的网络连接进行序列化，是否允许同时接收多个网络连接，选取哪种事件驱动模型来处理连接请求，每个 word process 可以同时支持的最大连接数等。**

 

- **上述例子就表示每个 work process 支持的最大连接数为 1024.**
- **这部分的配置对 Nginx 的性能影响较大，在实际中应该灵活配置。**

### 第三部分：http 块

```
http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }
}
```

**这算是 Nginx 服务器配置中最频繁的部分，代理、缓存和日志定义等绝大多数功能和第三方模块的配置都在这里。 需要注意的是：http 块也可以包括 http 全局块、server 块。**

**①、http 全局块**

- http 全局块配置的指令包括文件引入、MIME-TYPE 定义、日志自定义、连接超时时间、单链接请求数上限等。

**②、server 块**

**这块和虚拟主机有密切关系，虚拟主机从用户角度看，和一台独立的硬件主机是完全一样的，该技术的产生是为了 节省互联网服务器硬件成本。**

- 每个 http 块可以包括多个 server 块，而每个 server 块就相当于一个虚拟主机。
- 而每个 server 块也分为全局 server 块，以及可以同时包含多个 locaton 块。

**1、全局 server 块**

- 最常见的配置是本虚拟机主机的监听配置和本虚拟主机的名称或 IP 配

**2、location 块**

- 一个 server 块可以配置多个 location 块。

**这块的主要作用是基于 Nginx 服务器接收到的请求字符串（例如 server\_name/uri-string），对虚拟主机名称 （也可以是 IP 别名）之外的字符串（例如 前面的 /uri-string）进行匹配，对特定的请求进行处理。地址定向、数据缓 存和应答控制等功能，还有许多第三方模块的配置也在这里进行。**

## 相关博文：

### [Nginx 简介与安装、常用的命令和配置文件](https://blog.csdn.net/heian_99/article/details/103264404)

## [nginx 配置实例-反向代理](https://blog.csdn.net/heian_99/article/details/103292763)

### [nginx 配置实例-负载均衡](https://blog.csdn.net/heian_99/article/details/103298249)

### [Nginx 配置实例-动静分离](https://blog.csdn.net/heian_99/article/details/103391378)

### [Nginx 配置高可用的集群](https://blog.csdn.net/heian_99/article/details/103391454)