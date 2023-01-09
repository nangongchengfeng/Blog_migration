+++
author = "南宫乘风"
title = "Helm（bitnami）部署zookeeper和kafka集群"
date = "2021-03-15 16:57:54"
tags=['kafka', 'docker', 'linux', 'centos']
categories=['Kubernetes', ' Kubernetes应用']
image = "post/4kdongman/57.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/114840056](https://blog.csdn.net/heian_99/article/details/114840056)

首先介绍一下bitnami

**BitNami**是一个开源项目，该项目产生的开源软件包括安装 Web应用程序和解决方案堆栈，以及虚拟设备（通俗易懂的说：就是封装好各种应用包，提供人们使用。）

我们平时要部署一套高可用集群，大部分都是找到模板，没必要重复造轮子。**BitNami就是提供轮子的。**

 bitnami官方地址：  [https://bitnami.com/](https://bitnami.com/)

这次我们创建部署zookeeper和kafka集群，采取bitnami提供helm仓库，进行安装和部署。

不懂Helm的可以看看 [Helm部署RabbitMQ集群](https://blog.csdn.net/heian_99/article/details/114763052)，提供参考

部署安装文档：[https://docs.bitnami.com/tutorials/deploy-scalable-kafka-zookeeper-cluster-kubernetes](https://docs.bitnami.com/tutorials/deploy-scalable-kafka-zookeeper-cluster-kubernetes)

### helm添加**BitNami仓库**

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

### 部署zookeeper集群

```
helm install zookeeper bitnami/zookeeper 
  --set replicaCount=3 
  --set auth.enabled=false 
  --set allowAnonymousLogin=true
```

### 部署kafka集群

```
helm install kafka bitnami/kafka 
  --set zookeeper.enabled=false 
  --set replicaCount=3
  --set externalZookeeper.servers=ZOOKEEPER-SERVICE-NAME
```

查看kafka集群，连接zookeeper

![f5ef96ca56468ab510b3e66234c8ea97.png](https://img-blog.csdnimg.cn/img_convert/f5ef96ca56468ab510b3e66234c8ea97.png)

 

### 扩容和缩容

修改下面这个参数，重新运行。

```
--set replicaCount=7
```

 

如果遇到拉去镜像失败，这可以使用以下的镜像源

[https://www.daocloud.io/mirror](https://www.daocloud.io/mirror)

```
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://f1361db2.m.daocloud.io
```

```
[root@k8s-master01 kafka]# cat /etc/docker/daemon.json
{
  "registry-mirrors": ["http://f1361db2.m.daocloud.io"]
}

```

 
