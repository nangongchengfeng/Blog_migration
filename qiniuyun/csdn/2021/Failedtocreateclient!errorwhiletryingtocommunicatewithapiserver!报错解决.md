---
author: 南宫乘风
categories:
- 错误问题解决
date: 2021-03-16 21:36:32
description: 问题：安装普罗米修斯，其中容器一直报错环境：分析：首先，这个中有三个容器。问题出现在。导致容器不断的重启看问题，是无法连接到这个和端口上。由可见，这个是的核心和端口。但是他那边显示无法连接。测试一下这。。。。。。。
image: ../../title_pic/46.jpg
slug: '202103162136'
tags:
- docker
- 运维
- Kubernetes
- kubernetes
title: Failed to create client- error while trying to communicate with apiserver-
  报错解决
---

<!--more-->

问题：Kubernetes安装普罗米修斯，其中kube-state-metrics 容器一直报错

环境：Kubernetes 1.18

```bash
[root@k8s-master01 manifests]# kubectl logs -f kube-state-metrics-bdb8874fd-tnrrg  -n monitoring -c kube-state-metrics
I0316 13:12:52.295699       1 main.go:86] Using default collectors
I0316 13:12:52.295788       1 main.go:98] Using all namespace
I0316 13:12:52.295798       1 main.go:139] metric white-blacklisting: blacklisting the following items: 
W0316 13:12:52.295807       1 client_config.go:543] Neither --kubeconfig nor --master was specified.  Using the inClusterConfig.  This might not work.
I0316 13:12:52.297186       1 main.go:184] Testing communication with server
F0316 13:13:22.298801       1 main.go:147] Failed to create client: error while trying to communicate with apiserver: Get https://10.96.0.1:443/version?timeout=32s: dial tcp 10.96.0.1:443: i/o timeout
```

分析：

首先，这个kube-state-metrics-bdb8874fd-tnrrg 中有三个容器。问题出现在kube-state-metrics。导致容器不断的重启

看问题，是无法连接到10.96.0.1:443这个ip和端口上。

```bash
[root@k8s-master01 ~]# kubectl get svc
NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
csi-metrics-cephfsplugin   ClusterIP   10.96.218.238   <none>        8080/TCP   21h
kubernetes                 ClusterIP   10.96.0.1       <none>        443/TCP    83d
nginx                      ClusterIP   10.96.215.251   <none>        80/TCP     16d
```

由svc可见，这个是Kubernetes的核心ip和端口。但是他那边显示无法连接。

测试一下

![](../../image/20210316213148931.png)

这个端口是通的，但是无法连接。报错显示io线程延时。

解决：

kube-state-metrics原本安装在k8s-node02上。这边删除，还是从重建k8s-node02.

分析一下node02的cpu有点高，我直接指定到k8s-node01上。

然后测试，没有显示io延时报错

![](../../image/20210316213425478.png)

![](../../image/202103162136066.png)