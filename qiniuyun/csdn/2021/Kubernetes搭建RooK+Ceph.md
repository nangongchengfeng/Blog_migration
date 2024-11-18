---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-08 22:05:09
description: ：一个自我管理的分布式存储编排系统，它本身并不是存储系统，在存储和之前搭建了一个桥梁，存储系统的搭建或者维护变得特别简单，支持，做一些的快照、扩容等操作。是专用于环境的文件、块、对象存储服务。它实现了。。。。。。。
image: ../../title_pic/65.jpg
slug: '202103082205'
tags:
- Kubernetes应用
- kubernetes
- docker
title: Kubernetes搭建RooK+Ceph
---

<!--more-->

Rook：

       一个自我管理的分布式存储编排系统，它本身并不是存储系统，在存储和k8s之前搭建了一个桥梁，存储系统的搭建或者维护变得特别简单，Rook支持CSI，CSI做一些PVC的快照、PVC扩容等操作。

Rook是专用于Cloud-Native环境的文件、块、对象存储服务。它实现了一个自我管理的、自我扩容的、自我修复的分布式存储服务。

Rook支持自动部署、启动、配置、分配（provisioning）、扩容/缩容、升级、迁移、灾难恢复、监控，以及资源管理。 为了实现所有这些功能，Rook依赖底层的容器编排平台。

目前Rook仍然处于Alpha版本，初期专注于Kubernetes+Ceph。Ceph是一个分布式存储系统，支持文件、块、对象存储，在生产环境中被广泛应用。

![](../../image/20190104133544110.png)

![](../../image/20210308105542765.png)

Operator：主要用于有状态的服务，或者用于比较复杂应用的管理。

Helm：主要用于无状态的服务，配置分离。 

Rook：

       Agent：在每个存储节点上运行，用于配置一个FlexVolume插件，和k8s的存储卷进行集成。挂载网络存储、加载存储卷、格式化文件系统。

       Discover：主要用于检测链接到存储节点上的存储设备。

Ceph：

       OSD：直接连接每一个集群节点的物理磁盘或者是目录。集群的副本数、高可用性和容错性。

       MON：集群监控，所有集群的节点都会向Mon汇报。他记录了集群的拓扑以及数据存储位置的信息。

       MDS：元数据服务器，负责跟踪文件层次结构并存储ceph元数据。

       RGW：restful API接口。

       MGR：提供额外的监控和界面。

Rook 官方文档:<https://rook.io/docs/rook/v1.5/ceph-quickstart.html>

**环境部署**

```bash
git clone --single-branch --branch v1.5.8 https://github.com/rook/rook.git
cd rook/cluster/examples/kubernetes/ceph
kubectl create -f crds.yaml -f common.yaml -f operator.yaml

修改cluster.yaml文件
kubectl create -f cluster.yaml
```

```bash
  vim cluster.yaml

  storage: # cluster level storage configuration and selection
    useAllNodes: false #所有结节为存储节点，改为false
    useAllDevices: false  #使用所有的磁盘   改为false



    nodes:
    - name: "k8s-node02"
      devices: # specific devices to use for storage can be specified for each node
      - name: "sdb"  #k8s-node02新加的裸盘
    - name: "k8s-node01"
      directories:
      - path: "/data/ceph"

```

![](../../image/20210308114814270.png)

![](../../image/20210308124554144.png)

![](../../image/20210308124742127.png)

**[r](https://rook.io/docs/rook/v1.5/ceph-dashboard.html)ook的[dashboard](https://rook.io/docs/rook/v1.5/ceph-dashboard.html)：**  <https://rook.io/docs/rook/v1.5/ceph-dashboard.html>

 

```bash
kubectl -n rook-ceph get service
NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
rook-ceph-mgr                ClusterIP   10.108.111.192   <none>        9283/TCP         3h
rook-ceph-mgr-dashboard      ClusterIP   10.110.113.240   <none>        8443/TCP         3h
```

第一项服务用于报告[Prometheus指标](https://rook.io/docs/rook/v1.5/ceph-monitoring.html)，而后一项服务用于仪表板。如果您在集群中的节点上，则可以通过使用服务的DNS名称`https://rook-ceph-mgr-dashboard-https:8443`或通过连接到集群IP（在本示例中为）来连接到仪表板`https://10.110.113.240:8443`。或者使用NodePort暴露端口使用

**查询密码**

```bash
kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
```

 

![](../../image/20210308175946763.png)

 

![](../../image/20210308220450364.png)