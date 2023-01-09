+++
author = "南宫乘风"
title = "Kubernetes使用operator安装Redis集群"
date = "2021-03-09 21:43:40"
tags=['kubernetes', 'docker', 'redis', 'github', 'git']
categories=['Kubernetes']
image = "post/4kdongman/97.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/114601309](https://blog.csdn.net/heian_99/article/details/114601309)

## 通过operator部署redis集群

operator部署有状态的应用会简单很多

![20210225160104777.png](https://img-blog.csdnimg.cn/20210225160104777.png)

 

github文档：[https://github.com/ucloud/redis-cluster-operator#deploy-redis-cluster-operator](https://github.com/ucloud/redis-cluster-operator#deploy-redis-cluster-operator)

Redis Cluster Operator在Kubernetes上管理Redis-Cluster集群

每个主节点及其从节点都由statefulSet管理，为每个statefulSet创建无头svc，并为所有节点创建clusterIP服务。<br> 每个有状态集都使用PodAntiAffinity来确保主节点和从节点分散在不同的节点上。同时，当操作员在每个有状态集中选择主节点时，它会优先选择具有不同k8s节点的容器作为主节点。

### （1）下载redis-cluster-operator

```
git  clone  https://github.com/ucloud/redis-cluster-operator.git
```

在名称空间：redis-cluster下部署Redis集群，注意修改yaml文件的namespace参数<br> 创建名称空间Namespace：redis-cluster

```
[root@k8s-master01 redis-cluster-operator-master]# kubectl create ns redis-cluster
namespace/redis-node created
[root@k8s-master01 redis-cluster-operator-master]# kubectl get ns
NAME                   STATUS   AGE
default                Active   76d
ingress-nginx          Active   9d
kube-node-lease        Active   76d
kube-public            Active   76d
kube-system            Active   76d
kube-users             Active   2d21h
kubernetes-dashboard   Active   45h
redis-cluster          Active   11s
rook-ceph              Active   33h
[root@k8s-master01 redis-cluster-op
```

### （2）创建自定义资源（CRD）

```
[root@k8s-master01 redis]# kubectl apply -f deploy/crds/
customresourcedefinition.apiextensions.k8s.io/distributedredisclusters.redis.kun created
customresourcedefinition.apiextensions.k8s.io/redisclusterbackups.redis.kun created
```

### （3）创建operator

```
[root@k8s-master01 redis]# kubectl create -f deploy/service_account.yaml
serviceaccount/redis-cluster-operator created
[root@k8s-master01 redis]# kubectl create -f deploy/cluster/cluster_role.yaml
clusterrole.rbac.authorization.k8s.io/redis-cluster-operator created
[root@k8s-master01 redis]# kubectl create -f deploy/cluster/cluster_role_binding.yaml
clusterrolebinding.rbac.authorization.k8s.io/redis-cluster-operator created
[root@k8s-master01 redis]# kubectl create -f deploy/cluster/operator.yaml
deployment.apps/redis-cluster-operator created
configmap/redis-admin created
[root@k8s-master01 redis]# kubectl get deployment
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
metrics-metrics-server   1/1     1            1           10d
redis-cluster-operator   1/1     1            1           12s


// cluster-scoped 命令
$ kubectl create -f deploy/service_account.yaml
$ kubectl create -f deploy/cluster/cluster_role.yaml
$ kubectl create -f deploy/cluster/cluster_role_binding.yaml
$ kubectl create -f deploy/cluster/operator.yaml

```

### （4）部署样本Redis集群

注意：**只有使用持久性存储（pvc）的redis集群在意外删除或滚动更新后才能恢复。即使您不使用持久性（如rdb或aof），也需要将pvc设置为redis。**

```
apiVersion: redis.kun/v1alpha1
kind: DistributedRedisCluster
metadata:
  annotations:
    # if your operator run as cluster-scoped, add this annotations
    redis.kun/scope: cluster-scoped
  name: example-distributedrediscluster
spec:
  image: redis:5.0.4-alpine
  masterSize: 3
  clusterReplicas: 1
  resources:
    limits:
      cpu: 200m
      memory: 200Mi
    requests:
      cpu: 200m
      memory: 100Mi

```

因为使用样本，没有资源限制，会因为内存不足导致初始化失败，限制使用这个测试

```
kubectl create -f deploy/example/custom-resources.yaml
```

```
[root@k8s-master01 redis]# kubectl get pod,svc
NAME                                          READY   STATUS    RESTARTS   AGE
pod/drc-example-distributedrediscluster-0-0   1/1     Running   0          6m39s
pod/drc-example-distributedrediscluster-0-1   1/1     Running   0          6m2s
pod/drc-example-distributedrediscluster-1-0   1/1     Running   0          6m39s
pod/drc-example-distributedrediscluster-1-1   1/1     Running   0          6m7s
pod/drc-example-distributedrediscluster-2-0   1/1     Running   0          6m39s
pod/drc-example-distributedrediscluster-2-1   1/1     Running   0          6m6s
pod/metrics-metrics-server-6c7745d876-cw72h   1/1     Running   0          8h
pod/redis-cluster-operator-7f6cf86475-dhttx   1/1     Running   0          11m

NAME                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)              AGE
service/example-distributedrediscluster     ClusterIP   10.96.104.199   &lt;none&gt;        6379/TCP,16379/TCP   6m38s
service/example-distributedrediscluster-0   ClusterIP   None            &lt;none&gt;        6379/TCP,16379/TCP   6m38s
service/example-distributedrediscluster-1   ClusterIP   None            &lt;none&gt;        6379/TCP,16379/TCP   6m38s
service/example-distributedrediscluster-2   ClusterIP   None            &lt;none&gt;        6379/TCP,16379/TCP   6m38s
service/kubernetes                          ClusterIP   10.96.0.1       &lt;none&gt;        443/TCP              76d
service/metrics-metrics-server              ClusterIP   10.96.86.164    &lt;none&gt;        443/TCP              10d
service/nginx                               ClusterIP   10.96.215.251   &lt;none&gt;        80/TCP               9d
service/redis-cluster-operator-metrics      ClusterIP   10.96.58.127    &lt;none&gt;        8383/TCP,8686/TCP    11m
[root@k8s-master01 redis]# 

```

创建指定命名空间和动态存储的，我这个没有构建动态存储

```
cat redis-cluster.yaml 
apiVersion: redis.kun/v1alpha1
kind: DistributedRedisCluster
metadata:
  annotations:
    # if your operator run as cluster-scoped, add this annotations
    redis.kun/scope: cluster-scoped
  name: example-distributedrediscluster
  namespace: redis-cluster
spec:
  image: redis:5.0.4-alpine
  imagePullPolicy: IfNotPresent
  masterSize: 3			#master节点数量
  clusterReplicas: 1	#每个master节点的从节点数量
  serviceName: redis-svc
  # resources config
  resources:
    limits:
      cpu: 300m
      memory: 200Mi
    requests:
      cpu: 200m
      memory: 150Mi
  # pv storage
  storage:
    type: persistent-claim
    size: 2Gi
    class: nfs-storage
    deleteClaim: true
]# kubectl apply -f redis-cluster.yaml

```

### （5）验证集群

```
[root@k8s-master01 redis]# kubectl exec -it  drc-example-distributedrediscluster-0-0 -- sh
/data # redis-cli -c -h redis-svc
Could not connect to Redis at redis-svc:6379: Name does not resolve
not connected&gt; 
/data # redis-cli -c -h example-distributedrediscluster
example-distributedrediscluster:6379&gt;  cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:5
cluster_my_epoch:0
cluster_stats_messages_ping_sent:511
cluster_stats_messages_pong_sent:485
cluster_stats_messages_meet_sent:1
cluster_stats_messages_sent:997
cluster_stats_messages_ping_received:481
cluster_stats_messages_pong_received:512
cluster_stats_messages_meet_received:4
cluster_stats_messages_received:997
example-distributedrediscluster:6379&gt; set a b
-&gt; Redirected to slot [15495] located at 10.244.58.209:6379
OK
10.244.58.209:6379&gt; 

```

### （6）扩展Redis集群

增加masterSize触发放大。（注意：这个也直接可以使用edit修改。）

```
apiVersion: redis.kun/v1alpha1
kind: DistributedRedisCluster
metadata:
  annotations:
    # if your operator run as cluster-scoped, add this annotations
    redis.kun/scope: cluster-scoped
  name: example-distributedrediscluster
spec:
  # Increase the masterSize to trigger the scaling.
  masterSize: 4
  ClusterReplicas: 1
  image: redis:5.0.4-alpine
```

### （7）缩减Redis集群

减小masterSize触发缩小。

```
apiVersion: redis.kun/v1alpha1
kind: DistributedRedisCluster
metadata:
  annotations:
    # if your operator run as cluster-scoped, add this annotations
    redis.kun/scope: cluster-scoped
  name: example-distributedrediscluster
spec:
  # Increase the masterSize to trigger the scaling.
  masterSize: 3
  ClusterReplicas: 1
  image: redis:5.0.4-alpine
```

### （8）删除redis集群

```
]# cd redis-cluster-operator/ 
]# kubectl delete -f redis-cluster.yaml
]# cd cluster/
]# kubectl delete -f operator.yaml 
]# kubectl delete -f cluster_role_binding.yaml 
]# kubectl delete -f cluster_role.yaml 
]# kubectl delete -f service_account.yaml 
]# kubectl delete -f deploy/crds/
]# kubectl delete -f ns-redis-cluster.yaml

```

 

github文档：[https://github.com/ucloud/redis-cluster-operator#deploy-redis-cluster-operator](https://github.com/ucloud/redis-cluster-operator#deploy-redis-cluster-operator)
