---
author: 南宫乘风
categories:
- Docker
date: 2019-12-12 10:19:06
description: 目录是什么联合文件系统镜像加载原理分层的镜像为什么镜像要采用这种分层结构呢为什么镜像要采用这种分层结构呢特点镜像操作补充案例演示、从上下载镜像到本地并成功运行、故意删除上一步镜像生产容器的文档、一个没。。。。。。。
image: ../../title_pic/04.jpg
slug: '201912121019'
tags:
- docker
- 镜像
- 命令
- centos
title: Docker 镜像介绍和命令
---

<!--more-->

**目录**

 

[是什么](#%E6%98%AF%E4%BB%80%E4%B9%88)

[UnionFS（联合文件系统）](#UnionFS%EF%BC%88%E8%81%94%E5%90%88%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%EF%BC%89)

[ Docker镜像加载原理](#%C2%A0Docker%E9%95%9C%E5%83%8F%E5%8A%A0%E8%BD%BD%E5%8E%9F%E7%90%86)

[分层的镜像](#%E5%88%86%E5%B1%82%E7%9A%84%E9%95%9C%E5%83%8F)

[为什么 Docker 镜像要采用这种分层结构呢](<#为什么 Docker 镜像要采用这种分层结构呢>)

[特点](#%E7%89%B9%E7%82%B9)

[Docker镜像commit操作补充](#Docker%E9%95%9C%E5%83%8Fcommit%E6%93%8D%E4%BD%9C%E8%A1%A5%E5%85%85)

[案例演示](#%E6%A1%88%E4%BE%8B%E6%BC%94%E7%A4%BA)

[1、从Hub上下载tomcat镜像到本地并成功运行](#1%E3%80%81%E4%BB%8EHub%E4%B8%8A%E4%B8%8B%E8%BD%BDtomcat%E9%95%9C%E5%83%8F%E5%88%B0%E6%9C%AC%E5%9C%B0%E5%B9%B6%E6%88%90%E5%8A%9F%E8%BF%90%E8%A1%8C)

[2、故意删除上一步镜像生产tomcat容器的文档](#2%E3%80%81%E6%95%85%E6%84%8F%E5%88%A0%E9%99%A4%E4%B8%8A%E4%B8%80%E6%AD%A5%E9%95%9C%E5%83%8F%E7%94%9F%E4%BA%A7tomcat%E5%AE%B9%E5%99%A8%E7%9A%84%E6%96%87%E6%A1%A3)

[3、commit一个没有doc的tomcat新镜像](#3%E3%80%81commit%E4%B8%80%E4%B8%AA%E6%B2%A1%E6%9C%89doc%E7%9A%84tomcat%E6%96%B0%E9%95%9C%E5%83%8F)

[4.启动我们的新镜像并和原来的对比](#4.%E5%90%AF%E5%8A%A8%E6%88%91%E4%BB%AC%E7%9A%84%E6%96%B0%E9%95%9C%E5%83%8F%E5%B9%B6%E5%92%8C%E5%8E%9F%E6%9D%A5%E7%9A%84%E5%AF%B9%E6%AF%94)

---

# 是什么

镜像是一种轻量级、可执行的独立软件包，用来打包软件运行环境和基于运行环境开发的软件，它包含运行某个软件所需的所有内容，包括代码、运行时、库、环境变量和配置文件。

## UnionFS（联合文件系统）

UnionFS（联合文件系统）：Union文件系统（UnionFS）是一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下\(unite several directories into a single virtual filesystem\)。Union 文件系统是 Docker 镜像的基础。镜像可以通过分层来进行继承，基于基础镜像（没有父镜像），可以制作各种具体的应用镜像。

![](../../image/20191210151957847.png)

特性：一次同时加载多个文件系统，但从外面看起来，只能看到一个文件系统，联合加载会把各层文件系统叠加起来，这样最终的文件系统会包含所有底层的文件和目录

##  Docker镜像加载原理

docker的镜像实际上由一层一层的文件系统组成，这种层级的文件系统UnionFS。

bootfs\(boot file system\)主要包含bootloader和kernel, bootloader主要是引导加载kernel, Linux刚启动时会加载bootfs文件系统，在Docker镜像的最底层是bootfs。这一层与我们典型的Linux/Unix系统是一样的，包含boot加载器和内核。当boot加载完成之后整个内核就都在内存中了，此时内存的使用权已由bootfs转交给内核，此时系统也会卸载bootfs。

rootfs \(root file system\) ，在bootfs之上。包含的就是典型 Linux 系统中的 /dev, /proc, /bin, /etc 等标准目录和文件。rootfs就是各种不同的操作系统发行版，比如Ubuntu，Centos等等。

![](../../image/20191210152138263.png)

** 平时我们安装进虚拟机的CentOS都是好几个G，为什么docker这里才200M？？**

![](../../image/20191210152231510.png)

## 分层的镜像

以我们的pull为例，在下载的过程中我们可以看到docker的镜像好像是在一层一层的在下载

![](../../image/2019121015252170.png)

## 为什么 Docker 镜像要采用这种分层结构呢

最大的一个好处就是 \- 共享资源

 比如：有多个镜像都从相同的 base 镜像构建而来，那么宿主机只需在磁盘上保存一份base镜像，

同时内存中也只需加载一份 base 镜像，就可以为所有容器服务了。而且镜像的每一层都可以被共享。

# **特点**

Docker镜像都是只读的  
当容器启动时，一个新的可写层被加载到镜像的顶部。  
这一层通常被称作“容器层”，“容器层”之下的都叫“镜像层”。

# Docker镜像commit操作补充

 

docker commit提交容器副本使之成为一个新的镜像

 

docker commit \-m=“提交的描述信息” \-a=“作者” 容器ID 要创建的目标镜像名:\[标签名\]

 

## 案例演示

### 1、从Hub上下载tomcat镜像到本地并成功运行

 

**\-p 主机端口:docker容器端口【指定端口】**

```
docker run -it -p 8080:8080 tomcat
```

![](../../image/20191210160132315.png)

**\-P 随机分配端口**

```
docker run -it -P tomcat
```

![](../../image/20191212094736722.png)

**i:交互**

**t:终端**

 

### 2、故意删除上一步镜像生产tomcat容器的文档

![](../../image/20191212095237947.png)

![](../../image/20191212095755453.png)

![](../../image/20191212095823276.png)

### 3、commit一个没有doc的tomcat新镜像

**也即当前的tomcat运行实例是一个没有文档内容的容器，  
以它为模板commit一个没有doc的tomcat新镜像heian/tomcat02**

```
docker commit -a "wei" -m "del tomcat docs" 63982bc3e2d9 heian/mytomcat:1.2
```

![](../../image/20191212101021935.png)

### 4.启动我们的新镜像并和原来的对比

**启动heian/tomcat02，它没有docs**

```
docker run -it -p 7777:8080 heian/mytomcat:1.2 
```

![](../../image/2019121210170761.png)

**新启动原来的tomcat，它有docs**

![](../../image/20191212095237947.png)