---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-12-25 10:13:24
description: 目录、项目迁移到平台的怎样的流程、基本概念、构建项目镜像、部署项目镜像到平台、项目迁移到平台的怎样的流程、基本概念最小部署单元一组容器的集合一个中的容器共享网络命名空间是短暂的：无状态应用部署：有状态。。。。。。。
image: http://image.ownit.top/4kdongman/37.jpg
tags:
- kubernetes
title: 在Kubernetes（k8s）中部署Java应用
---

<!--more-->

**目录**

[1、项目迁移到k8s平台的怎样的流程](#1%E3%80%81%E9%A1%B9%E7%9B%AE%E8%BF%81%E7%A7%BB%E5%88%B0k8s%E5%B9%B3%E5%8F%B0%E7%9A%84%E6%80%8E%E6%A0%B7%E7%9A%84%E6%B5%81%E7%A8%8B)

[2、Kubernetes基本概念](#2%E3%80%81Kubernetes%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5)

[3、构建项目镜像](#3%E3%80%81%E6%9E%84%E5%BB%BA%E9%A1%B9%E7%9B%AE%E9%95%9C%E5%83%8F)

[4、部署项目镜像到Kubernetes平台](#4%E3%80%81%E9%83%A8%E7%BD%B2%E9%A1%B9%E7%9B%AE%E9%95%9C%E5%83%8F%E5%88%B0Kubernetes%E5%B9%B3%E5%8F%B0)

---

# 1、项目迁移到k8s平台的怎样的流程

![](http://image.ownit.top/csdn/2020010911345217.png)

## 2、Kubernetes基本概念

** Pod** • 最小部署单元 • 一组容器的集合 • 一个Pod中的容器共享网络命名空间 • Pod是短暂的

** Controllers** • Deployment ： 无状态应用部署 • StatefulSet ： 有状态应用部署 • DaemonSet ： 确保所有Node运行同一个Pod • Job ： 一次性任务 • Cronjob ： 定时任务  
更高级层次对象，部署和管理Pod

** Service** • 防止Pod失联 • 定义一组Pod的访问策略  
** Label** ： 标签，附加到某个资源上，用于关联对象、查询和筛选  
** Namespaces** ： 命名空间，将对象逻辑上隔离

## 3、构建项目镜像

## 1、准备Jar包

![](http://image.ownit.top/csdn/20200109133438926.png)

## 2、制作镜像

解压文件

```
yum install -y unzip && unzip tomcat-java-demo-master.zip 
```

把这个sql文件导入mysql。

![](http://image.ownit.top/csdn/2020010913432272.png)

在Node1上下载mysql:5.6的镜像。

```
docker run -p 3306:3306 --name mysql-master \
-v /mydata/mysql/master/log:/var/log/mysql \
-v /mydata/mysql/master/data:/var/lib/mysql \
-v /mydata/mysql/master/conf:/etc/mysql \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:5.6
```

![](http://image.ownit.top/csdn/20200109134158834.png)

接下导入sql数据。

可以使用工具导入方便。

![](http://image.ownit.top/csdn/20200109134655562.png)

修改代码里的配置文件

![](http://image.ownit.top/csdn/20200109135014179.png)

![](http://image.ownit.top/csdn/20200109134951198.png)

安装JDk和Maven环境

```
 yum install -y java-1.8.0-openjdk maven
```

修改maven源

```bash
vim /etc/maven/settings.xml


<mirror>
    <id>alimaven</id>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    <mirrorOf>central</mirrorOf>
</mirror>
```

![](http://image.ownit.top/csdn/20201222131952108.png)

编译源码 【漫长的等待】

```
mvn clean package -D maven.test.skip=true
```

![](http://image.ownit.top/csdn/20200109142726284.png)

准备使用DockerFile文件来构建镜像。

![](http://image.ownit.top/csdn/20200109160811294.png)

```bash
FROM lizhenliang/tomcat 
LABEL maintainer www.ctnrs.com
RUN rm -rf /usr/local/tomcat/webapps/*
ADD target/*.war /usr/local/tomcat/webapps/ROOT.war 
```

构建镜像

```bash
docker build -t lizhenliang/java-demo -f Dockerfile .
```

![](http://image.ownit.top/csdn/2020010916181546.png)

已经成功

![](http://image.ownit.top/csdn/2020010916261039.png)

写ymal文件【生成模板，在修改】

```bash
kubectl create deployment java-demo --image=lizhenliang/java-demo --dry-run -o yaml 

#内容
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: java-demo
  name: java-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: java-demo
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: java-demo
    spec:
      containers:
      - image: lizhenliang/java-demo
        name: java-demo
        resources: {}
status: {}
```

重定向，生成本地的yaml

```bash
kubectl create deployment java-demo --image=lizhenliang/java-demo --dry-run -o yaml > deploy.yaml
```

```bash
[root@master ~]# cat deploy.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: java-demo
  name: java-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: java-demo
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: java-demo
    spec:
      containers:
      - image: lizhenliang/java-demo
        name: java-demo
```

运行

```
kubectl apply -f deploy.yaml 
```

![](http://image.ownit.top/csdn/2020010916434881.png)

```bash
kubectl get pods
```

![](http://image.ownit.top/csdn/20200109164626209.png)

## 4、部署项目镜像到Kubernetes平台

![](http://image.ownit.top/csdn/20201222145905995.png)