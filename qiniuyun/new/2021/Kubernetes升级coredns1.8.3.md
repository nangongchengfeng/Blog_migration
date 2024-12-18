---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-17 21:39:04
description: 日常工作中，我们有时会对一些比较低的组件做升级。版本的升级，可以解决一下和漏洞，稳定系统的性能。这次我升级对升级。主要是中对域名和解析，可以作为内网的解析服务器。一、查看当前版本二、升级、查询最新版的。。。。。。。
image: http://image.ownit.top/4kdongman/33.jpg
tags:
- Kubernetes应用
- kubernetes
- github
- coredns
title: Kubernetes升级coredns1.8.3
---

<!--more-->

日常工作中，我们有时会对一些比较低的组件做升级。

版本的升级，可以解决一下bug和漏洞，稳定系统的性能。

这次我升级对coredns升级。

coredns主要是Kubernetes中对域名和ip解析，可以作为内网的dns解析服务器。

## 一、查看当前coredns版本

```bash
[root@k8s-master01 ~]# kubectl get pod -n kube-system coredns-7ff77c879f-h2jw9 -oyaml | grep image
            f:image: {}
            f:imagePullPolicy: {}
    image: registry.aliyuncs.com/google_containers/coredns:1.6.7
    imagePullPolicy: IfNotPresent
    image: registry.aliyuncs.com/google_containers/coredns:1.6.7
    imageID: docker-pullable://registry.aliyuncs.com/google_containers/coredns@sha256:695a5e109604331f843d2c435f488bf3f239a88aec49112d452c1cbf87e88405
```

### ![](http://image.ownit.top/csdn/20210317212518122.png)

## 二、升级

### 2.1、查询最新版coredns的版本

```bash
# coredns官网：https://github.com/coredns/coredns
# 老版本用：kube-dns
# 新版的都用：coredns


# 部署文档：https://github.com/coredns/deployment/tree/master/kubernetes
```

最新版地址：<https://github.com/coredns/deployment/blob/master/kubernetes/coredns.yaml.sed>

![](http://image.ownit.top/csdn/20210317212559119.png)

现在最新版是1.8.3

### 2.2、备份原来的cm、deploy、clusterrole、clusterrolebinding

**切记：日常我们做任何操作（升级，删除，修改），一定要备份，防止错误操作，导致数据丢失，或者功能无法使用**

**备份好处，可以确保数据安全性，如果出现功能不能使用，可以立刻回滚，不长时间影响业务**

```bash
mkdir coredns && cd coredns
kubectl get cm -n kube-system coredns -oyaml > coredns-config.yaml
kubectl get deploy -n kube-system coredns -oyaml > coredns-controllers.yaml
kubectl get clusterrole system:coredns -oyaml > coredns-clusterrole.yaml
kubectl get clusterrolebinding  system:coredns -oyaml > coredns-clusterrolebinding.yaml
```

![](http://image.ownit.top/csdn/20210317213032740.png)

### 2.3、升级coredns

下载地址：git clone https://github.com/coredns/deployment.git

```bash
# 1、下载文件
git clone https://github.com/coredns/deployment.git

# 2、升级
cd deployment/kubernetes/
./deploy.sh -s | kubectl apply -f -




[root@k8s-master01 ~]# cd deployment/kubernetes/
[root@k8s-master01 kubernetes]# ./deploy.sh -s | kubectl apply -f -
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
serviceaccount/coredns configured
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
clusterrole.rbac.authorization.k8s.io/system:coredns configured
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
clusterrolebinding.rbac.authorization.k8s.io/system:coredns configured
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
configmap/coredns configured
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
deployment.apps/coredns configured
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
service/kube-dns configured
```

![](http://image.ownit.top/csdn/20210317213826746.png)

已经升级成功