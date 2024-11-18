---
author: 南宫乘风
categories:
- Docker
date: 2020-01-17 15:20:40
description: 介绍这个项目名称特别贴切。在的解释中，是指动物的群集行为。比如我们常见的蜂群，鱼群，秋天往南飞的雁群都可以称作。项目正是这样，通过把多个聚集在一起，形成一个大的，对外提供容器的集群服务。同时这个集群对。。。。。。。
image: http://image.ownit.top/4kdongman/14.jpg
tags:
- swarm
- docker
- 集群
title: Centos搭建docker swarm集群详细教程
---

<!--more-->

#  swarm介绍 

Swarm这个项目名称特别贴切。在Wiki的解释中，Swarm behavior是指动物的群集行 为。比如我们常见的蜂群，鱼群，秋天往南飞的雁群都可以称作Swarm behavior。 Swarm项目正是这样，通过把多个Docker Engine聚集在一起，形成一个大的dockerengine，对外提供容器的集群服务。同时这个集群对外提供Swarm API（命令，docker engine的命令），用户可以像使用Docker Engine一样使用Docker集群。  
![](http://image.ownit.top/csdn/20200117141322621.png)

Swarm是Docker公司在2014年12月初发布的容器管理工具，和Swarm一起发布的 Docker管理工具还有Machine以及Compose。Swarm是一套较为简单的工具，用以管理 Docker集群，使得Docker集群暴露给用户时相当于一个虚拟的整体。Swarm将一群 Docker宿主机变成一个单一的，虚拟的主机。Swarm使用标准的Docker API接口作为其 前端访问入口，换言之，各种形式的Docker Client\(docker client in Go, docker\_py, docker等\)均可以直接与Swarm通信。Swarm几乎全部用Go语言来完成开发，Swarm0.2 版本增加了一个新的策略来调度集群中的容器，使得在可用的节点上传播它们，以及支  
持更多的Docker命令以及集群驱动。Swarm deamon只是一个调度器（Scheduler）加 路由器\(router\)，Swarm自己不运行容器，它只是接受docker客户端发送过来的请求， 调度适合的节点来运行容器，这意味着，即使Swarm由于某些原因挂掉了，集群中的节 点也会照常运行，当Swarm重新恢复运行之后，它会收集重建集群信息。 

## **docker swarm特点：**

- 1\) 对外以Docker API接口呈现，这样带来的好处是，如果现有系统使用Docker Engine， 则可以平滑将Docker Engine切到Swarm上，无需改动现有系统。
- 2\) Swarm对用户来说，之前使用Docker的经验可以继承过来。非常容易上手，学习成本 和二次开发成本都比较低。同时Swarm本身专注于Docker集群管理，非常轻量，占用资 源也非常少。简单说，就是插件化机制，Swarm中的各个模块都抽象出了API，可以根据 自己一些特点进行定制实现。 
- 3\)  Swarm自身对Docker命令参数支持的比较完善，Swarm目前与Docker是同步发布 的。Docker的新功能，都会第一时间在Swarm中体现。 

## **docker swarm架构 **

Swarm作为一个管理Docker集群的工具，首先需要将其部署起来，可以单独将Swarm部 署于一个节点。另外，自然需要一个Docker集群，集群上每一个节点均安装有Docker。

