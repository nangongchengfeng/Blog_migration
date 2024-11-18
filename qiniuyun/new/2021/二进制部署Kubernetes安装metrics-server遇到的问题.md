---
author: 南宫乘风
categories:
- 错误问题解决
date: 2021-03-23 19:16:02
description: 部署后执行或报错一、问题检查步骤：、查看服务日志检查发现是由于调用无权限，返回了错误、检查是否配置了以下参数、问题总结：服务配置是没有问题的，但服务依然报错，有两种方法可以解决问题、授权集群角色给用户。。。。。。。
image: http://image.ownit.top/4kdongman/56.jpg
tags:
- Kubernetes应用
- Kubernetes
- kubernetes
title: 二进制部署Kubernetes安装metrics-server遇到的问题
---

<!--more-->

ubernetes部署metrics-server后执行kubectl top pod或kubectl top node报错  
Error from server \(ServiceUnavailable\): the server is currently unable to handle the request \(get pods.metrics.k8s.io\)

![](http://image.ownit.top/csdn/20200322214527823.png)

一、问题检查步骤：

1.1、查看metrics-server服务日志

```bash
Cluster doesn't provide requestheader-client-ca-file in configmap/extension-apiserver-authentication in kube-system, so request-header client certificate authentication won't work.
```

检查发现是由于调用metrics-server无权限，返回了http 403错误

1.2、检查是否配置了以下参数

```bash
        args:
          - --cert-dir=/tmp
          - --secure-port=4443
          - --kubelet-insecure-tls=true
          - --kubelet-preferred-address-types=InternalIP,Hostname,InternalDNS,externalDNS
```

1.3、问题总结：

metrics-server服务配置是没有问题的，但服务依然报错 Error from server \(ServiceUnavailable\): the server is currently unable to handle the request \(get pods.metrics.k8s.io\)，有两种方法可以解决问题

1、授权集群角色给用户system:anonymous

```
kubectl create clusterrolebinding system:anonymous  --clusterrole=cluster-admin  --user=system:anonymous
```

2、创建system:metrics-server角色并授权

二、问题解决\(创建system:metrics-server角色并授权\)

配置metrics-server证书

```bash
# vim metrics-server-csr.json
{
  "CN": "system:metrics-server",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",
      "OU": "system"
    }
  ]
}
```

 

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes metrics-server-csr.json | cfssljson -bare metrics-server
```

配置metrics-server  RBAC授权

```bash
cat > auth-metrics-server.yaml << EOF
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:auth-metrics-server-reader
  labels:
    rbac.authorization.k8s.io/aggregate-to-view: "true"
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
rules:
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods", "nodes"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: metrics-server:system:auth-metrics-server
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-metrics-server-reader
subjects:
- kind: User
  name: system:metrics-server
  namespace: kube-system
EOF
```

kube-apiserver添加metrics-server需要的配置

```bash
--requestheader-client-ca-file=/opt/kubernetes/ssl/ca.pem \
--requestheader-allowed-names=aggregator,metrics-server \
--requestheader-extra-headers-prefix=X-Remote-Extra- \
--requestheader-group-headers=X-Remote-Group \
--requestheader-username-headers=X-Remote-User \
--proxy-client-cert-file=/opt/kubernetes/ssl/metrics-server.pem \
--proxy-client-key-file=/opt/kubernetes/ssl/metrics-server-key.pem 
```

检查是否能够正常获取到监控信息

![](http://image.ownit.top/csdn/20210323191550516.png)