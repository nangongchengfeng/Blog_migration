---
author: 南宫乘风
categories:
- Kubernetes应用
date: 2021-04-02 18:01:08
description: 环境需要使用内核模块，我们可以通过运行来测试节点是否有该模块，如果没有，则需要更新下内核版本。另外需要在节点上安装软件包：安装我们这里部署最新的版本的，部署清单文件地址：。从上面链接中下载与两个资源清。。。。。。。
image: ../../title_pic/20.jpg
slug: '202104021801'
tags:
- kubernetes
- docker
- linux
- 数据库
title: Rook部署测试Ceph和wordpress实战应用
---

<!--more-->

### 环境

Rook Ceph 需要使用 RBD 内核模块，我们可以通过运行 `modprobe rbd` 来测试 Kubernetes 节点是否有该模块，如果没有，则需要更新下内核版本。

另外需要在节点上安装 `lvm2` 软件包：

```
# Centos
sudo yum install -y lvm2

# Ubuntu
sudo apt-get install -y lvm2
```

### 安装

我们这里部署最新的 release-1.2 版本的 Rook，部署清单文件地址：<https://github.com/rook/rook/tree/release-1.2/cluster/examples/kubernetes/ceph>。

从上面链接中下载 common.yaml 与 operator.yaml 两个资源清单文件：<https://github.com/nangongchengfeng/Kubernetes/tree/main/Ceph>（这个是已经整合好的，方便测试）

```bash
# 会安装crd、rbac相关资源对象
$ kubectl apply -f common.yaml
# 安装 rook operator
$ kubectl apply -f operator.yaml
```

在继续操作之前，验证 `rook-ceph-operator` 是否处于`“Running”`状态： 

```bash
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl get pod -n rook-ceph 
NAME                                                 READY   STATUS      RESTARTS   AGE
csi-cephfsplugin-79wcl                               3/3     Running     0          7h28m
csi-cephfsplugin-jmrgs                               3/3     Running     0          7h28m
csi-cephfsplugin-provisioner-85979bcd-cfgqx          4/4     Running     22         7h28m
csi-cephfsplugin-provisioner-85979bcd-pzjsr          4/4     Running     10         7h28m
csi-rbdplugin-j26wk                                  3/3     Running     0          7h28m
csi-rbdplugin-pdbjl                                  3/3     Running     0          7h28m
csi-rbdplugin-provisioner-66f64ff49c-qwhh9           5/5     Running     18         7h28m
csi-rbdplugin-provisioner-66f64ff49c-sq57h           5/5     Running     37         7h28m
rook-ceph-crashcollector-k8s-node1-fcb4cfc96-4fn26   1/1     Running     0          7h26m
rook-ceph-crashcollector-k8s-node2-d97b797b5-mnc2b   1/1     Running     0          7h26m
rook-ceph-mgr-a-5dcbf79d8b-n9j68                     1/1     Running     0          4h49m
rook-ceph-mon-a-75978c9d5b-vhmkx                     1/1     Running     1          7h27m
rook-ceph-mon-b-7955589ff4-fhbb5                     1/1     Running     0          7h26m
rook-ceph-operator-658dfb6cc4-9z5lw                  1/1     Running     13         7h29m
rook-ceph-osd-0-546d474d95-wkn4k                     1/1     Running     0          7h26m
rook-ceph-osd-1-5c7cc4b9d6-g4g7t                     1/1     Running     0          7h26m
rook-ceph-osd-prepare-k8s-node1-6nttm                0/1     Completed   0          140m
rook-ceph-osd-prepare-k8s-node2-jmddp                0/1     Completed   0          140m
rook-ceph-tools-f56f69476-8mnjf                      1/1     Running     0          7h16m
rook-discover-bgcth                                  1/1     Running     0          7h29m
rook-discover-km45k                                  1/1     Running     0          7h29m
```

