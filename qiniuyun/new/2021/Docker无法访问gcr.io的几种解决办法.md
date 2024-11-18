---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-06 22:46:41
description: 由于一些原因在国内无法访问上的镜像在安装时经常访问阿里云的地址。面结合实际经验列举出几种常用的办法来解决这个问题！一、使用阿里云镜像地址地址一：地址二：二、使用下的这个域名下同步了很多谷歌镜像比如说要。。。。。。。
image: http://image.ownit.top/4kdongman/21.jpg
tags:
- 技术记录
title: Docker无法访问gcr.io的几种解决办法
---

<!--more-->

 

由于一些原因,在国内无法访问gcr.io上的镜像,在安装kubernetes时经常访问阿里云的地址。面结合实际经验,列举出几种常用的办法来解决这个问题！

### 一、使用阿里云镜像地址

```
地址一：registry.aliyuncs.com/google_containers
地址二：registry.cn-hangzhou.aliyuncs.com/google_containers
```

 

### 二、使用dockerhub下的`mirrorgooglecontainers`

​ 这个域名下同步了很多谷歌镜像,比如说要下载`gcr.io/google_containers/coredns:1.7.0`,

可以使用`docker pull mirrorgooglecontainers/coredns:1.7.0`来进行下载,下载以后对镜像重新打标签:

```bash
# 1、先pull下来
[root@k8s-master01 Ratel]# docker pull mirrorgooglecontainers/kube-proxy-amd64:v1.11.3
v1.11.3: Pulling from mirrorgooglecontainers/kube-proxy-amd64
06545d1c6152: Pull complete 
d5f5a75f5817: Pull complete 
c21dcda023ab: Pull complete 
Digest: sha256:cd0c257e3f4a79a0ae7964b3429c491e9d43bf1bb015618a4c311165d3915b7b
Status: Downloaded newer image for mirrorgooglecontainers/kube-proxy-amd64:v1.11.3
docker.io/mirrorgooglecontainers/kube-proxy-amd64:v1.11.3

# 2、重新打标签
[root@k8s-master01 Ratel]# docker tag docker.io/mirrorgooglecontainers/kube-proxy-amd64:v1.11.3   k8s.gcr.io/kube-proxy-amd64:v1.11.3

# 3、查看镜像，然后就可以直接使用这个镜像了
[root@k8s-master01 Ratel]# docker images | grep k8s.gcr.io/kube-proxy-amd64
k8s.gcr.io/kube-proxy-amd64                                       v1.11.3   be5a6e1ecfa6   2 years ago     97.8MB
```

### 三、使用国内作者制作的gcr.io镜像安装工具

```bash
项目地址: https://github.com/zhangguanzhang/gcr.io
```

3.0、使用search命令的时候,如果没有安装jq则会提示安装jq.jq在centos下安装方法:

 -    安装EPEL源：

```
[root@k8s-master01 ~]# yum install epel-release
```

 -    安装完EPEL源后，可以查看下jq包是否存在：

```
[root@k8s-master01 ~]# yum list jq
```

 -    安装jq：

```
[root@k8s-master01 ~]# yum install jq -y
```

3.1、查询namespace

```
[root@k8s-master01 ~]# curl -s https://zhangguanzhang.github.io/bash/pull.sh | bash -s search gcr.io
cloud-builders
cloud-datalab
cloudsql-docker
distroless
google-appengine
google-samples
google_containers
google_samples
heptio-images
```

3.2、查询某一名称空间下镜像列表

```
[root@k8s-master01 ~]# curl -s https://zhangguanzhang.github.io/bash/pull.sh | bash -s search gcr.io/google_containers
# gcr.io/google_containers ---> namespace ——————> 根据上面查询出来的namespace查
addon-builder
addon-resizer-amd64
addon-resizer-arm
addon-resizer-arm64
addon-resizer-ppc64le
addon-resizer-s390x
addon-resizer
aggregator
alpine-iptables-amd64
alpine-iptables-arm
alpine-iptables-arm64
```

3.3、查询某一镜像的版本所有版本tag

```
[root@k8s-master01 ~]# curl -s https://zhangguanzhang.github.io/bash/pull.sh | bash -s search gcr.io/google_containers/coredns 

# 在namespace后面搜索image的版本tag
1.0.1
1.0.1__amd64_linux
1.0.1__arm64_linux
1.0.1__arm_linux
1.0.1__ppc64le_linux
1.0.1__s390x_linux
1.0.6
1.0.6__amd64_linux
1.0.6__arm64_linux
1.0.6__arm_linux
1.0.6__ppc64le_linux
1.0.6__s390x_linux
1.1.3
1.1.3__amd64_linux
```

3.4 下载镜像

```bash
curl -s https://zhangguanzhang.github.io/bash/pull.sh | bash -s  gcr.io/google_containers/coredns:1.7.0
```

原文地址：<https://www.cnblogs.com/tylerzhou/p/10971341.html>