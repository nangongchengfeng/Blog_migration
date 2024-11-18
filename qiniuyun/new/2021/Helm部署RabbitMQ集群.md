---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-14 17:37:25
description: 帮助您管理应用程序帮助您定义、安装和升级最复杂的应用程序。可以使用启动集群，提供可用的工作流：一个集群一个数据库一个边界负载均衡特性：查找并使用流行的软件，将其打包为，以便在中运行以的形式共享您自己的。。。。。。。
image: http://image.ownit.top/4kdongman/73.jpg
tags:
- docker
- kubernetes
- helm
- linux
title: Helm部署RabbitMQ集群
---

<!--more-->

**Helm** 帮助您管理 Kubernetes 应用程序——Helm Charts 帮助您定义、安装和升级最复杂的 Kubernetes 应用程序。

Helm 可以使用 Charts 启动 Kubernetes 集群，提供可用的工作流：

- 一个 Redis 集群

- 一个 Postgres 数据库

- 一个 HAProxy 边界负载均衡

特性：

- 查找并使用流行的软件，将其打包为 Helm Charts，以便在 Kubernetes 中运行
- 以 Helm Charts 的形式共享您自己的应用程序
- 为您的 Kubernetes 应用程序创建可复制的构建
- 智能地管理您的 Kubernetes 清单文件
- 管理 Helm 包的发行版

 

### helm的安装

官方文档：<https://helm.sh/docs/intro/install/>

版本下载地址：<https://github.com/helm/helm/releases>

```bash
tar -zxvf helm-v3.0.0-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin/helm

已经安装完成

[root@k8s-master01 ~]# helm version
version.BuildInfo{Version:"v3.5.3", GitCommit:"041ce5a2c17a58be0fcd5f5e16fb3e7e95fea622", GitTreeState:"dirty", GoVersion:"go1.15.8"}
```

至于怎么添加仓库，可以百度

```bash
[root@k8s-master01 ~]# helm repo list 
NAME         	URL                                                   
aliyuncs     	https://apphub.aliyuncs.com                           
stable       	https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
ingress-nginx	https://kubernetes.github.io/ingress-nginx 
```

###  查看可使用tabbitmq-ha的版本

```bash
[root@k8s-master01 ~]# helm search repo rabbitmq-ha 
NAME                	CHART VERSION	APP VERSION	DESCRIPTION                                       
aliyuncs/rabbitmq-ha	1.39.0       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
stable/rabbitmq-ha  	1.0.0        	3.7.3      	Highly available RabbitMQ cluster, the open sou...
[root@k8s-master01 ~]# helm search repo rabbitmq-ha --versions
NAME                	CHART VERSION	APP VERSION	DESCRIPTION                                       
aliyuncs/rabbitmq-ha	1.39.0       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.38.2       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.38.1       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.36.4       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.36.3       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.36.0       	3.8.0      	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.34.1       	3.7.19     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.34.0       	3.7.19     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.33.0       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.32.4       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.32.3       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.32.2       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.32.0       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.31.0       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.30.0       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.29.1       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.29.0       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.28.0       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.27.2       	3.7.15     	Highly available RabbitMQ cluster, the open sou...
aliyuncs/rabbitmq-ha	1.27.1       	3.7.12     	Highly available RabbitMQ cluster, the open sou...
stable/rabbitmq-ha  	1.0.0        	3.7.3      	Highly available RabbitMQ cluster, the open sou...
stable/rabbitmq-ha  	0.1.1        	3.7.0      	Highly available RabbitMQ cluster, the open sou...
```

### 拉去指定版本的配置

```bash
[root@k8s-master01 ~]# helm pull aliyuncs/rabbitmq-ha --version=1.33.0
[root@k8s-master01 ~]# ls
helm  old  rabbitmq-cluster  rabbitmq-ha-1.33.0.tgz #这个就只拉去的文件，可以解压
```

### 查询配置文件

```bash
[root@k8s-master01 ~]# tar -xf rabbitmq-ha-1.33.0.tgz 
[root@k8s-master01 ~]# ls
helm  old  rabbitmq-cluster  rabbitmq-ha  rabbitmq-ha-1.33.0.tgz
[root@k8s-master01 ~]# tree rabbitmq-ha
rabbitmq-ha
├── Chart.yaml
├── OWNERS
├── README.md
├── templates
│   ├── alerts.yaml
│   ├── configmap.yaml
│   ├── _helpers.tpl
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── pdb.yaml
│   ├── rolebinding.yaml
│   ├── role.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── service-discovery.yaml
│   ├── servicemonitor.yaml
│   ├── service.yaml
│   └── statefulset.yaml
└── values.yaml

1 directory, 18 files

```

参考

```bash


├── charts # 依赖文件
├── Chart.yaml # 这个chart的版本信息
├── templates #模板
│   ├── deployment.yaml
│   ├── _helpers.tpl # 自定义的模板或者函数
│   ├── ingress.yaml
│   ├── NOTES.txt #这个chart的信息
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml #配置全局变量或者一些参数
```

### 创建namespaces

helm指定namespaces，如果没有namespaces空间，就会报错。需要提前创建

```bash
[root@k8s-master01 ~]# helm create rabbitmq-cluster
Creating rabbitmq-cluster
```

### 运行rabbitmq集群

