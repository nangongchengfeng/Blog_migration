---
author: 南宫乘风
categories:
- Docker
date: 2019-12-10 14:15:02
description: 目录新建并启动容器说明启动交互式容器列出当前所有正在运行的容器退出容器进入出容器启动容器停止容器强制停止容器删除已停止的容器一次性删除多个容器有镜像才能创建容器，这是根本前提下载一个镜像演示新建并启动。。。。。。。
image: ../../title_pic/15.jpg
slug: '201912101415'
tags:
- docker
- 容器
- 命令
title: Docker容器常用命令
---

<!--more-->

**目录**

[新建并启动容器](#%E6%96%B0%E5%BB%BA%E5%B9%B6%E5%90%AF%E5%8A%A8%E5%AE%B9%E5%99%A8)

[OPTIONS说明](#OPTIONS%E8%AF%B4%E6%98%8E)

[启动交互式容器](#%E5%90%AF%E5%8A%A8%E4%BA%A4%E4%BA%92%E5%BC%8F%E5%AE%B9%E5%99%A8)

[列出当前所有正在运行的容器](#%E5%88%97%E5%87%BA%E5%BD%93%E5%89%8D%E6%89%80%E6%9C%89%E6%AD%A3%E5%9C%A8%E8%BF%90%E8%A1%8C%E7%9A%84%E5%AE%B9%E5%99%A8)

[退出容器](#%E9%80%80%E5%87%BA%E5%AE%B9%E5%99%A8)

[exit](#exit)

[ctrl+P+Q](#ctrl%2BP%2BQ)

[进入出容器](#%E8%BF%9B%E5%85%A5%E5%87%BA%E5%AE%B9%E5%99%A8)

[启动容器](#%E5%90%AF%E5%8A%A8%E5%AE%B9%E5%99%A8)

[停止容器](#%E5%81%9C%E6%AD%A2%E5%AE%B9%E5%99%A8)

[强制停止容器](#%E5%BC%BA%E5%88%B6%E5%81%9C%E6%AD%A2%E5%AE%B9%E5%99%A8)

[删除已停止的容器](#%E5%88%A0%E9%99%A4%E5%B7%B2%E5%81%9C%E6%AD%A2%E7%9A%84%E5%AE%B9%E5%99%A8)

[一次性删除多个容器](#%E4%B8%80%E6%AC%A1%E6%80%A7%E5%88%A0%E9%99%A4%E5%A4%9A%E4%B8%AA%E5%AE%B9%E5%99%A8)

---
 

> **有镜像才能创建容器，这是根本前提\(下载一个CentOS镜像演示\)**

```bash
docker pull centos
```

![](../../image/20191209172937238.png)

## **新建并启动容器**

**docker run \[OPTIONS\] IMAGE \[COMMAND\] \[ARG...\]**

### OPTIONS说明

OPTIONS说明（常用）：有些是一个减号，有些是两个减号

- \--name="容器新名字": 为容器指定一个名称；
- \-d: 后台运行容器，并返回容器ID，也即启动守护式容器；
- \-i：以交互模式运行容器，通常与 -t 同时使用；
- \-t：为容器重新分配一个伪输入终端，通常与 -i 同时使用；
- \-P: 随机端口映射；

 

- \-p: 指定端口映射，有以下四种格式
-       ip:hostPort:containerPort
-       ip::containerPort
-       hostPort:containerPort
-       containerPort

### 启动交互式容器

**#使用镜像centos:latest以交互模式启动一个容器,在容器内执行/bin/bash命令。**

```bash
docker run -it centos /bin/bash 
```

![](../../image/20191209173613526.png)

## 列出当前所有正在运行的容器

**docker ps \[OPTIONS\]**

OPTIONS说明（常用）：

- \-a :列出当前所有正在运行的容器+历史上运行过的（docker ps）![](../../image/20191209174141861.png)
- \-l :显示最近创建的容器。
- \-n：显示最近n个创建的容器。
- \-q :静默模式，只显示容器编号。
- \--no-trunc :不截断输出

## 退出容器

### exit

- **容器停止退出**

### **ctrl+P+Q**

- **容器不停止退出**

## 进入出容器

**docker attach  名称**

```
 docker attach edc486762ad2
```

![](../../image/20191209180317727.png)

## 启动容器

```
docker start 容器ID或者容器名
```

**重启容器**

```
docker restart 容器ID或者容器名
```

## 停止容器

```
docker stop 容器ID或者容器名
```

## 强制停止容器

```
docker kill 容器ID或者容器名
```

## 删除已停止的容器

```
docker rm 容器ID
```

## 一次性删除多个容器

```
docker rm -f $(docker ps -a -q)
```

```
docker ps -a -q | xargs docker rm
```