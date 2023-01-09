+++
author = "南宫乘风"
title = "Kubernetes（k8s）的调度器 - 调度亲和性详细介绍"
date = "2020-02-11 16:02:24"
tags=['Kubernetes', 'k8s', '调度', '亲和性']
categories=[]
image = "post/4kdongman/99.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104263089](https://blog.csdn.net/heian_99/article/details/104263089)

# 节点亲和性

**pod.spec.nodeAﬃnity**
- preferredDuringSchedulingIgnoredDuringExecution：软策略- requiredDuringSchedulingIgnoredDuringExecution：硬策略
### requiredDuringSchedulingIgnoredDuringExecution

```
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

# ![20200211145022940.png](https://img-blog.csdnimg.cn/20200211145022940.png)

# ![20200211145132557.png](https://img-blog.csdnimg.cn/20200211145132557.png)

### preferredDuringSchedulingIgnoredDuringExecution

```
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

![20200211150043932.png](https://img-blog.csdnimg.cn/20200211150043932.png)

# 先硬后软

```
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
- **In：label 的值在某个列表中**- **NotIn：label 的值不在某个列表中**- **Gt：label 的值大于某个值**- **Lt：label 的值小于某个值**- **Exists：某个 label 存在**- **DoesNotExist：某个 label 不存在**<br>  
#  Pod  亲和性

**pod.spec.aﬃnity.podAﬃnity/podAntiAﬃnity**
- **preferredDuringSchedulingIgnoredDuringExecution：软策略**- **requiredDuringSchedulingIgnoredDuringExecution：硬策略**
```
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

亲和性/反亲和性调度策略比较如下：<br>  
|调度策略匹配 标签|匹配 标签|操作符|拓扑域 支持|调度目标
|nodeAﬃnity| 主机|In, NotIn, Exists, DoesNotExist, Gt, Lt|否|指向主机
|podAﬃnity |POD|In, NotIn, Exists, DoesNotExist|是|POD与指定POD同一拓 扑域
|podAnitAﬃnity |POD|In, NotIn, Exists, DoesNotExist|是|POD与指定POD不在同 一拓扑域

 