![](http://image.ownit.top/csdn/20210314172044985.png)

镜像配置方面，可以修改values.yaml

 

```bash
[root@k8s-master01 rabbitmq-ha]# pwd
/root/rabbitmq-ha
[root@k8s-master01 rabbitmq-ha]# ls
Chart.yaml  OWNERS  README.md  templates  values.yaml
[root@k8s-master01 rabbitmq-ha]# helm install rabbitmq --namespace  rabbitmq-cluster --set ingress.enabled=true,ingress.hostName=rabbitmq.akiraka.net --set rabbitmqUsername=aka,rabbitmqPassword=rabbitmq,managementPassword=rabbitmq,rabbitmqErlangCookie=secretcookie .
NAME: rabbitmq
LAST DEPLOYED: Sun Mar 14 17:25:11 2021
NAMESPACE: rabbitmq-cluster
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
** Please be patient while the chart is being deployed **

  Credentials:

    Username            : aka
    Password            : $(kubectl get secret --namespace rabbitmq-cluster rabbitmq-rabbitmq-ha -o jsonpath="{.data.rabbitmq-password}" | base64 --decode)
    Management username : management
    Management password : $(kubectl get secret --namespace rabbitmq-cluster rabbitmq-rabbitmq-ha -o jsonpath="{.data.rabbitmq-management-password}" | base64 --decode)
    ErLang Cookie       : $(kubectl get secret --namespace rabbitmq-cluster rabbitmq-rabbitmq-ha -o jsonpath="{.data.rabbitmq-erlang-cookie}" | base64 --decode)

  RabbitMQ can be accessed within the cluster on port 5672 at rabbitmq-rabbitmq-ha.rabbitmq-cluster.svc.cluster.local

  To access the cluster externally execute the following commands:

    export POD_NAME=$(kubectl get pods --namespace rabbitmq-cluster -l "app=rabbitmq-ha" -o jsonpath="{.items[0].metadata.name}")
    kubectl port-forward $POD_NAME --namespace rabbitmq-cluster 5672:5672 15672:15672

  To Access the RabbitMQ AMQP port:

    amqp://127.0.0.1:5672/ 

  To Access the RabbitMQ Management interface:

    URL : http://127.0.0.1:15672
[root@k8s-master01 rabbitmq-ha]# 
```

### 查看集群

已经正常运行起来了

```bash
[root@k8s-master01 rabbitmq-ha]# kubectl get svc,pod,ingress -n rabbitmq-cluster  
NAME                                     TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                       AGE
service/rabbitmq-rabbitmq-ha             ClusterIP   None         <none>        15672/TCP,5672/TCP,4369/TCP   7m23s
service/rabbitmq-rabbitmq-ha-discovery   ClusterIP   None         <none>        15672/TCP,5672/TCP,4369/TCP   7m23s

NAME                         READY   STATUS    RESTARTS   AGE
pod/rabbitmq-rabbitmq-ha-0   1/1     Running   0          7m23s
pod/rabbitmq-rabbitmq-ha-1   1/1     Running   0          6m56s
pod/rabbitmq-rabbitmq-ha-2   1/1     Running   0          6m34s

NAME                                      CLASS    HOSTS                  ADDRESS        PORTS   AGE
ingress.extensions/rabbitmq-rabbitmq-ha   <none>   rabbitmq.akiraka.net   10.96.107.62   80      7m23s
```

![](http://image.ownit.top/csdn/20210314173345427.png)

![](http://image.ownit.top/csdn/20210314173452536.png)

很方便的，几个命令就完成集群的部署

 

### 补充

```
helm install helm-test2 --set fullnameOverride=aaaaaaa --dry-run .
这个是模拟运行，懂的人都懂（带值）
```

```
删除helm uninstall rabbitmq-cluster -n public-service  # helm v3 --keep-history
	helm delete/del NAME --purge 
升级helm upgrade rabbitmq-cluster -n public-service .
```

 

卸载保留历史记录

```bash
[root@k8s-master01 rabbitmq-ha]# helm  uninstall rabbitmq -n rabbitmq-cluster --keep-history 
release "rabbitmq" uninstalled
[root@k8s-master01 rabbitmq-ha]# helm list  -n rabbitmq-cluster 
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
[root@k8s-master01 rabbitmq-ha]# helm list  
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
[root@k8s-master01 rabbitmq-ha]# helm  ls
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
[root@k8s-master01 rabbitmq-ha]#  helm status rabbitmq -n rabbitmq-cluster
NAME: rabbitmq
LAST DEPLOYED: Sun Mar 14 17:25:11 2021
NAMESPACE: rabbitmq-cluster
STATUS: uninstalled
REVISION: 1
TEST SUITE: None
NOTES:
** Please be patient while the chart is being deployed **

  Credentials:

    Username            : aka
    Password            : $(kubectl get secret --namespace rabbitmq-cluster rabbitmq-rabbitmq-ha -o jsonpath="{.data.rabbitmq-password}" | base64 --decode)
    Management username : management
    Management password : $(kubectl get secret --namespace rabbitmq-cluster rabbitmq-rabbitmq-ha -o jsonpath="{.data.rabbitmq-management-password}" | base64 --decode)
    ErLang Cookie       : $(kubectl get secret --namespace rabbitmq-cluster rabbitmq-rabbitmq-ha -o jsonpath="{.data.rabbitmq-erlang-cookie}" | base64 --decode)

  RabbitMQ can be accessed within the cluster on port 5672 at rabbitmq-rabbitmq-ha.rabbitmq-cluster.svc.cluster.local

  To access the cluster externally execute the following commands:

    export POD_NAME=$(kubectl get pods --namespace rabbitmq-cluster -l "app=rabbitmq-ha" -o jsonpath="{.items[0].metadata.name}")
    kubectl port-forward $POD_NAME --namespace rabbitmq-cluster 5672:5672 15672:15672

  To Access the RabbitMQ AMQP port:

    amqp://127.0.0.1:5672/ 

  To Access the RabbitMQ Management interface:

    URL : http://127.0.0.1:15672
```