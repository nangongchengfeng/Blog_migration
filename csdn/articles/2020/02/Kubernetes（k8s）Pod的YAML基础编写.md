+++
author = "南宫乘风"
title = "Kubernetes（k8s）Pod的YAML基础编写"
date = "2020-02-03 21:02:49"
tags=['Yaml', 'Kubernetes', 'pod', 'k8s']
categories=[]
image = "post/4kdongman/84.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104161525](https://blog.csdn.net/heian_99/article/details/104161525)

**Kubernetes中的Pod一般都是采用yaml编写**

```
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

```
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
   apiVersion    &lt;string&gt;
     ........
     ........

```

字段配置格式

```
apiVersion &lt;string&gt;          #表示字符串类型
metadata &lt;Object&gt;            #表示需要嵌套多层字段
labels &lt;map[string]string&gt;   #表示由k:v组成的映射
finalizers &lt;[]string&gt;        #表示字串列表
ownerReferences &lt;[]Object&gt;   #表示对象列表
hostPID &lt;boolean&gt;            #布尔类型
priority &lt;integer&gt;           #整型
name &lt;string&gt; -required-     #如果类型后面接 -required-，表示为必填字段

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

![2020020320455893.png](https://img-blog.csdnimg.cn/2020020320455893.png)

**查看Pod的详细信息**

```
kubectl describe pod myapp-pod

```

![20200203205310698.png](https://img-blog.csdnimg.cn/20200203205310698.png)

**查看Pod的日志**

```
kubectl log myapp-pod -c test

```

![2020020320554467.png](https://img-blog.csdnimg.cn/2020020320554467.png)

**删除Pod**

```
kubectl delete pod myapp-pod
```

![20200203205912850.png](https://img-blog.csdnimg.cn/20200203205912850.png)

**重新编写yaml文件**

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

```

![20200203210019600.png](https://img-blog.csdnimg.cn/20200203210019600.png)

**测速访问**

![20200203210211351.png](https://img-blog.csdnimg.cn/20200203210211351.png)
