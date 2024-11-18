---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-02-11 16:02:24
description: 节点亲和性：软策略：硬策略先硬后软键值运算关系：的值在某个列表中：的值不在某个列表中：的值大于某个值：的值小于某个值：某个存在：某个不存在亲和性：软策略：硬策略亲和性反亲和性调度策略比较如下：调度策略。。。。。。。
image: ../../title_pic/02.jpg
slug: '202002111602'
tags:
- Kubernetes
- k8s
- 调度
- 亲和性
title: Kubernetes（k8s）的调度器 - 调度亲和性详细介绍
---

<!--more-->

# 节点亲和性

**pod.spec.nodeAﬃnity**

- preferredDuringSchedulingIgnoredDuringExecution：软策略
- requiredDuringSchedulingIgnoredDuringExecution：硬策略

### requiredDuringSchedulingIgnoredDuringExecution

```bash
apiVersion: v1
kind: Pod
metadata:
  name: affinity
  labels:
    app: node-affinity-pod
spec:
  containers:
  - name: with-node-affinity
    image: wangyanglinux/myapp:v1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            operator: NotIn
            values:
            - node02
```

# ![](../../image/20200211145022940.png)

# ![](../../image/20200211145132557.png)

### preferredDuringSchedulingIgnoredDuringExecution

```bash
apiVersion: v1
kind: Pod
metadata:
  name: affinity
  labels:
    app: node-affinity-pod
spec:
  containers:
  - name: with-node-affinity
    image: wangyanglinux/myapp:v1
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
            - node3
```

![](../../image/20200211150043932.png)

# 先硬后软

```bash
apiVersion: v1
kind: Pod
metadata:
  name: affinity
  labels:
    app: node-affinity-pod
spec:
  containers:
  - name: with-node-affinity
    image: hub.atguigu.com/library/myapp:v1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            operator: NotIn
            values:
            - k8s-node02
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: source
            operator: In
            values:
            - qikqiak
```

### **键值运算关系**

- **In：label 的值在某个列表中**
- **NotIn：label 的值不在某个列表中**
- **Gt：label 的值大于某个值**
- **Lt：label 的值小于某个值**
- **Exists：某个 label 存在**
- **DoesNotExist：某个 label 不存在**  
 

#  Pod  亲和性

**pod.spec.aﬃnity.podAﬃnity/podAntiAﬃnity**

 -    **preferredDuringSchedulingIgnoredDuringExecution：软策略**
 -    **requiredDuringSchedulingIgnoredDuringExecution：硬策略**

```bash
apiVersion: v1
kind: Pod
metadata:
  name: pod-3
  labels:
    app: pod-3
spec:
  containers:
  - name: pod-3
    image: wangyanglinux/myapp:v1
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - pod-1
        topologyKey: kubernetes.io/hostname
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - pod-2
          topologyKey: kubernetes.io/hostname
```

亲和性/反亲和性调度策略比较如下：  
 

<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:700px;"><tbody><tr><td>调度策略匹配 标签</td><td>匹配 标签</td><td>操作符</td><td>拓扑域 支持</td><td>调度目标</td></tr><tr><td>nodeAﬃnity</td><td>&nbsp;主机</td><td>In, NotIn, Exists, DoesNotExist, Gt, Lt</td><td>否</td><td>指向主机</td></tr><tr><td>podAﬃnity&nbsp;</td><td>POD</td><td>In, NotIn, Exists, DoesNotExist</td><td>是</td><td>POD与指定POD同一拓 扑域</td></tr><tr><td>podAnitAﬃnity&nbsp;</td><td>POD</td><td>In, NotIn, Exists, DoesNotExist</td><td>是</td><td>POD与指定POD不在同 一拓扑域</td></tr></tbody></table>