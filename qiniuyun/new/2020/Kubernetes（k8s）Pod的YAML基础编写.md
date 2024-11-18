---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-02-03 21:02:49
description: 中的一般都是采用编写如果没有给定名称，那么默认为，可以使用获取当前版本上所有的版本信息每个版本可能不同资源类别：资源元数据主要目的是方便用户阅读查找期望的状态：当前状态，本字段有自身维护，用户不能去定。。。。。。。
image: http://image.ownit.top/4kdongman/12.jpg
tags:
- Yaml
- Kubernetes
- pod
- k8s
title: Kubernetes（k8s）Pod的YAML基础编写
---

<!--more-->

**Kubernetes中的Pod一般都是采用yaml编写**

```bash
apiVersion: group/apiversion  # 如果没有给定 group 名称，那么默认为 core，可以使用 kubectl api-versions # 获取当前 k8s 版本上所有的 apiVersion 版本信息( 每个版本可能不同 )
kind:       #资源类别
metadata：  #资源元数据
   name
   namespace
   lables
   annotations   # 主要目的是方便用户阅读查找
spec: # 期望的状态（disired state）
status：# 当前状态，本字段有 Kubernetes 自身维护，用户不能去定义
```

## 资源清单的常用命令

获取 apiversion 版本信息

```bash
[root@k8s-master01 ~]# kubectl api-versions 
admissionregistration.k8s.io/v1beta1
apiextensions.k8s.io/v1beta1
apiregistration.k8s.io/v1
apiregistration.k8s.io/v1beta1
apps/v1
......(以下省略)
```

获取资源的 apiVersion 版本信息

```
[root@k8s-master01 ~]# kubectl explain pod
KIND:     Pod
VERSION:  v1
.....(以下省略)
[root@k8s-master01 ~]# kubectl explain Ingress
KIND:     Ingress
VERSION:  extensions/v1beta1
```

获取字段设置帮助文档 

```
[root@k8s-master01 ~]# kubectl explain pod
KIND:     Pod
VERSION:  v1
DESCRIPTION:
     Pod is a collection of containers that can run on a host. This resource is
     created by clients and scheduled onto hosts.
FIELDS:
   apiVersion    <string>
     ........
     ........
```

字段配置格式

```
apiVersion <string>          #表示字符串类型
metadata <Object>            #表示需要嵌套多层字段
labels <map[string]string>   #表示由k:v组成的映射
finalizers <[]string>        #表示字串列表
ownerReferences <[]Object>   #表示对象列表
hostPID <boolean>            #布尔类型
priority <integer>           #整型
name <string> -required-     #如果类型后面接 -required-，表示为必填字段
```

## 通过定义清单文件创建 Pod【myapp这个是nginx镜像】（这地方有个错误哦，下面讲）

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
    version: v1
spec:
  containers:
  - name: app
    image: wangyanglinux/myapp:v1
  - name: test
    image: wangyanglinux/myapp:v1
```

错误：因为这回事nginx容器，在同一Pod中，只用一个80端口可以，所以，一个会一直报错。看下面截图

【一个在运行，一个在一直报错重启。】

运行Pod.yaml文件

```
kubectl apply -f pod.yaml 
```

**下面看详细步骤解析**

![](http://image.ownit.top/csdn/2020020320455893.png)

**查看Pod的详细信息**

```bash
kubectl describe pod myapp-pod
```

![](http://image.ownit.top/csdn/20200203205310698.png)

**查看Pod的日志**

```
kubectl log myapp-pod -c test
```

![](http://image.ownit.top/csdn/2020020320554467.png)

**删除Pod**

```bash
kubectl delete pod myapp-pod
```

![](http://image.ownit.top/csdn/20200203205912850.png)

**重新编写yaml文件**

```bash
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
    version: v1
spec:
  containers:
  - name: app
    image: wangyanglinux/myapp:v1
```

![](http://image.ownit.top/csdn/20200203210019600.png)

**测速访问**

![](http://image.ownit.top/csdn/20200203210211351.png)