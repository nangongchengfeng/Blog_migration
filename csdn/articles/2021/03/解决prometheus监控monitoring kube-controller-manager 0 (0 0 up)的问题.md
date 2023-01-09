+++
author = "南宫乘风"
title = "解决prometheus监控monitoring/kube-controller-manager/0 (0/0 up)的问题"
date = "2021-03-18 12:32:12"
tags=['kubernetes', 'centos', '运维']
categories=['Prometheus监控', 'Kubernetes', ' Kubernetes应用']
image = "post/4kdongman/63.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/114971123](https://blog.csdn.net/heian_99/article/details/114971123)

我前面使用Kubernetes构建prometheus监控，没有什么大问题，但是monitoring/kube-controller-manager/0 (0/0 up)，这个没有数值。

![20210318123025468.png](https://img-blog.csdnimg.cn/20210318123025468.png)

一般出现这个问题，都是Kubernetes部署时，没有对应的标签，导致无法找到资源

## 问题

### 问题一：ip地址

**正常开启的，但是这个监听端口是127.0.0.1的，普罗米修斯无法直接访问**

```
[root@k8s-master01 jiankong]# netstat -lntp | grep control
tcp        0      0 127.0.0.1:10257         0.0.0.0:*               LISTEN      112736/kube-control 
tcp6       0      0 :::10252                :::*                    LISTEN      112736/kube-control
```

![20210318115511934.png](https://img-blog.csdnimg.cn/20210318115511934.png)

### 问题二：SVC没有标签资源

```
[root@k8s-master01 jiankong]# kubectl get servicemonitors.monitoring.coreos.com -n monitoring kube-controller-manager -oyaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  annotations:
..............................
      sourceLabels:
      - __name__
    - action: drop
      regex: etcd_(debugging|disk|request|server).*
      sourceLabels:
      - __name__
    port: http-metrics
  jobLabel: k8s-app
  namespaceSelector:
    matchNames:
    - kube-system
  selector:
    matchLabels:
      k8s-app: kube-controller-manager  #通过这个标签匹配kube-controller-manager

[root@k8s-master01 jiankong]# kubectl get svc -n kube-system -l k8s-app= kube-controller-manager
error: name cannot be provided when a selector is specified

#这边在kube-system没有这个标签的svc，所以无法匹配到
```

 

## 解决：

### 1、修改监听地址

```
vim /etc/kubernetes/manifests/kube-controller-manager.yaml

    - --bind-address=0.0.0.0


```

![2021031812044881.png](https://img-blog.csdnimg.cn/2021031812044881.png)

![20210318121030394.png](https://img-blog.csdnimg.cn/20210318121030394.png)

开0.0.0.0，是可以的，因为Kubernetes通信需要证书，是双向的。

 

### 2、添加svc ep标签

```
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: kube-controller-manager
  name: kube-controller-manage-monitor
  namespace: kube-system
spec:
  ports:
  - name: http-metrics
    port: 10252
    protocol: TCP
    targetPort: 10252
  sessionAffinity: None
  type: ClusterIP

apiVersion: v1
kind: Endpoints
metadata:
  labels:
    k8s-app: kube-controller-manager
  name: kube-controller-manage-monitor
  namespace: kube-system
subsets:
- addresses:
  - ip: 192.168.0.100
  ports:
  - name: http-metrics
    port: 10252
    protocol: TCP
```

 

![20210318122907108.png](https://img-blog.csdnimg.cn/20210318122907108.png)

![20210318123052749.png](https://img-blog.csdnimg.cn/20210318123052749.png)

### 3、测试

![20210318123145527.png](https://img-blog.csdnimg.cn/20210318123145527.png)

 
