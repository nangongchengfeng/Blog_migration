---
author: 南宫乘风
categories:
- Docker
date: 2020-03-20 16:38:14
description: 网络、、详细介绍容器间通信前面我们已经解决了容器间通信的问题，接下来讨论容器如何与外部世界通信。这里涉及两个方向：容器访问外部世界。外部世界访问容器。容器访问外部世界在我们当前的实验环境下，是可以访问。。。。。。。
image: ../../title_pic/65.jpg
slug: '202003201638'
tags:
- docker
- 网络
- 通信
- 容器
title: Docker容器访问外部世界
---

<!--more-->

# [Docker网络（host、bridge、none）详细介绍](https://blog.csdn.net/heian_99/article/details/104914945)

# [Docker容器间通信](https://blog.csdn.net/heian_99/article/details/104944575)

前面我们已经解决了容器间通信的问题，接下来讨论容器如何与外部世界通信。

这里涉及两个方向：

（1）容器访问外部世界。

（2）外部世界访问容器。

## 容器访问外部世界

在我们当前的实验环境下，docker host是可以访问外网的

![](../../image/20200320161023549.png)

我们看一下容器是否也能访问外网呢？

![](../../image/20200320161151610.png)

**可见，容器默认就能访问外网。**  
**请注意：这里外网指的是容器网络以外的网络环境，并非特指Internet.**

> 现象很简单，但更重要的：我们应该理解现象下的本质。
> 
>   
> 在上面的例子中，busybox位于dockero这个私有bridge网络中（172.17.0.0/16），当busybox从容器向外ping时，数据包是怎样到达bing.com的呢？
> 
>   
> **这里的关键就是NAT，我们查看一下docker host上的iptables规则**

![](../../image/20200320161357178.png)

### 在NAT表中，有这么一条规则：

```bash
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
```

**其含义是：如果网桥docker0收到来自172.17.0.0/16网段的外出包，把它交给MASQUERADE处理。而且MASQUERADE的处理方式是将**

**包的原地址替换成host的地址发送出去，机 做了一次网络地址转换（NAT）**

---

**下面我们通过tcpdump查看地址是如何转换的。先查看docker host的路由表**

![](../../image/20200320161827561.png)

默认路由通过ens192发出去，所以我们同时要监控ens192和docker0上的icmp（ping）的数据包。

当busybox ping www.baidu.com时，tcpdumo输出如下

```bash
tcpdump -i docker0 -n icmp
```

![](../../image/20200320162226557.png)

docker0收到busybox的ping包，源地址为容器的IP：172.17.0.2，这没问题，交给MASQUERADE处理。这时，在看ens192的变化。

![](../../image/2020032016253616.png)

ping包的源地址变成ens192的192.168.1.100

这就是iptables的NAT规则的处理结果，从而保证数据包能够到达外网。

下面这张图来说明结果。

![](../../image/20200320162712634.png)

> - （1）busybox发送ping包：172.17.0.2 > www.bing.com。
> - （2）dockero收到包，发现是发送到外网的，交给NAT处理。
> - （3）NAT将源地址换成ens192的IP：10.0.2.15 >www.bing.com.
> - （4）ping从 ens192出去，达www.bing.como

## 通过NAT，docker实现了容器对外网的访问。

 

## 外部世界访问容器

**下面我们来讨论另一个方向：外网如何访问到容器？**  
**答案是：端口映射。**

  
**docker可将容器对外提供服务的端口映射到host的某个端口，外网通过该端口访问容器。容器启动时通过-p参数映射端口**

```bash
[root@kvm ~]# docker run -d -p 80 httpd
6b89d7e3f47a425256af6934689c0009fbbad9099bf31c2e6148a6cb236a9655
[root@kvm ~]# docker ps
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS                   NAMES
6b89d7e3f47a        httpd               "httpd-foreground"   5 seconds ago       Up 2 seconds        0.0.0.0:32768->80/tcp   stoic_bartik
78de9710bce0        busybox             "sh"                 19 minutes ago      Up 19 minutes                               hei
[root@kvm ~]# docker port 6b89d7e3f47a
80/tcp -> 0.0.0.0:32768
```

![](../../image/20200320163142538.png)

**容器启动后，可通过docker ps或者docker port查看到host映射的端口。在上面的例子中，httpd容器的80端口被映射到host 32768上，这样就可以通过\<host ip>：\<32773>访问容器的Web服务了**

![](../../image/20200320163253965.png)

**除了映射动态端口，也可在-p中指定映射到host某个特定端口，例如可将80端口映射到host的8080端口**

```bash
[root@kvm ~]# docker run -d -p 8080:80 httpd
8d7db7b2c7a6fc03cd219d6d3c07f15261d8a12efda3be25fdb60576c91c1a7e
[root@kvm ~]# curl 192.168.1.100:8080
<html><body><h1>It works!</h1></body></html>
[root@kvm ~]# 
```

![](../../image/20200320163433687.png)

**每一个映射的端口，host都会启动一个docker-proxy进程来处理访问容器的流量。**

![](../../image/20200320163639265.png)

### 以0.0.0.0：32773-280/tcp为例分析整个过程

![](../../image/2020032016370255.png)

> - （1）docker-proxy监听host的32773端口。
> - （2）当curl访问10.0.2.15：32773时，docker-proxy转发给容器172.170.2：80。
> - （3）httpd容器响应请求并返回结果。