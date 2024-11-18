---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-02-03 22:08:53
description: 初始化：初始换容器能够具有多个容器，应用运行在容器里面，但是它也可能有一个或多个先于应用容器启动的容器容器与普通的容器非常像，除了如下两点：容器总是运行到成功完成为止每个容器都必须在下一个容器启动之前。。。。。。。
image: ../../title_pic/71.jpg
slug: '202002032208'
tags:
- Kubernetes
- Pod
- 生命周期
- init
title: Kubernetes（k8s）Pod的生命周期
---

<!--more-->

# Kubernetes pod 初始化

![](../../image/20200203210606608.png)init C ：初始换容器

Pod 能够具有多个容器，应用运行在容器里面，但是它也可能有一个或多个先于应用容器启动的  Init容器

Init 容器与普通的容器非常像，除了如下两点：  

- Ø Init 容器总是运行到成功完成为止  
- Ø 每个 Init 容器都必须在下一个 Init 容器启动之前成功完成  

**如果 Pod 的 Init 容器失败，Kubernetes 会不断地重启该 Pod，直到Init 容器成功为止。然而**

**如果 Pod 对应的 restartPolicy 为 Never，它不会重新启动**

 

### **因为 Init 容器具有与应用程序容器分离的单独镜像，所以它们的启动相关代码具有如下优势：**

![](../../image/20200203212713217.png)

 

# Init 容器  

**init 模板 **

```bash
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; 
done;']
  - name: init-mydb
    image: busybox
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']
```

![](../../image/20200203215837563.png)

等待init的初始化。

```bash
kind: Service
apiVersion: v1
metadata:
  name: myservice
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

![](../../image/20200203220232560.png)

```
kind: Service
apiVersion: v1
metadata:
  name: mydb
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9377
```

![](../../image/20200203220452435.png)

**两个initC已经初始换完成**

![](../../image/20200203220626352.png)

![](../../image/20200203220642103.png)