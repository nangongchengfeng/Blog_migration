---
author: 南宫乘风
categories:
- Docker
date: 2020-03-18 14:47:52
description: 通信从前面的例子可以得出这样一个结论：两个容器要能通信，必须要有属于同一个网络的网卡。满足这个条件后，容器就可以通过交互了。具体做法是在容器创建时通过指定相应的网络，或者通过将现有容器加入到指定网络。。。。。。。。
image: http://image.ownit.top/4kdongman/21.jpg
tags:
- 技术记录
title: Docker容器间通信
---

<!--more-->

## IP通信

从前面的例子可以得出这样一个结论：两个容器要能通信，必须要有属于同一个网络的网卡。满足这个条件后，容器就可以通过IP交互了。具体做法是在容器创建时通过-network指定相应的网络，或者通过docker network connect将现有容器加入到指定网络。可参考上一节

**[Docker网络（host、bridge、none）详细介绍](https://blog.csdn.net/heian_99/article/details/104914945)**

## Docker DNS Server

通过IP访问容器虽然满足了通信的需求，但还是不够灵活。因为在部署应用之前可能无法确定IP，部署之后再指定要访问的IP会比较麻烦。对于这个问题，可以通过docker自带的DNS服务解决。

**从Docker 1.10版本开始，docker daemon实现了一个内嵌的DNS server，使容器可以直接1通过“容器名”通信。方法很简单，只要在启动时用-name为容器命名就可以了。**

```bash
docker run -it --network=my_net2 --name=bbox1 busybox 
docker run -it --network=my_net2 --name=bbox2 busybox
```

**然后，bbox2就可以直接ping到bbox1了**

![](http://image.ownit.top/csdn/20200318144200839.png)

使用docker DNS有个限制：只能在user-defined网络中使用。也就是说，默认的bridge网络是无法使用DNS的。

下面验证一下：**创建bbox3和bbox4，均连接到bridge网络。**

```bash
docker run -it --name=bbox3 busybox 
docker run -it --name=bbox4 busybox
```

**bbox4无法ping到bbox3**

![](http://image.ownit.top/csdn/20200318144318852.png)

 

## Joined容器

joined容器非常特别，它可以使两个或多个容器共享一个网络栈，共享网卡和配置信息，joined容器之间可以通过127.0.01直接通信。

请看下面的例子：**先创建一个httpd容器，名字为web1。**

```bash
docker run -d -it --name=web1 =httpd
```

然后创建busybox容器并通过-network-container:webl指定joined容器为webl，

```bash
docker run -it --network=container:web1 busybox
```

![](http://image.ownit.top/csdn/20200318144541356.png)

 

请注意busybox器中网配置息，下面我们查看一下webl的网络，

![](http://image.ownit.top/csdn/20200318144601257.png)

看！busybox和webl的网卡mac地址与IP完全一样，它们共享了相同的网络栈。  
**busybox可以直接用127.0.0.1访问webl的http服务**

![](http://image.ownit.top/csdn/20200318144619828.png)

### joined容器非常适合以下场景：

1.  不同容器中的程序希望通过loopback高效快速地通信，比如web Server与App Server.
2.  希望监控其他容器的网络流量，比如运行在独立容器中的网络监控程序。