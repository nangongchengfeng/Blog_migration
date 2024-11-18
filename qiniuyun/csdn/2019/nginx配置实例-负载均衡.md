---
author: 南宫乘风
categories:
- Nginx
date: 2019-11-28 18:03:28
description: 、实现效果浏览器地址栏输入地址，负载均衡效果，平均和端口中、准备工作准备两台服务器，一台，一台在两台里面目录中，创建名称是文件夹，在文件夹中创建页面，用于测试、在的配置文件中进行负载均衡的配置、分配服。。。。。。。
image: ../../title_pic/77.jpg
slug: '201911281803'
tags:
- 技术记录
title: nginx 配置实例-负载均衡
---

<!--more-->

## 1、实现效果

（1）浏览器地址栏输入地址 http://www.123.com/edu/a.html，负载均衡效果，平均 8080 和 8081 端口中

## 2、准备工作

（1）准备两台 tomcat 服务器，一台 8080，一台 8082

（2）在两台 tomcat 里面 webapps 目录中，创建名称是 edu 文件夹，在 edu 文件夹中创建 页面 a.html，用于测试 

## 3、在 nginx 的配置文件中进行负载均衡的配置

```
upstream heian{
   server  localhost:8080;
   server  localhost:8082;
}
```

![](../../image/2019112817574981.png)

![](../../image/20191128175948286.png)

![](../../image/20191128180003645.png)

##   
 4、nginx 分配服务器策略

**第一种 轮询（默认）**

- 每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器 down 掉，能自动剔除

**第二种 weight **

 -    weight 代表权重默认为 1,权重越高被分配的客户端越
 -    指定轮询几率，weight 和访问比率成正比，用于后端服务器性能不均的情况。 例如： 

```
upstream server_pool{   
 server 192.168.5.21 weight=10;  
   server 192.168.5.22 weight=10;   
  }
```

**3、ip\_hash **

- 每个请求按访问 ip 的 hash 结果分配，这样每个访客固定访问一个后端服务器，可以解决 session 的问题。 例如：

 

```
upstream server_pool{    
    ip_hash;   
      server 192.168.5.21:80;  
       server 192.168.5.22:80;     } 
```

**4、fair（第三方） **

**按后端服务器的响应时间来分配请求，响应时间短的优先分配**

```
upstream server_pool{  
  server 192.168.5.21:80; 
    server 192.168.5.22:80;
     fair;  
   }
```

## 相关博文：

### [Nginx 简介与安装、常用的命令和配置文件](https://blog.csdn.net/heian_99/article/details/103264404)

## [nginx 配置实例-反向代理](https://blog.csdn.net/heian_99/article/details/103292763)

### [nginx 配置实例-负载均衡](https://blog.csdn.net/heian_99/article/details/103298249)

### [Nginx 配置实例-动静分离](https://blog.csdn.net/heian_99/article/details/103391378)

### [Nginx 配置高可用的集群](https://blog.csdn.net/heian_99/article/details/103391454)