![](http://image.ownit.top/csdn/20200117141452862.png)

![](http://image.ownit.top/csdn/20200117141503667.png)

## 相关术语：

- Swarm Manager：集群的管理工具，通过swarm manager管理多个节点。
- Node：是已加入到swarm的Docker引擎的实例 。
- manager nodes：也就是管理节点 ，执行集群的管理功能，维护集群的状态， 选举一个leader节点去执   行调度任务
- worker nodes，也就是工作节点 ，接收和执行任务。参与容器集群负载调度， 仅用于承载task   
 

![](http://image.ownit.top/csdn/20200117141553516.png)

**一个服务是工作节点上执行任务的定义。创建一个服务，指定了容器所使用的镜像和 容器运行的命令。service是运行在worker nodes上的task的描述，service的描述包 括使用哪个docker 镜像，以及在使用该镜像的容器中执行什么命令。**  
![](http://image.ownit.top/csdn/20200117141606627.png)

**task任务：一个任务包含了一个容器及其运行的命令。task是service的执行实体， task启动docker容器并在容器中执行任务**

![](http://image.ownit.top/csdn/20200117141622287.png)

#  docker swarm使用 

搭建步骤：

##   
1、环境准备：

1.1、准备三台已近安装docker engine的centos/Ubuntu系统主机（docker版本必须在 1.12以上的版本，老版本不支持swarm）

1.2、docker容器主机的ip地址固定，集群中所有工作节点必须能访问该管理节点

1.3、集群管理节点必须使用相应的协议并且保证端口可用 集群管理通信：

- TCP，端口2377      
- 节点通信：TCP和UDP，端口7946      
- 覆盖型网络\(docker网络\)：UDP，端口4789   overlay驱动      

说明：三台容器主机的ip地址分别为： 192.168.200.162（管理节点） 192.168.200.163（工作节点） 192.168.200.158（工作节点）

主机名称分别为：manager1、work1以及work2

```
vim /etc/hostname  (修改完成后需要重启)
```

## 2、创建docker swarm 

2.1、在manager1机器上创建docker swarm集群 

```
docker swarm init ‐‐advertise‐addr 192.168.200.162 （‐‐advertise‐addr将该IP地址的机器设置为集群管理节点；如果是单节点，无需该参 数
```

2.2、查看管理节点集群信息： 

```
docker node ls
```

## 3、向docker swarm中添加工作节点：在两个工作节点中分别执行如下命令，ip地址是 manager节点的 

3.1、添加两个work节点 

```
docker swarm join ‐‐token xxx 192.168.200.138:2377  （worker1）
 docker swarm join ‐‐token xxx 192.168.200.138:2377  （worker2） 
```

（‐‐token xxx:向指定集群中加入工作节点的认证信息，xxx认证信息是在创建docker  swarm时产生的） 

3.2、继续查看管理节点集群信息与之前的区别 

```
docker node ls
```

## 4、在docker swarm中部署服务

在Docker Swarm集群中部署服务时，既可以使用Docker Hub上自带的镜像来启动服务，也  
5 docker compose编排工具 5.1 docker compose介绍   
可以使用自己通Dockerfile构建的镜像来启动服务。如果使用自己通过Dockerfile构建的 镜像来启动服务那么必须先将镜像推送到Docker Hub中心仓库。为了方便读者的学习，这里 以使用Docker Hub上自带的alpine镜像为例来部署集群服务 

4.1、部署服务 

```
docker service create ‐‐replicas 1 ‐‐name helloworld alpine ping  docker.com 
```

- docker service create指令：用于在Swarm集群中创建一个基于alpine镜像的服务
- ‐‐replicas参数：指定了该服务只有一个副本实例
- ‐‐name参数：指定创建成功后的服务名称为helloworld
- ping docker.com指令：表示服务启动后执行的命令

## 5.查看docker swarm集群中的服务 

```bash
查看服务列表：docker service ls 
查看部署具体服务的详细信息：docker service inspect 
服务名称 查看服务在集群节点上的分配以及运行情况：docker service ps 服务名称
```

## 6、修改副本数量

在manager1上，更改服务副本的数量（创建的副本会随机分配到不同的节点） 

```
docker service scale helloworld=5
```

## 7、删除服务（在管理节点）

```
docker service rm 服务名称
```

## 8、访问服务 

8.1、查看集群环境下的网络列表：

```
docker network ls
```

8.2、在manager1上创建一overlay为驱动的网络（默认使用的网络连接ingress） 

```
docker network create ‐d=overlay my‐multi‐host‐network 
```

8.3、在集群管理节点manager1上部署一个nginx服务 

```bash
docker service create \   
‐‐network my‐multi‐host‐network \   
‐‐name my‐web \
   ‐p 8080:80 \
   ‐‐replicas 2 \ 
  nginx 
```

8.3、在管理节点查看服务的运行情况： 

```bash
docker service ps my‐web 
```