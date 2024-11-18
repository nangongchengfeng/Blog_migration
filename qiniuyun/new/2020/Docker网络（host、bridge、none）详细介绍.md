---
author: 南宫乘风
categories:
- Docker
date: 2020-03-17 11:35:03
description: 网络、、我们会首先学习提供的几种原生网络，以及如何创建自定义网络；然后探讨容器之间如何通信，以及容器与外界如何交互。网络从覆盖范围可分为单个上的容器网络和跨多个的网络，本章重点讨论前一种。对于更为复杂。。。。。。。
image: http://image.ownit.top/4kdongman/52.jpg
tags:
- docker
- 通信
- 网络
- host
- bridge
title: Docker网络（host、bridge、none）详细介绍
---

<!--more-->

# Docker网络（host、bridge、none）

**我们会首先学习Docker提供的几种原生网络，以及如何创建自定义网络；然后探讨容器之间如何通信，以及容器与外界如何交互。**

 Docker网络从覆盖范围可分为单个host上的容器网络和跨多个host的网络，本章重点讨论前一种。对于更为复杂的多host容器网络，我们会在后面进阶技术章节单独讨论。

  
Docker 安装时会自动在host 上创建三个网络，我们可用**docker network ls**命令查看

```bash
docker network ls
```

![](http://image.ownit.top/csdn/20200317094903719.png)

## none网络

**顾名思义，none网络就是什么都没有的网络。挂在这个网络下的容器除了1o，没有其他任何网卡。容器创建时，可以通过-network=none指定使用none网络，如图**

```bash
docker run -it --network=none busybox
```

![](http://image.ownit.top/csdn/20200317095403385.png)

**我们不禁会问，这样一个封闭的网络有什么用呢？**

>   
> 其实还真有应用场景。封闭意味着隔离，一些对安全性要求高并且不需要联网的应用可以使用none网络。  
> 比如某个容器的唯一用途是生成随机密码，就可以放到none网络中避免密码被窃取。
> 
>   
> **当然大部分容器是需要网络的，我们接着看host网络。**

 

## host网络

**连接到host网络的容器共享Docker host的网络栈，容器的网络配置与host完全一样。**  
**可以通过-network-host 指定使用host网络**

```bash
docker run -it --network=host busybox
```

![](http://image.ownit.top/csdn/2020031709570833.png)

![](http://image.ownit.top/csdn/20200317100148893.png)

### **在容器中可以看到host的所有网卡，并且连hostmame 也是host的。host网络的使用场景又是什么呢？**

直接使用Docker host的网络最大的好处就是性能，如果容器对网络传输效率有较高要求，则可以选择host网络。当然不便之处就是牺牲一些灵活性，比如要**考虑端口冲突问题**，Docker host 上**已经使用的端口就不能再用**了。  
**Docker host的另一个用途是让容器可以直接配置host网路，比如某些跨host的网络解决方案，其本身也是以容器方式运行的，这些方案需要对网络进行配置，比如管理iptables**  
 

## bridge网络

**Docker安装时会创建一个命名为docker0的Linux bridge。如果不指定-network，创建的容器默认都会挂到docker0上**

```bash
brctl show
```

![](http://image.ownit.top/csdn/20200317100442883.png)

当前docker0上没有任何其他网络设备，我们创建一个容器看看有什么变化

![](http://image.ownit.top/csdn/20200317100641383.png)

**一个新的网络接口vethb56e98c被挂到了docker0上，vethb56e98c就是新创建容器的虚拟网卡。**  
下面看一下容器的网络配置

![](http://image.ownit.top/csdn/20200317102259644.png)

![](http://image.ownit.top/csdn/20200317102355122.png)

**容器有一个网卡eth0\@if34，为什么不是vethb56e98c呢？**

实际上eth0\@if34 和veth28c57df 是一对veth pair。 veth pair 是一种成对出现的特殊网络设备，可以把它们想象成由一根虚拟网线连接起来的一对网卡， 网卡的一头\(eth0\@if34\) 在容器中，另一头\(veth28c57df\) 挂在网桥docker0 上，其效果就是将eth0\@if34 也挂在了docker0上。  
我们还看到eth0\@if34 已经配置了IP 172.17.0.2， 为什么是这个网段呢\?让我们通过**docker network inspect bridge**看- \-下bridge 网络的配置信息

![](http://image.ownit.top/csdn/20200317103035414.png)

原来bridge 网络配置的subnet 就是172.17.0.0/16, 并且网关是172.17.0.1. 这个网关在哪儿呢\?大概你已经猜出来了，就是docker0

![](http://image.ownit.top/csdn/20200317103118420.png)

**容器网络拓扑图**

![](http://image.ownit.top/csdn/20200317103137881.png)

**容器创建时，docker 会自动从172.17.0.0/16 中分配-个IP,这里16 位的掩码保证有足够多的IP可以供容器使用。**

## user-defined网络

除了none、host、bridge这三个自动创建的网络，用户也可以根据业务需要创建user-defined网络。  
Docker提供三种user-defined 网络驱动：bridge、overlay 和macvlan。overlay 和macvlan用于创建跨主机的网络

我们可通过bridge 驱动创建类似前面默认的bridge 网络

```bash
docker network create --driver bridge my_net
```

```bash
[root@kvm ~]# docker network create --driver bridge my_net
7428a4d14c67b44be3a7184a5a065303d3688b5b13883526989b7173af881170
[root@kvm ~]# brctl show
bridge name	bridge id		STP enabled	interfaces
br-7428a4d14c67		8000.024221339eb6	no		
docker0		8000.024280532eb0	no		veth6281a8d
virbr0		8000.52540015904b	yes		virbr0-nic
```

![](http://image.ownit.top/csdn/20200317104818355.png)

新增了一个网桥br-7428a4d14c67，这里7428a4d14c67正好是新建bridge网络my\_net的短id。执行**docker network inspect**查看一下my\_net的配置信息，

![](http://image.ownit.top/csdn/20200317104949890.png)

**这里172.18.0.0/16是Docker自动分配的IP网段。  
我们可以自己指定IP网段吗？  
答案是：可以。**

  
**只需在创建网段时指定--subnet和-gateway参数**

```
docker network create --driver bridge --subnet 172.22.16.0/24 --gateway 172.22.16.1 my_net2
```

![](http://image.ownit.top/csdn/20200317105333121.png)

这里我们创建了新的bridge网络my\_net2，网段为172.22.16.0/24，网关为172.22.16.1与前面一样，网关在my net2对应的网桥br-5d863e9778b6上

![](http://image.ownit.top/csdn/20200317105504416.png)

 

**容器要使用新的网络，需要在启动时通过--network指定**

```bash
docker run -it --network=my_net2 busybox
```

![](http://image.ownit.top/csdn/20200317105622853.png)

容器分配到的IP为172.22.16.20到目前为止，容器的IP都是docker自动从subnet中分配，我们能否指定一个静态IP呢？  
**答案是：可以，通过-p指定**

```bash
docker run -it --network=my_net2 --ip 172.22.16.8 busybox
```

![](http://image.ownit.top/csdn/20200317110228543.png)

### **好了，我们来看看当前docker host的网络拓扑结构**

![](http://image.ownit.top/csdn/20200317110738979.png)

两个busybox容器都挂在mynet2上，应该能够互通

![](http://image.ownit.top/csdn/20200317111158421.png)

![](http://image.ownit.top/csdn/20200317111230330.png)

**可见同一网络中的容器、网关之间都是可以通信的。**  
my\_net2与默认bridge网络能通信吗？  
从拓扑图可知，两个网络属于不同的网桥，应该不能通信，我们通过实验验证一下，让busybox容器ping 不同网段容器

 

![](http://image.ownit.top/csdn/20200317111500404.png)

确实 ping不通，符合预期。  
“等等！不同的网络如果加上路由应该就可以通信了吧？”我已经听到有读者在建议了这是一个非常非常好的想法。

确实，如果host上对每个网络都有一条路由，同时操作系统上打开了ip forwarding，host就成了一个路由器，挂接在不同网桥上的网络就能够相互通信。下面我们来看看docker host是否满足这些条件呢？  
 

ip r查看host上的路由表：

![](http://image.ownit.top/csdn/20200317111807344.png)

172.17.0.0/16和172.22.16.0/24两个网络的路由都定义好了。再看看ip forwarding：

```
[root@kvm ~]# sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```

ip forwarding也已经启用了。条件都满足，为什么不能通行呢？  
我们还得看看iptables：

```
iptavles-save

-A DOCKER-ISOLATION -i br-13ceb40bd8e8 -o docker0 -j DROP
-A DOCKER-ISOLATION -i docker0 -o br-13ceb40bd8e8 -j DROP
```

原因就在这里了：**iptables DROP掉了网桥dockero与br-13ceb40bd8e8之间双向的流量。**

**从规则的命名DOCKER-ISOLATION可知docker在设计上就是要隔离不同的netwrok**

那么接下来的问题是：怎样才能让busybox与httpd 通信呢？

  
**答案是：为httpd容器添加一块net\_my2的网卡。这个可以通过docker network connect命令实现，**

![](http://image.ownit.top/csdn/20200317112835177.png)

```bash
docker network connect my_net2 655643ea6894
```

我们在docker0网段器中查看一下网络配置

![](http://image.ownit.top/csdn/20200317113019172.png)

容器中增加了一个网卡ethl，分配了my\_net2的IP 172.22.16.3。现在busybox应该能够访问docker0网段了，验证一下

![](http://image.ownit.top/csdn/20200317113317665.png)

busybox能够ping到httpd，并且可以访问httpd的Web服务所示。

（因为这里我在docker0网段，用busybox代替的httpd）

 

![](http://image.ownit.top/csdn/20200317113409925.png)

学习了Docker各种类型网络之后，接下来我们讨论容器与容器、容器与外界的连通问题