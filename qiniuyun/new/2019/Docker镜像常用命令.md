---
author: 南宫乘风
categories:
- Docker
date: 2019-12-09 17:24:35
description: 目录帮助命令镜像命令列出本地主机上的镜像某个镜像名字某个镜像名字某个镜像名字某个镜像名字删除镜像帮助命令镜像命令列出本地主机上的镜像各个选项说明：表示镜像的仓库源：镜像的标签：镜像：镜像创建时间：镜像。。。。。。。
image: http://image.ownit.top/4kdongman/63.jpg
tags:
- docker
- 镜像
- 命令
title: Docker镜像常用命令
---

<!--more-->

**目录**

[帮助命令](#%E5%B8%AE%E5%8A%A9%E5%91%BD%E4%BB%A4)

[镜像命令](#%E9%95%9C%E5%83%8F%E5%91%BD%E4%BB%A4)

[列出本地主机上的镜像](#%E5%88%97%E5%87%BA%E6%9C%AC%E5%9C%B0%E4%B8%BB%E6%9C%BA%E4%B8%8A%E7%9A%84%E9%95%9C%E5%83%8F)

[docker search 某个XXX镜像名字](<#docker search 某个XXX镜像名字>)

[docker pull 某个XXX镜像名字](<#docker pull 某个XXX镜像名字>)

[删除镜像](#%E5%88%A0%E9%99%A4%E9%95%9C%E5%83%8F)

---

## 帮助命令

```
docker version
```

![](http://image.ownit.top/csdn/20191209110618276.png)

```
docker info
```

![](http://image.ownit.top/csdn/20191209110738194.png)

```
docker --help
```

![](http://image.ownit.top/csdn/20191209110801845.png)

## 镜像命令

```
docker images
```

### 列出本地主机上的镜像

![](http://image.ownit.top/csdn/20191209111049708.png)

各个选项说明:

- REPOSITORY：表示镜像的仓库源
- TAG：镜像的标签
- IMAGE ID：镜像ID
- CREATED：镜像创建时间
- SIZE：镜像大小

 

- \-a :列出本地所有的镜像（含中间映像层）![](http://image.ownit.top/csdn/20191209111417319.png)
- \-q :只显示镜像ID。
- ![](http://image.ownit.top/csdn/20191209111645528.png)
- \--digests :显示镜像的摘要信息![](http://image.ownit.top/csdn/20191209111612839.png)
- \--no-trunc :显示完整的镜像信息![](http://image.ownit.top/csdn/20191209111840714.png)

同一仓库源可以有多个 TAG，代表这个仓库源的不同个版本，我们使用 REPOSITORY:TAG 来定义不同的镜像。

如果你不指定一个镜像的版本标签，例如你只使用 ubuntu，docker 将默认使用 ubuntu:latest 镜像

### docker search 某个XXX镜像名字

**网站**

<https://hub.docker.com>

**命令**

```
docker search [OPTIONS] 镜像名字
```

![](http://image.ownit.top/csdn/20191209112039202.png)

OPTIONS说明：

- \--no-trunc : 显示完整的镜像描述

![](http://image.ownit.top/csdn/20191209112556124.png)

- \-s : 列出收藏数不小于指定值的镜像。

![](http://image.ownit.top/csdn/2019120911251532.png)

- \--automated : 只列出 automated build类型的镜像；

![](http://image.ownit.top/csdn/20191209112647955.png)

## docker pull 某个XXX镜像名字

**下载镜像**

```
docker pull 镜像名字[:TAG]
```

![](http://image.ownit.top/csdn/20191209112916321.png)

```
docker  pull tomcat
```

![](http://image.ownit.top/csdn/20191209165858974.png)

![](http://image.ownit.top/csdn/20191209170037662.png)

## **删除镜像**

**docker rmi 某个XXX镜像名字ID**

> **删除单个**

```
docker rmi  -f 镜像ID
```

![](http://image.ownit.top/csdn/20191209170531976.png)

> **删除多个**

```
docker rmi -f 镜像名1:TAG 镜像名2:TAG 
```

```
docker rmi -f hello-world nginx
```

![](http://image.ownit.top/csdn/2019120917183790.png)

> **删除全部**

```
docker rmi -f $(docker images -qa)
```

![](http://image.ownit.top/csdn/2019120917232912.png)