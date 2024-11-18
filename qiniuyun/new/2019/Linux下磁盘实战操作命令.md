---
author: 南宫乘风
categories:
- Linux基础
date: 2019-12-16 23:48:41
description: 企业真实场景由于硬盘常年大量读写，经常会出现坏盘，需要更换硬盘。或者由于磁盘空间不足，需添加新硬盘，新添加的硬盘需要经过格式化、分区才能被系统所使用。虚拟机模拟真实服务器添加一块新硬盘，不需要关机，直。。。。。。。
image: http://image.ownit.top/4kdongman/53.jpg
tags:
- 磁盘
- 挂载
title: Linux下磁盘实战操作命令
---

<!--more-->

      企业真实场景由于硬盘常年大量读写，经常会出现坏盘，需要更换硬盘。或者由于磁盘空间不足，需添加新硬盘，新添加的硬盘需要经过格式化、分区才能被 Linux 系统所使用。

         虚拟机 CentOS 7 Linux 模拟DELL R730 真实服务器添加一块新硬盘，不需要关机，直接插入用硬盘即可，一般硬盘均支持热插拔功能。企业中添加新硬盘的操作流程如下：

（1） 检测Linux系统识别的硬盘设备，新添加硬盘被识别为/dev/sdb，如果有多块硬盘，会依次识别成/dev/sdc、/dev/sdd 等设备名称

```
fdisk -l
```

  
![](http://image.ownit.top/csdn/20191216205706409.png)

（2） 基于新硬盘/dev/sdb设备，创建磁盘分区/dev/sdb1

```
fdisk /dev/sdb
```

![](http://image.ownit.top/csdn/20191216230722943.png)

（3） fdisk 分区命令参数如下，常用参数包括m、n、p、e、d、w。  
![](http://image.ownit.top/csdn/20191216230850786.png)

![](http://image.ownit.top/csdn/20191216233226648.png)

（4） 创建/dev/sdb1 分区方法，fdisk /dev/sdb，然后按 n-p-1-Enter 键+20G-Enter 键-w，最后执行 fdisk –l|tail \-10

![](http://image.ownit.top/csdn/20191216233448579.png)

（5） mkfs.ext4 /dev/sdb1 格式化磁盘分区

```
mkfs.ext4 /dev/sdb1
```

![](http://image.ownit.top/csdn/20191216233552574.png)

（6） /dev/sdb1 分区格式化，使用mount 命令挂载到/data/目录

1.  mkdir -p /data/ 创建/data/数据目录
2.  mount /dev/sdb1 /data 挂载/dev/sdb1 分区至/data/目录
3.  df -h 查看磁盘分区详情
4.  echo "mount /dev/sdb1 /data" >>/etc/rc.local 将 挂 载 分 区 命 令 加 入/etc/rc.local 开机启动

![](http://image.ownit.top/csdn/20191216233917643.png)

（7） 自动挂载分区除了可以加入到/etc/rc.local 开机启动之外，还可以加入到/etc/fstab文件中

- /dev/sdb1 /data/ ext4 defaults  0 0
- mount -o rw,remount / 重新挂载/系统，检测/etc/fstab 是否有误

![](http://image.ownit.top/csdn/20191216234434499.png)

![](http://image.ownit.top/csdn/20191216234810535.png)