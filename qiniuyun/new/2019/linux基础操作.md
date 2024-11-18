---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-02 16:59:18
description: 近期要入坑运维，在此交流自己的技术和心得。开始自己博客的生涯。大神勿喷成功安装后的基础步骤软件：系统：安装成功的界面安装完毕后操作关闭防火墙当前关闭防火墙开机禁用防火墙禁用上面两串代码效果一样，只需要。。。。。。。
image: http://image.ownit.top/4kdongman/64.jpg
tags:
- linu
- 运
title: linux基础操作
---

<!--more-->

**近期要入坑linux运维，在此交流自己的技术和心得。开始自己博客的生涯。（大神勿喷）**

**成功安装CentOS7后的基础步骤**

**软件：Vmware Workstation**

**系统：CentOS7**

**![](http://image.ownit.top/csdn/2019010216493436.png)**

**安装成功的CentOS7界面**

**安装完毕后操作:**

**（1） 关闭防火墙**

```
	systemctl   stop  firewalld   # 当前关闭防火墙
	systemctl   disable  firewalld  # 开机禁用防火墙
```

**（2）禁用SELinux**

```
sed  -i.bak  ‘s/=enforcing/=disabled/’ /etc/selinux/config
```

```
sed  -i.bak  ‘s/=enforcing/=disabled/’ /etc/sysconfig/selinux
```

**上面两串代码效果一样，只需要运行一个即可**

**（3）  关机**

```
shutdown -h now
```

**（4）创建快照，避免重新安装**

**![](http://image.ownit.top/csdn/20190102165741149.png)**

**（6）安装远程管理软件Xmanager6**