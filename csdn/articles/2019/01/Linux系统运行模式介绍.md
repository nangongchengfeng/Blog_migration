+++
author = "南宫乘风"
title = "Linux系统运行模式介绍"
date = "2019-01-31 20:50:49"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/83.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86725989](https://blog.csdn.net/heian_99/article/details/86725989)

Linux运行模式
-          自由服务，即不需要用户独立去安装的软件服务，而是在系统安装好之后就可以直接使用的服务（内置服务）。-          运行模式也称为运行级别，属于linux的自有服务。-          运行模式可以理解为一旦你开机了，计算机就以你设置的运行模式给你展示。-          控制运行模式的进程是：init   ，初始化进程，进程id是1。
Centos 7系统运行方式（target）：

        multi—user.target  字符模式（多用户模式）<br>         graphical.target    图像模式<br>         <br> （1）查看当前的默认级别：

```
[root@wei ~]# systemctl get-default
multi-user.target
```

（2）修改默认级别

```
[root@wei ~]# systemctl get-default graphical.target
```

        

Centos 6系统运行方式：<br>       <br>       0    关机模式<br>       1    单用户模式（修复）<br>       2    字符模式（无网络）<br>       3    完全字符模式（黑底白字）<br>       4    预留<br>       5    图形模式<br>       6    重启模式 <br>       <br> 查看当前的默认级别

```
[root@wei ~]# runlevel 
N 3
      
```

<br>       <br>       <br> init id 可以来回切换模式<br> 编辑文件/etc/inittab修改默认的启动模式

<br>  <br>       

<br>  
