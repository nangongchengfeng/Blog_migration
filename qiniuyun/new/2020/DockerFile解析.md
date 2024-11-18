---
author: 南宫乘风
categories:
- Docker
date: 2020-01-03 11:29:01
description: 、是什么是用来构建镜像的构建文件，是由一系列命令和参数构成的脚本。构建三步骤编写文件文件什么样？？？以我们熟悉的为例、构建过程解析内容基础知识：每条保留字指令都必须为大写字母且后面要跟随至少一个参数：。。。。。。。
image: http://image.ownit.top/4kdongman/10.jpg
tags:
- dockerfile
- docker
- 镜像
- 容器
title: DockerFile解析
---

<!--more-->

# 1、是什么

Dockerfile是用来构建Docker镜像的构建文件，是由一系列命令和参数构成的脚本。

### 构建三步骤

1.  编写Dockerfile文件
2.  docker build
3.  docker run

### 文件什么样？？？

以我们熟悉的CentOS为例 

<https://hub.docker.com/_/centos/>

![](http://image.ownit.top/csdn/20200103112030333.png)

![](http://image.ownit.top/csdn/20200103112043210.png)  
 

```bash
FROM scratch
ADD centos- 7-docker.tar.xz /
LABEL org. label-schema. schema-version = "1.0" \
org. label-schema. name="CentOS Base Image" \
org. label-schema. vendor="Cent0S" \
org. label-schema. license="GPLv2" \
org. label-schema. build-date="20180531"
CMD ["/bin/bash"]
```

# 2、DockerFile构建过程解析

### **Dockerfile内容基础知识**

- 1：每条保留字指令都必须为大写字母且后面要跟随至少一个参数
- 2：指令按照从上到下，顺序执行
- 3：#表示注释
- 4：每条指令都会创建一个新的镜像层，并对镜像进行提交

### **Docker执行Dockerfile的大致流程**

- （1）docker从基础镜像运行一个容器
- （2）执行一条指令并对容器作出修改
- （3）执行类似docker commit的操作提交一个新的镜像层
- （4）docker再基于刚提交的镜像运行一个新容器
- （4）docker再基于刚提交的镜像运行一个新容器

**从应用软件的角度来看，Dockerfile、Docker镜像与Docker容器分别代表软件的三个不同阶段，**

\*  Dockerfile是软件的原材料

\*  Docker镜像是软件的交付品

\*  Docker容器则可以认为是软件的运行态。

Dockerfile面向开发，Docker镜像成为交付标准，Docker容器则涉及部署与运维，三者缺一不可，合力充当Docker体系的基石。

![](http://image.ownit.top/csdn/20200103112536955.png)

1 Dockerfile，需要定义一个Dockerfile，Dockerfile定义了进程需要的一切东西。Dockerfile涉及的内容包括执行代码或者是文件、环境变量、依赖包、运行时环境、动态链接库、操作系统的发行版、服务进程和内核进程\(当应用进程需要和系统服务和内核进程打交道，这时需要考虑如何设计namespace的权限控制\)等等;

2 Docker镜像，在用Dockerfile定义一个文件之后，docker build时会产生一个Docker镜像，当运行 Docker镜像时，会真正开始提供服务;

3 Docker容器，容器是直接提供服务的。