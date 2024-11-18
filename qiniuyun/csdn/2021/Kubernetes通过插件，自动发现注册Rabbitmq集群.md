---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-11 10:58:13
description: 是实现了高级消息队列协议的开源消息代理软件亦称面向消息的中间件可伸缩性：集群服务消息持久化：从内存持久化消息到硬盘，再从硬盘加载到内存工作中，我们经常使用到，有单节点，有集群的。通过该来安装，通过插来。。。。。。。
image: ../../title_pic/67.jpg
slug: '202103111058'
tags:
- Kubernetes应用
- 中间件
- 可视化
- rabbitmq
- kubernetes
- docker
title: Kubernetes通过插件，自动发现注册Rabbitmq集群
---

<!--more-->

**RabbitMQ**是实现了高级消息队列协议（AMQP）的开源消息代理软件（亦称面向消息的中间件）

- 可伸缩性：集群服务

- 消息持久化：从内存持久化消息到硬盘，再从硬盘加载到内存 

 

工作中，我们经常使用到Rabbitmq，有单节点，有集群的。

通过该Kubernetes来安装RabbitMQ，通过插【rabbitmq\_management,rabbitmq\_peer\_discovery\_k8s】来自动发现注册集群：

RabbitMQ通过StatefulSet来部署，可以通过域名来访问，方便处理

![](../../image/20210311094106956.png)

![](../../image/20210311094255588.png)

 

## （1）环境

需要Kubernetes集群

下载部署文件

```bash
下载地址：https://github.com/dotbalo/k8s/tree/master/k8s-rabbitmq-cluster
```

![](../../image/20210311094814793.png)

 

## （2）创建命名空间

```bash
kubectl create ns public-service
```

如果不使用public-service，需要更改所有yaml文件的public-service为你namespace。

```bash
sed -i "s#public-service#YOUR_NAMESPACE#g" *.yaml
```

## （3）修改配置文件

```bash
在rabbitmq-configmap.yaml配置，添加这两个字段，解决密码不生效的问题
      default_pass = RABBITMQ_PASS
      default_user = RABBITMQ_USER
```

![](../../image/20210311100213362.png)

这边PV是使用nfs的。测试环境，这边我是手动创建的，也可以使用插件，自动创建，并回收。

```bash
[root@k8s-master01 k8s-rabbitmq-cluster]# cat rabbitmq-pv.yaml 
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-rmq-1
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: "rmq-storage-class"
  nfs:
    # real share directory
    path: /ifs/kubernetts/rabbitmq-cluster-0
    # nfs real ip
    server: 192.168.0.109

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-rmq-2
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: "rmq-storage-class"
  nfs:
    # real share directory
    path: /ifs/kubernetts/rabbitmq-cluster-1
    # nfs real ip
    server: 192.168.0.109

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-rmq-3
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: "rmq-storage-class"
  nfs:
    # real share directory
    path: /ifs/kubernetts/rabbitmq-cluster-2
    # nfs real ip
    server: 192.168.0.109
```

## （4）创建集群

```bash
[root@k8s-master01 k8s-rabbitmq-cluster]# kubectl apply -f .
statefulset.apps/rmq-cluster created
configmap/rmq-cluster-config created
persistentvolume/pv-rmq-1 created
persistentvolume/pv-rmq-2 created
persistentvolume/pv-rmq-3 created
serviceaccount/rmq-cluster created
role.rbac.authorization.k8s.io/rmq-cluster created
rolebinding.rbac.authorization.k8s.io/rmq-cluster created
secret/rmq-cluster-secret created
service/rmq-cluster created
service/rmq-cluster-balancer created
```

## 查看容器日志，显示这个就是正常的

