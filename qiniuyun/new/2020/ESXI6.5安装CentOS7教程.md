---
author: 南宫乘风
categories:
- Linux实战操作
date: 2020-03-16 09:59:18
description: 三个版本：单机级，用在个人桌面系统中，需要操作系统支持：工作组级，用于服务器，需要操作系统支持：企业级，用于服务器，不需要操作系统支持是一款虚拟化系统，与，不同，它不需要安装在其他操作系统上，直接运行。。。。。。。
image: http://image.ownit.top/4kdongman/81.jpg
tags:
- esxi
- centos7
- Linux
title: ESXI6.5安装CentOS7教程
---

<!--more-->

VMware三个版本

workstation： 单机级，用在个人桌面系统中，需要操作系统支持

servier：工作组级，用于服务器，需要操作系统支持

esxi：企业级，用于服务器，不需要操作系统支持

Exsi 是一款虚拟化系统，与VMware，VirtualBox不同，它不需要安装在其他操作系统上，直接运行在裸机上；占用系统资源很小，易于管理，所以被大多数中小型公司所使用；

### 安装图解：

镜像已上传到服务器，CentOS7镜像包

![](http://image.ownit.top/csdn/20200316094044629.png)

新建虚拟机

![](http://image.ownit.top/csdn/20200316094121259.png)

![](http://image.ownit.top/csdn/2020031609421728.png)

选择存储

![](http://image.ownit.top/csdn/20200316094300587.png)

自定义设置

![](http://image.ownit.top/csdn/20200316094537426.png)

![](http://image.ownit.top/csdn/20200316094607941.png)

如果配置不够，可进行修改

![](http://image.ownit.top/csdn/20200316094645722.png)

将镜像加载到新建的虚拟机里，CD/DVD驱动器选择数据存储ISO文件

![](http://image.ownit.top/csdn/20200316094723876.png)

![](http://image.ownit.top/csdn/20200316094747276.png)

现在开始运行，首先打开电源,打开控制台

![](http://image.ownit.top/csdn/20200316094819324.png)

![](http://image.ownit.top/csdn/2020031609501224.png)

下面步骤就可安装Centos7一样了。

选择自己需求的东西就行，然后开始安装。