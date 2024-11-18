---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-17 22:51:35
description: 模式是的扩展软件，它利用定制资源管理应用及其组件。遵循的理念，特别是在控制器方面。的场景就是专门给有状态应用而设计的。为什么只给有状态应用？因为无状态应用简单啊，没有服务间的交互，要再开一家火锅店，跟。。。。。。。
image: ../../title_pic/50.jpg
slug: '202103172251'
tags:
- Prometheus监控
- kubernetes
- docker
- 普罗米修斯
title: Kubernetes用operator部署prometheus
---

<!--more-->

## Operator 模式

Operator 是 Kubernetes 的扩展软件，它利用 [定制资源](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/) 管理应用及其组件。 Operator 遵循 Kubernetes 的理念，特别是在[控制器](https://kubernetes.io/zh/docs/concepts/architecture/controller/) 方面。

Operator的场景就是专门给有状态应用而设计的。

为什么只给有状态应用？

因为无状态应用简单啊，没有服务间的交互，要再开一家火锅店，跟k8s说一声，开一家一样的就可以了。

有状态不一样，你开了一家火锅店以后，客户的信息怎么同步，就涉及到与别的火锅店交涉的问题，当然你也可以写个别的程序做这个数据同步的操作。

但是operator做的事情就是能自动识别到火锅店客户信息的不对称，主动同步，你只用告诉operator我要再开一家连锁火锅店就好了。

## Kubernetes 上的 Operator[ ](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/operator/#kubernetes-%E4%B8%8A%E7%9A%84-operator)

Kubernetes 为自动化而生。无需任何修改，你即可以从 Kubernetes 核心中获得许多内置的自动化功能。 你可以使用 Kubernetes 自动化部署和运行工作负载， _甚至_ 可以自动化 Kubernetes 自身。

Kubernetes [控制器](https://kubernetes.io/zh/docs/concepts/architecture/controller/) 使你无需修改 Kubernetes 自身的代码，即可以扩展集群的行为。 Operator 是 Kubernetes API 的客户端，充当 [定制资源](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/) 的控制器

官网文档：<https://kubernetes.io/zh/docs/concepts/extend-kubernetes/operator/>

## 部署prometheus

### 1.1、下载

```bash
git clone -b release-0.7 --single-branch https://github.com/coreos/kube-prometheus.git
```

### 1.2、安装operator

```bash
[root@k8s-master01 ~]# cd /root/kube-prometheus/manifests/setup
[root@k8s-master01 setup]# kubectl create -f .

# 查看是否Running
[root@k8s-master01 ~]# kubectl get pod -n monitoring
NAME                                   READY   STATUS        RESTARTS   AGE
prometheus-operator-848d669f6d-bz2tc   2/2     Running       0          4m16s
```

### 1.3、安装Prometheus

```bash
[root@k8s-master01 ~]# cd /root/kube-prometheus/manifests
[root@k8s-master01 manifests]# kubectl create -f .
```

### 1.4、创建ingress

```bash
[root@k8s-master01 manifests]# cat svc-ingress.yal 
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: prom-ingresses
  namespace: monitoring
spec:
  rules:
  - host: alert.test.com
    http:
      paths:
      - backend:
          serviceName: alertmanager-main
          servicePort: 9093
        path: /
  - host: grafana.test.com
    http:
      paths:
      - backend:
          serviceName: grafana
          servicePort: 3000
        path: /
  - host: prom.test.com
    http:
      paths:
      - backend:
          serviceName: prometheus-k8s
          servicePort: 9090
        path: /





[root@k8s-master01 manifests]# kubectl get ingress -n monitoring 
NAME             CLASS    HOSTS                                           ADDRESS        PORTS   AGE
prom-ingresses   <none>   alert.test.com,grafana.test.com,prom.test.com   10.96.107.62   80      23h
```

### alert.test.com（报警）

![](../../image/20210317224918783.png)

### prom.test.com（普罗米修斯）

![](../../image/20210317225010450.png)

### grafana.test.com（图形展示）

![](../../image/20210317225110179.png)