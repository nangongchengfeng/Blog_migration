---
author: 南宫乘风
categories:
- 技术记录
date: 2019-10-26 09:50:55
description: 目录安装步骤、查看的版本、安装、安装、启动、设置为开启启动、查看安装信息、使用中国加速器、使用中国加速器安装步骤安装操作系统，最小化安装禁用修改文件，将改为，重启机器即可、查看的版本、安装、启动、设置。。。。。。。
image: http://image.ownit.top/4kdongman/72.jpg
tags:
- 技术记录
title: CentOS 7上安装Docker
---

<!--more-->

**目录**

 

[安装步骤](#%E5%AE%89%E8%A3%85%E6%AD%A5%E9%AA%A4)

[1、查看Docker的版本](#1%E3%80%81%E6%9F%A5%E7%9C%8BDocker%E7%9A%84%E7%89%88%E6%9C%AC)

[​](#%E2%80%8B)

[2、安装 Docker](<#2、安装 Docker>)

[3、启动Docker](#3%E3%80%81%E5%90%AF%E5%8A%A8Docker)

[4、设置为开启启动](#4%E3%80%81%E8%AE%BE%E7%BD%AE%E4%B8%BA%E5%BC%80%E5%90%AF%E5%90%AF%E5%8A%A8)

[5、查看Docker安装信息](#5%E3%80%81%E6%9F%A5%E7%9C%8BDocker%E5%AE%89%E8%A3%85%E4%BF%A1%E6%81%AF)

[6、使用Docker 中国加速器](<#6、使用Docker 中国加速器>)

---

## 安装步骤

安装操作系统，最小化安装（mini）

禁用Selinux, 修改/etc/selinux/config 文件，将SELINUX=enforcing改为SELINUX=disabled，重启机器即可

## 1、查看Docker的版本

```
[root@wei ~]# yum list docker
```

## ![](http://image.ownit.top/csdn/20191026094216908.png)

## 2、安装 Docker

```
[root@wei ~]# yum install -y docker
```

![](http://image.ownit.top/csdn/20191026094413199.png)

## 3、启动Docker

```bash
[root@wei ~]# systemctl start docker
```

## 4、设置为开启启动

```bash
[root@wei ~]# systemctl enable docker
```

## 5、查看Docker安装信息

```bash
[root@wei ~]# docker version
```

![](http://image.ownit.top/csdn/20191026094834789.png)

## 6、使用Docker 中国加速器

由于网络原因，我们在pull Image 的时候，从Docker Hub上下载会很慢。

修改文件

```
vi  /etc/docker/daemon.json
#添加后：
{
    "registry-mirrors": ["https://registry.docker-cn.com"],
    "live-restore": true
}
```

重起docker服务

```
systemctl restart docker
```