我们可以看到 Operator 运行成功后，还会有一个 DaemonSet 控制器运行得 rook-discover 应用，当 `Rook Operator` 处于 Running 状态，我们就可以创建 Ceph 集群了。为了使集群在重启后不受影响，请确保设置的 `dataDirHostPath` 属性值为有效得主机路径。更多相关设置，可以查看[集群配置相关文档](https://rook.io/docs/rook/v1.2/ceph-cluster-crd.html)。

创建如下的资源清单文件：\(cluster.yaml\)

```bash
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    # 最新得 ceph 镜像, 可以查看 https://hub.docker.com/r/ceph/ceph/tags
    image: ceph/ceph:v14.2.5
  dataDirHostPath: /var/lib/rook  # 主机有效目录
  mon:
    count: 3
  dashboard:
    enabled: true
  storage:
    useAllNodes: true
    useAllDevices: false
    # 重要: Directories 应该只在预生产环境中使用
    directories:
    - path: /data/rook
```

其中有几个比较重要的字段：

- `dataDirHostPath`：宿主机上的目录，用于每个服务存储配置和数据。如果目录不存在，会自动创建该目录。由于此目录在主机上保留，因此在删除 Pod 后将保留该目录，另外不得使用以下路径及其任何子路径：`/etc/ceph`、`/rook` 或 `/var/log/ceph`。

+ `useAllNodes`：用于表示是否使用集群中的所有节点进行存储，如果在 `nodes` 字段下指定了各个节点，则必须将`useAllNodes`设置为 false。

+ `useAllDevices`：表示 OSD 是否自动使用节点上的所有设备，一般设置为 false，这样可控性较高

+ `directories`：一般来说应该使用一块裸盘来做存储，有时为了测试方便，使用一个目录也是可以的，当然生成环境不推荐使用目录。

除了上面这些字段属性之外还有很多其他可以细粒度控制得参数，可以查看[集群配置相关文档](https://rook.io/docs/rook/v1.2/ceph-cluster-crd.html)。

现在直接创建上面的 `CephCluster` 对象即可：

```bash
$ kubectl apply -f cluster.yaml 
cephcluster.ceph.rook.io/rook-ceph created
```

创建完成后，Rook Operator 就会根据我

### 验证

要验证集群是否处于正常状态，我们可以使用 [Rook 工具箱](https://rook.io/docs/rook/v1.2/ceph-toolbox.html) 来运行 `ceph status` 命令查看。

Rook 工具箱是一个用于调试和测试 Rook 的常用工具容器，该工具基于 CentOS 镜像，所以可以使用 yum 来轻松安装更多的工具包。我们这里用 Deployment 控制器来部署 Rook 工具箱，部署的资源清单文件如下所示：（toolbox.yaml）

们的描述信息去自动创建 Ceph 集群了。

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rook-ceph-tools
  namespace: rook-ceph
  labels:
    app: rook-ceph-tools
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rook-ceph-tools
  template:
    metadata:
      labels:
        app: rook-ceph-tools
    spec:
      dnsPolicy: ClusterFirstWithHostNet
      containers:
      - name: rook-ceph-tools
        image: rook/ceph:v1.2.1
        command: ["/tini"]
        args: ["-g", "--", "/usr/local/bin/toolbox.sh"]
        imagePullPolicy: IfNotPresent
        env:
          - name: ROOK_ADMIN_SECRET
            valueFrom:
              secretKeyRef:
                name: rook-ceph-mon
                key: admin-secret
        securityContext:
          privileged: true
        volumeMounts:
          - mountPath: /dev
            name: dev
          - mountPath: /sys/bus
            name: sysbus
          - mountPath: /lib/modules
            name: libmodules
          - name: mon-endpoint-volume
            mountPath: /etc/rook
      # 如果设置 hostNetwork: false,  "rbd map" 命令会被 hang 住, 参考 https://github.com/rook/rook/issues/2021
      hostNetwork: true
      volumes:
        - name: dev
          hostPath:
            path: /dev
        - name: sysbus
          hostPath:
            path: /sys/bus
        - name: libmodules
          hostPath:
            path: /lib/modules
        - name: mon-endpoint-volume
          configMap:
            name: rook-ceph-mon-endpoints
            items:
            - key: data
              path: mon-endpoints
```

然后直接创建这个 Pod：

```
$ kubectl apply -f toolbox.yaml
deployment.apps/rook-ceph-tools created
```

一旦 toolbox 的 Pod 运行成功后，我们就可以使用下面的命令进入到工具箱内部进行操作：

```
$ kubectl -n rook-ceph exec -it $(kubectl -n rook-ceph get pod -l "app=rook-ceph-tools" -o jsonpath='{.items[0].metadata.name}') bash
```

 

工具箱中的所有可用工具命令均已准备就绪，可满足您的故障排除需求。例如：

```
ceph status
ceph osd status
ceph df
rados df
```

 

比如现在我们要查看集群的状态，需要满足下面的条件才认为是健康的：

 -    所有 mons 应该达到法定数量
 -    mgr 应该是激活状态
 -    至少有一个 OSD 处于激活状态
 -    如果不是 HEALTH\_OK 状态，则应该查看告警或者错误信息

```
$ ceph status
ceph status
  cluster:
    id:     dae083e6-8487-447b-b6ae-9eb321818439
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum a,b,c (age 15m)
    mgr: a(active, since 2m)
    osd: 31 osds: 2 up (since 6m), 2 in (since 6m)

  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   79 GiB used, 314 GiB / 393 GiB avail
    pgs:
```

如果群集运行不正常，可以查看 [Ceph 常见问题](https://rook.io/docs/rook/v1.2/ceph-common-issues.html)以了解更多详细信息和可能的解决方案。

### Dashboard

Ceph 有一个 Dashboard 工具，我们可以在上面查看集群的状态，包括总体运行状态，mgr、osd 和其他 Ceph 进程的状态，查看池和 PG 状态，以及显示守护进程的日志等等。

我们可以在上面的 cluster CRD 对象中开启 dashboard，设置`dashboard.enable=true`即可，这样 Rook Operator 就会启用 ceph-mgr dashboard 模块，并将创建一个 Kubernetes Service 来暴露该服务，将启用端口 7000 进行 https 访问，如果 Ceph 集群部署成功了，我们可以使用下面的命令来查看 Dashboard 的 Service：

```
$ kubectl get svc -n rook-ceph
NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
rook-ceph-mgr              ClusterIP   10.99.87.1       <none>        9283/TCP            3m6s
rook-ceph-mgr-dashboard    ClusterIP   10.111.195.180   <none>        7000/TCP            3m29s
```

 

这里的 rook-ceph-mgr 服务用于报告 Prometheus metrics 指标数据的，而后面的的 rook-ceph-mgr-dashboard 服务就是我们的 Dashboard 服务，如果在集群内部我们可以通过 DNS 名称 `http://rook-ceph-mgr-dashboard.rook-ceph:7000`或者 CluterIP `http://10.111.195.180:7000` 来进行访问，但是如果要在集群外部进行访问的话，我们就需要通过 Ingress 或者 NodePort 类型的 Service 来暴露了，为了方便测试我们这里创建一个新的 NodePort 类型的服务来访问 Dashboard，资源清单如下所示：（dashboard-external.yaml）

```
apiVersion: v1
kind: Service
metadata:
  name: rook-ceph-mgr-dashboard-external
  namespace: rook-ceph
  labels:
    app: rook-ceph-mgr
    rook_cluster: rook-ceph
spec:
  ports:
  - name: dashboard
    port: 7000
    protocol: TCP
    targetPort: 7000
  selector:
    app: rook-ceph-mgr
    rook_cluster: rook-ceph
  type: NodePort
```

 

同样直接创建即可：

```
$ kubectl apply -f dashboard-external.yaml
```

 

创建完成后我们可以查看到新创建的 rook-ceph-mgr-dashboard-external 这个 Service 服务：

```
$ kubectl get svc -n rook-ceph 
NAME                                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
rook-ceph-mgr                           ClusterIP   10.96.49.29     <none>        9283/TCP            23m
rook-ceph-mgr-dashboard                 ClusterIP   10.109.8.98     <none>        7000/TCP            23m
rook-ceph-mgr-dashboard-external   NodePort    10.109.53.223    <none>        7000:31361/TCP      14s
```

 

现在我们需要通过 `http://<NodeIp>:31361` 就可以访问到 Dashboard 了。

但是在访问的时候需要我们登录才能够访问，Rook 创建了一个默认的用户 admin，并在运行 Rook 的命名空间中生成了一个名为 `rook-ceph-dashboard-admin-password` 的 Secret，要获取密码，可以运行以下命令：

```
$ kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
xxxx（登录密码）
```

 

用上面获得的密码和用户名 admin 就可以登录 Dashboard 了，在 Dashboard 上面可以查看到整个集群的状态：

![ceph dashboard](../../image/5be64fa889b70b6a38f230dc179f87ab.png)

## 使用

现在我们的 Ceph 集群搭建成功了，我们就可以来使用存储了。首先我们需要创建存储池，可以用 CRD 来定义 Pool。Rook 提供了两种机制来维持 OSD：

- 副本：缺省选项，每个对象都会根据 `spec.replicated.size` 在多个磁盘上进行复制。建议非生产环境至少 2 个副本，生产环境至少 3 个。
- Erasure Code：是一种较为节约的方式。EC 把数据拆分 n 段（`spec.erasureCoded.dataChunks`），再加入 k 个代码段（`spec.erasureCoded.codingChunks`），用分布的方式把 `n+k` 段数据保存在磁盘上。这种情况下 Ceph 能够隔离 k 个 OSD 的损失。

我们这里使用副本的方式，创建如下所示的 RBD 类型的存储池：\(pool.yaml\)

```
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata:
  name: k8s-test-pool   # operator会监听并创建一个pool，执行完后界面上也能看到对应的pool
  namespace: rook-ceph
spec:
  failureDomain: host  # 数据块的故障域: 值为host时，每个数据块将放置在不同的主机上;值为osd时，每个数据块将放置在不同的osd上
  replicated:
    size: 3   # 池中数据的副本数,1就是不保存任何副本
```

 

直接创建上面的资源对象：

```
$ kubectl apply -f pool.yaml 
cephblockpool.ceph.rook.io/k8s-test-pool created
```

 

存储池创建完成后我们在 Dashboard 上面的确可以看到新增了一个 pool，但是会发现集群健康状态变成了 `WARN`，我们可以查看到有如下日志出现：

```
Health check update: too few PGs per OSD (6 < min 30) (TOO_FEW_PGS)
```

 

这是因为每个 osd 上的 pg 数量小于最小的数目30个。pgs 为8，因为是3副本的配置，所以当有4个 osd 的时候，每个 osd 上均分了8/4 \*3=6个pgs，也就是出现了如上的错误小于最小配置30个，集群这种状态如果进行数据的存储和操作，集群会卡死，无法响应io，同时会导致大面积的 osd down。

我们可以进入 toolbox 的容器中查看上面存储的 pg 数量：

```
$ ceph osd pool get k8s-test-pool pg_num
pg_num: 8
```

 

我们可以通过增加 pg\_num 来解决这个问题：

```
$ ceph osd pool set k8s-test-pool pg_num 64
set pool 1 pg_num to 64
$ ceph -s
  cluster:
    id:     7851387c-5d18-489a-8c04-b699fb9764c0
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum a,b,c (age 33m)
    mgr: a(active, since 32m)
    osd: 4 osds: 4 up (since 32m), 4 in (since 32m)

  data:
    pools:   1 pools, 64 pgs
    objects: 0 objects, 0 B
    usage:   182 GiB used, 605 GiB / 787 GiB avail
    pgs:     64 active+clean
```

 

这个时候我们再查看就可以看到现在就是健康状态了。不过需要注意的是我们这里的 pool 上没有数据，所以修改 pg 影响并不大，但是如果是生产环境重新修改 pg 数，会对生产环境产生较大影响。因为 pg 数变了，就会导致整个集群的数据重新均衡和迁移，数据越大响应 io 的时间会越长。所以，最好在一开始就设置好 pg 数。

现在我们来创建一个 StorageClass 来进行动态存储配置，如下所示我们定义一个 Ceph 的块存储的 StorageClass：\(storageclass.yaml\)

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-ceph-block
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  # clusterID 是 rook 集群运行的命名空间
  clusterID: rook-ceph

  # 指定存储池
  pool: k8s-test-pool

  # RBD image (实际的存储介质) 格式. 默认为 "2".
  imageFormat: "2"

  # RBD image 特性. CSI RBD 现在只支持 `layering` .
  imageFeatures: layering

  # Ceph 管理员认证信息，这些都是在 clusterID 命名空间下面自动生成的
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
  # 指定 volume 的文件系统格式，如果不指定, csi-provisioner 会默认设置为 `ext4`
  csi.storage.k8s.io/fstype: ext4
# uncomment the following to use rbd-nbd as mounter on supported nodes
# **IMPORTANT**: If you are using rbd-nbd as the mounter, during upgrade you will be hit a ceph-csi
# issue that causes the mount to be disconnected. You will need to follow special upgrade steps
# to restart your application pods. Therefore, this option is not recommended.
#mounter: rbd-nbd
reclaimPolicy: Delete
```

 

直接创建上面的 StorageClass 资源对象：

```
$ kubectl apply -f storageclass.yaml 
storageclass.storage.k8s.io/rook-ceph-block created
$ kubectl get storageclass
NAME              PROVISIONER                    AGE
rook-ceph-block   rook-ceph.rbd.csi.ceph.com     35s
```

 

然后创建一个 PVC 来使用上面的 StorageClass 对象：\(pvc.yaml\)

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  labels:
    app: wordpress
spec:
  storageClassName: rook-ceph-block
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```

 

同样直接创建上面的 PVC 资源对象：

```
$ kubectl apply -f pvc.yaml 
persistentvolumeclaim/mysql-pv-claim created
$ kubectl get pvc -l app=wordpress
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
mysql-pv-claim   Bound    pvc-1eab82e3-d214-4d8e-8fcc-ed379c24e0e3   20Gi       RWO            rook-ceph-block   32m
```

 

创建完成后我们可以看到我们的 PVC 对象已经是 Bound 状态了，自动创建了对应的 PV，然后我们就可以直接使用这个 PVC 对象来做数据持久化操作了。

这个时候可能集群还会出现如下的健康提示：

```
$ ceph health detail
HEALTH_WARN application not enabled on 1 pool(s)
POOL_APP_NOT_ENABLED application not enabled on 1 pool(s)
    application not enabled on pool 'k8s-test-pool'
    use 'ceph osd pool application enable <pool-name> <app-name>', where <app-name> is 'cephfs', 'rbd', 'rgw', or freeform for custom applications.
$ ceph osd pool application enable k8s-test-pool k8srbd
enabled application 'k8srbd' on pool 'k8s-test-pool'
```

 

根据提示启用一个 application 即可。

在官方仓库 [cluster/examples/kubernetes](https://github.com/rook/rook/tree/release-1.2/cluster/examples/kubernetes) 目录下，官方给了个 wordpress 的例子，可以直接运行测试即可：

```
$ kubectl apply -f mysql.yaml
$ kubectl apply -f wordpress.yaml  
```

 

官方的这个示例里面的 wordpress 用的 Loadbalancer 类型，我们可以改成 NodePort：

```
$ kubectl get pvc -l app=wordpress
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
mysql-pv-claim   Bound    pvc-1eab82e3-d214-4d8e-8fcc-ed379c24e0e3   20Gi       RWO            rook-ceph-block   12h
wp-pv-claim      Bound    pvc-237932ed-5ca7-468c-bd16-220ebb2a1ce3   20Gi       RWO            rook-ceph-block   25s
$ kubectl get pods -l app=wordpress               
NAME                              READY   STATUS    RESTARTS   AGE
wordpress-5b886cf59b-4xwn8        1/1     Running   0          24m
wordpress-mysql-b9ddd6d4c-qhjd4   1/1     Running   0          24m
$ kubectl get svc -l app=wordpress
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
wordpress         NodePort    10.106.253.225   <none>        80:30307/TCP   80s
wordpress-mysql   ClusterIP   None             <none>        3306/TCP       87s
```

![](../../image/20210402180045917.png)

当应用都处于 Running 状态后，我们可以通过 `http://<任意节点IP>:30307` 去访问 wordpress 应用：

 

比如我们在第一篇文章中更改下内容，然后我们将应用 Pod 全部删除重建：

```
$ kubectl delete pod wordpress-mysql-b9ddd6d4c-qhjd4 wordpress-5b886cf59b-4xwn8
pod "wordpress-mysql-b9ddd6d4c-qhjd4" deleted
pod "wordpress-5b886cf59b-4xwn8" deleted
$ kubectl get pods -l app=wordpress                                            
NAME                              READY   STATUS    RESTARTS   AGE
wordpress-5b886cf59b-kwxk4        1/1     Running   0          2m52s
wordpress-mysql-b9ddd6d4c-kkcr7   1/1     Running   0          2m52s
```

 

当 Pod 重建完成后再次访问 wordpress 应用的主页我们可以发现之前我们添加的数据仍然存在，这就证明我们的数据持久化是正确的。

 

原文地址：<https://www.qikqiak.com/k8strain/storage/ceph/>