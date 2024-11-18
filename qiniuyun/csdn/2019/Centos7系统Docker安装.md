---
author: 南宫乘风
categories:
- Docker
date: 2019-12-09 11:04:32
description: 目录前期说明安装步骤、官网中文安装参考手册、确定你是及以上版本、安装相关、卸载旧版本、安装需要的软件包、设置镜像仓库、更新软件包索引、安装、启动、测试、配置镜像加速、卸载底层原理、是怎么工作的、为什么。。。。。。。
image: ../../title_pic/54.jpg
slug: '201912091104'
tags:
- Docker
- 容器
- 安装
- Centos7
title: Centos7系统Docker安装
---

<!--more-->

**目录**

[前期说明](#%E5%89%8D%E6%9C%9F%E8%AF%B4%E6%98%8E)

[安装步骤](#%E5%AE%89%E8%A3%85%E6%AD%A5%E9%AA%A4)

[1、官网中文安装参考手册](#1%E3%80%81%E5%AE%98%E7%BD%91%E4%B8%AD%E6%96%87%E5%AE%89%E8%A3%85%E5%8F%82%E8%80%83%E6%89%8B%E5%86%8C)

[2、确定你是CentOS7及以上版本](#2%E3%80%81%E7%A1%AE%E5%AE%9A%E4%BD%A0%E6%98%AFCentOS7%E5%8F%8A%E4%BB%A5%E4%B8%8A%E7%89%88%E6%9C%AC)

[3、yum安装gcc相关](#3%E3%80%81yum%E5%AE%89%E8%A3%85gcc%E7%9B%B8%E5%85%B3)

[4、卸载旧版本](#4%E3%80%81%E5%8D%B8%E8%BD%BD%E6%97%A7%E7%89%88%E6%9C%AC)

[5、安装需要的软件包](#5%E3%80%81%E5%AE%89%E8%A3%85%E9%9C%80%E8%A6%81%E7%9A%84%E8%BD%AF%E4%BB%B6%E5%8C%85)

[6、设置stable镜像仓库](#6%E3%80%81%E8%AE%BE%E7%BD%AEstable%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)

[7、更新yum软件包索引](#7%E3%80%81%E6%9B%B4%E6%96%B0yum%E8%BD%AF%E4%BB%B6%E5%8C%85%E7%B4%A2%E5%BC%95)

[8、安装DOCKER-CE](#8%E3%80%81%E5%AE%89%E8%A3%85DOCKER-CE)

[9、启动docker](#9%E3%80%81%E5%90%AF%E5%8A%A8docker)

[10、测试](#10%E3%80%81%E6%B5%8B%E8%AF%95)

[11、配置镜像加速](#11%E3%80%81%E9%85%8D%E7%BD%AE%E9%95%9C%E5%83%8F%E5%8A%A0%E9%80%9F)

[12、卸载](#12%E3%80%81%E5%8D%B8%E8%BD%BD)

[底层原理](#%E5%BA%95%E5%B1%82%E5%8E%9F%E7%90%86)

[1、Docker是怎么工作的](#1%E3%80%81Docker%E6%98%AF%E6%80%8E%E4%B9%88%E5%B7%A5%E4%BD%9C%E7%9A%84)

[2、为什么Docker比较比VM快](#2%E3%80%81%E4%B8%BA%E4%BB%80%E4%B9%88Docker%E6%AF%94%E8%BE%83%E6%AF%94VM%E5%BF%AB)

---

# **前期说明**

**CentOS Docker 安装**

Docker支持以下的CentOS版本：

CentOS 7 \(64-bit\)

CentOS 6.5 \(64-bit\) 或更高的版本

**前提条件**

目前，CentOS 仅发行版本中的内核支持 Docker。

Docker 运行在 CentOS 7 上，要求系统为64位、系统内核版本为 3.10 以上。

Docker 运行在 CentOS-6.5 或更高的版本的 CentOS 上，要求系统为64位、系统内核版本为 2.6.32-431 或者更高版本。

**查看自己的内核**

uname命令用于打印当前系统相关信息（内核版本号、硬件架构、主机名称和操作系统类型等）。

![](../../image/2019120909053022.png)

查看已安装的CentOS版本信息（CentOS6.8有，CentOS7无该命令）

![](../../image/20191209090705982.png)

Centos7

![](../../image/20191209090645659.png)

 

![](../../image/20191209090811471.png)  
 

# 安装步骤

 

## 1、官网中文安装参考手册

<https://docs.docker.com/install/linux/docker-ce/centos/>

## 2、确定你是CentOS7及以上版本

![](../../image/20191209101910198.png)

## 3、yum安装gcc相关

**CentOS7能上外网**

![](../../image/20191209102025841.png)

```
yum -y install gcc
yum -y install gcc-c++
```

## 4、卸载旧版本

```
yum -y remove docker docker-common docker-selinux docker-engine
```

**2018.3官网版本**

```

yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

## 5、安装需要的软件包

```
yum install -y yum-utils device-mapper-persistent-data lvm2
```

## 6、设置stable镜像仓库

> **大坑**

```
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

**报错：**  
1   \[Errno 14\] curl#35 \- TCP connection reset by peer   
2   \[Errno 12\] curl#35 \- Timeout  
注意：因为这是Docker的官网的，是外国的，所以下载慢。

**解决：推荐使用阿里云源，或者网易的源**

> **推荐**

```
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

**注意**：**这里是阿里云的源，国内的，速度很快。**

![](../../image/20191209103234127.png)

## 7、更新yum软件包索引

```
yum makecache fast
```

![](../../image/20191209103332400.png)

### 8、安装DOCKER-CE

```
yum -y install docker-ce
```

## 9、启动docker

```
systemctl start docker
```

## 10、测试

```
docker version
```

![](../../image/20191209103717137.png)

```
docker run hello-world
```

![](../../image/20191209103821938.png)

## 11、配置镜像加速

1、创建目录（docker会自动创建）

```
mkdir -p /etc/docker
```

2、使用阿里云的加速地址

```
vim  /etc/docker/daemon.json
```

![](../../image/20191209104628821.png)

![](../../image/20191209104534262.png)

```
systemctl daemon-reload
```

3、重启Docker

```
systemctl restart docker
```

## 12、卸载

停止Docker

```
systemctl stop docker 
```

yum卸载Docker

```
yum -y remove docker-ce
```

rm删除Docker的目录

```
rm -rf /var/lib/docker
```

# 底层原理

## 1、Docker是怎么工作的

Docker是一个Client-Server结构的系统，Docker守护进程运行在主机上， 然后通过Socket连接从客户端访问，守护进程从客户端接受命令并管理运行在主机上的容器。 容器，是一个运行时环境，就是我们前面说到的集装箱。

![](../../image/20191209110025739.png)

## 2、为什么Docker比较比VM快

\(1\)docker有着比虚拟机更少的抽象层。由亍docker不需要Hypervisor实现硬件资源虚拟化,运行在docker容器上的程序直接使用的都是实际物理机的硬件资源。因此在CPU、内存利用率上docker将会在效率上有明显优势。

\(2\)docker利用的是宿主机的内核,而不需要Guest OS。因此,当新建一个容器时,docker不需要和虚拟机一样重新加载一个操作系统内核。仍而避免引寻、加载操作系统内核返个比较费时费资源的过程,当新建一个虚拟机时,虚拟机软件需要加载Guest OS,返个新建过程是分钟级别的。而docker由于直接利用宿主机的操作系统,则省略了返个过程,因此新建一个docker容器只需要几秒钟。

![](../../image/20191209110143217.png)

![](../../image/20191209110219865.png)