```bash
kubectl logs -f rmq-cluster-0    -n public-service 
'/etc/rabbitmq/rabbitmq.conf' -> '/var/lib/rabbitmq/rabbitmq.conf'
2021-03-11 02:24:03.469 [info] <0.9.0> Feature flags: list of feature flags found:
2021-03-11 02:24:03.469 [info] <0.9.0> Feature flags: feature flag states written to 
。。。。。。。。。。。。。。。
。。。。。。。。。。。。。。。
2021-03-11 02:24:04.273 [info] <0.692.0> Statistics database started.
2021-03-11 02:24:04.274 [info] <0.691.0> Starting worker pool 'management_worker_pool' with 3 processes in it
 completed with 5 plugins.
2021-03-11 02:24:04.411 [info] <0.9.0> Server startup complete; 5 plugins started.
 * rabbitmq_management
 * rabbitmq_management_agent
 * rabbitmq_web_dispatch
 * rabbitmq_peer_discovery_k8s
 * rabbitmq_peer_discovery_common
2021-03-11 02:24:23.135 [info] <0.434.0> node 'rabbit@rmq-cluster-1.rmq-cluster.public-service.svc.cluster.local' up
2021-03-11 02:24:23.904 [info] <0.434.0> rabbit on node 'rabbit@rmq-cluster-1.rmq-cluster.public-service.svc.cluster.local' up
2021-03-11 02:24:44.524 [info] <0.434.0> node 'rabbit@rmq-cluster-2.rmq-cluster.public-service.svc.cluster.local' up
2021-03-11 02:24:45.477 [info] <0.434.0> rabbit on node 'rabbit@rmq-cluster-2.rmq-cluster.public-service.svc.cluster.local' up
```

创建资源如下

```bash
[root@k8s-master01 ~]# kubectl get pod,sts,svc,ep,pv,pvc -n public-service 
NAME                READY   STATUS    RESTARTS   AGE
pod/rmq-cluster-0   1/1     Running   0          8m10s
pod/rmq-cluster-1   1/1     Running   0          7m34s
pod/rmq-cluster-2   1/1     Running   0          7m18s

NAME                           READY   AGE
statefulset.apps/rmq-cluster   3/3     8m11s

NAME                           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                          AGE
service/rmq-cluster            ClusterIP   None           <none>        5672/TCP                         8m11s
service/rmq-cluster-balancer   NodePort    10.96.58.102   <none>        15672:31824/TCP,5672:31993/TCP   8m11s

NAME                             ENDPOINTS                                                              AGE
endpoints/rmq-cluster            10.244.32.129:5672,10.244.58.225:5672,10.244.85.246:5672               8m11s
endpoints/rmq-cluster-balancer   10.244.32.129:5672,10.244.58.225:5672,10.244.85.246:5672 + 3 more...   8m11s

NAME                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                           STORAGECLASS        REASON   AGE
persistentvolume/pv-rmq-1   1Gi        RWX            Recycle          Bound    public-service/rabbitmq-storage-rmq-cluster-2   rmq-storage-class            8m11s
persistentvolume/pv-rmq-2   1Gi        RWX            Recycle          Bound    public-service/rabbitmq-storage-rmq-cluster-1   rmq-storage-class            8m11s
persistentvolume/pv-rmq-3   1Gi        RWX            Recycle          Bound    public-service/rabbitmq-storage-rmq-cluster-0   rmq-storage-class            8m11s
persistentvolume/pv0001     2Gi        RWO            Recycle          Bound    default/test-pvc2                               slow                         9d

NAME                                                   STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS        AGE
persistentvolumeclaim/rabbitmq-storage-rmq-cluster-0   Bound    pv-rmq-3   1Gi        RWX            rmq-storage-class   8m11s
persistentvolumeclaim/rabbitmq-storage-rmq-cluster-1   Bound    pv-rmq-2   1Gi        RWX            rmq-storage-class   7m34s
persistentvolumeclaim/rabbitmq-storage-rmq-cluster-2   Bound    pv-rmq-1   1Gi        RWX            rmq-storage-class   7m18s
[root@k8s-master01 ~]# 
```

## （5）验证集群

可以通过svc的nodeport端口暴露，或者ingress来访问rabbitmq可视化界面

![](../../image/20210311103353828.png)

![](../../image/20210311103342131.png)

```bash

      default_user = RABBITMQ_USER   #账号
      default_pass = RABBITMQ_PASS   #密码
```

## （6）集群扩容，缩容

扩容，如果使用的pv，建议查看pv是否够，不然状态一直是pending

```bash
kubectl scale statefulset -n public-service --replicas=4 rmq-cluster

--replicas=4   改这个值，就可以用来扩容和缩容
```

![](../../image/20210311104053402.png)

![](../../image/20210311105422245.png)

![](../../image/20210311105503765.png)

![](../../image/20210311105728953.png)

<https://github.com/dotbalo/k8s/tree/master/k8s-rabbitmq-cluster>