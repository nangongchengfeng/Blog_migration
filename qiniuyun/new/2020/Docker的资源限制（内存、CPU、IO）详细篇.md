---
author: 南宫乘风
categories:
- Docker
date: 2020-03-16 17:43:53
description: 一个上会运行若干容器，每个容器都需要、内存和资源。对于、等虚拟化技术，用户可以控制分配多少、内存资源给每个虚拟机。对于容器，也提供了类似的机制避免某个容器因占用太多资源而影响其他容器乃至整个的性能。内。。。。。。。
image: http://image.ownit.top/4kdongman/28.jpg
tags:
- docker
- 内存
- 硬盘
- io
- 资源限制
title: Docker的资源限制（内存、CPU、IO）详细篇
---

<!--more-->

### **一个docker host. 上会运行若干容器，每个容器都需要CPU、内存和I0资源。对于KVM、VMware 等虚拟化技术，用户可以控制分配多少CPU、内存资源给每个虚拟机。对于容器，Docker 也提供了类似的机制避免某个容器因占用太多资源而影响其他容器乃至整个host  
的性能。**  
 

# 内存限额

与操作系统类似，容器可以使用的内存包括两部分：物理内存和Swap。

Docker通过下面两组参数来控制容器内存的使用量

（1）-m 或 \--memory ：设置内存的使用限额，例如100MB，2GB

（2）--memory-swap：设置内存+swawp的使用限额

 

当我们执行如下的命令时

```bash
docker run -m 200M --memory-swap=300M ubuntu
```

其含义是允许该容器最多使用200MB的内存和100MB 的swap。默认情况下，上面两组参数为-1, 即对容器内存和swap的使用没有限制。

下面我们将使用progrium/stress 镜像来学习如何为容器分配内存。该镜像可用于对容器执行压力测试。执行如下命令:  
 

```bash
docker run -it -m 200M --memory-swap=300M progrium/stress --vm 1 --vm-bytes 208M
```

- \--vm1:启动1个内存工作线程。
- \--vm-bytes 280M:每个线程分配280MB内存。

 

**运行如下图结果**

![](http://image.ownit.top/csdn/2020031616300042.png)

因为280MB在可分配的范围\(300MB\) 内，所以工作线程能够正常工作，其过程是:  
\(1\)分配280MB内存。  
\(2\)释放280MB内存。  
\(3\)再分配280MB内存。  
\(4\)再释放280MB内存。  
\(5\)一-直循环.....  
如果让工作线程分配的内存超过300MB,结果如图

```bash
docker run -it -m 200M --memory-swap=300M progrium/stress --vm 1 --vm-bytes 310M
```

![](http://image.ownit.top/csdn/20200316165917983.png)

分配的内存超过限额，stress 线程报错，容器退出。  
如果在启动容器时只指定-m而不指定-memoryswap, 那么-memory-swap 默认为-m的两倍，比如:  
 

```
docker run -it -m 200M ubuntu
```

容器最多使用200M绒里内存和200swap

## CPU限额

**默认设置下，所有容器可以平等地使用host CPU资源并且没有限制**。

  
**Docker可以通过-c或-pu-shares设置容器使用CPU的权重。如果不指定，默认值为1024。**  
与内存限额不同，通过-c设置的cpu share 并不是CPU资源的绝对数量，而是一个相对的权重值。某个容器最终能分配到的CPU资源取决于它的cpu share占所有容器cpu share总和的比例。  
换句话说:通过cpu share可以设置容器使用CPU的优先级。

比如在host中启动了两个容器:

```bash
docker run --name "cont_A" -c 1024 ubuntu docker run --name "cont_B" -c 512 ubuntu
```

**containerA的cpu share 1024， 是containerB 的两倍。当两个容器都需要CPU资源时，containerA可以得到的CPU是containerB 的两倍。  
需要特别注意的是，这种按权重分配CPU只会发生在CPU资源紧张的情况下。如果containerA处于空闲状态，这时，为了充分利用CPU资源，containerB 也可以分配到全部可用的CPU.**

  
下面我们继续用progrium/stress 做实验。

###   
\(1\)启动\(container\_ A, cpu share为1024  
 

```bash
docker run --name "cont_A" -it -c 1024  progrium/stress --cpu 1
```

![](http://image.ownit.top/csdn/20200316170953506.png)

\--cpu用来设置工作线程的数量。因为当前host 只有1颗CPU,所以一个工作线程就能将CPU压满。如果host有多颗CPU,则需要相应增加--cpu的数量。  
 

### \(2\)启动\(container\_B, cpu share为512

```bash
docker run --name "cont_B" -it -c 512  progrium/stress --cpu 1
```

![](http://image.ownit.top/csdn/20200316171149233.png)

### \(3\)在host中执行top, 查看容器对CPU的使用情况，  
 

![](http://image.ownit.top/csdn/20200316171249683.png)

```bash
ps aux|head -1;ps aux|sort -k3nr |head -4
```

![](http://image.ownit.top/csdn/20200316171752731.png)

### **containerA消耗的CPU是containerB 的两倍。**  
 

### \(4\)现在暂停container. A

### ![](http://image.ownit.top/csdn/20200316172530957.png)

### \(5\) top 显示containerB在containerA空闲的情况下能够用满整颗CPU

### ![](http://image.ownit.top/csdn/20200316172546902.png)

# Block IO 带宽限额

Block 10是另一种可以限制容器使用的资源。Block I0指的是磁盘的读写，docker 可通过设置权重、限制bps和iops 的方式控制容器读写磁盘的带宽，下 面分别讨论。  
**注:目前Block I0限额只对direct IO \(不使用文件缓存\)有效。**  
Block IO权重  
默认情况下，所有容器能平等地读写磁盘，可以通过设置**\-blkio-weight**参数来改变容器block Io的优先级。  
**\-blkio-weight**与--cpu-shares 类似，设置的是相对权重值，默认为500。 在下面的例子中，containerA 读写磁盘的带宽是containerB 的两倍。

```bash
docker run -it --name cont_A --blkip-weight 600 ubuntu
docker run -it --name cont_B --blkip-weight 300 ubuntu
```

### 限制bps和iops

bps是 byte per second ，每秒读写的数量

iops是 io per second ，每秒IO的次数

可以同过下面的参数控制容器的bps和iops；

- \--device-read-bps:限制读某个设备的bps.
- \--devce-write-bps:限制写某个设备的bps.
- \--device- read-iops:限制读某个设备的iops.
- \--device-write-iops: 限制写某个设备的iops。  
 

下面这个例子限制容器写/dev/sda 的速率为30 MB/s:  
 

```bash
[root@kvm ~]# docker run -it --device-write-bps /dev/sda:30MB ubuntu
root@10845a98036e:/# time dd if=/dev/zero of=test.out bs=1M count=800 oflag=direct
800+0 records in
800+0 records out
838860800 bytes (839 MB, 800 MiB) copied, 26.6211 s, 31.5 MB/s

real	0m26.623s
user	0m0.000s
sys	0m0.106s
root@10845a98036e:/# 
```

```bash
docker run -it --device-write-bps /dev/sda:30MB ubuntu
```

**有限制**

![](http://image.ownit.top/csdn/2020031617393618.png)

**没有限制**

![](http://image.ownit.top/csdn/20200316174047490.png)

通过dd测试在容器中写磁盘的速度。因为容器的文件系统是在host /dev/sda. 上的，在容器中写文件相当于对host /dev/sda 进行写操作。另外，oflag= \-direct指定用direct I0方式写文件，这样--device-write-bps才能生效。  
 

看到，没有限速的话，速度很快，

其他参数，大家也可以试试