---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-08-01 23:23:37
description: 布署完后，但是访问会报错，此处有两个坑、聚合功能通过二进制方式部署完成后，部署后，查看日志出现下面错误信息：根据错误日志信息，可以知道是缺少认证的证书文件，导致不能访问而出现的问题。出现这个错误是因为。。。。。。。
image: http://image.ownit.top/4kdongman/44.jpg
tags:
- 错误问题解决
- Kubernetes
- docker
- 虚拟化
- 问题
title: 解决二进制K8S布署的metrics-server查看集群资源报错权限问题
---

<!--more-->

布署完metircs-server后，但是访问会报错，此处有两个坑

## 1、API聚合功能

通过二进制方式部署完成 `kubernetes` 后，部署 `Metrics Server` 后，查看日志出现下面错误信息：

```bash
E1231 10:33:31.978715 1 configmap_cafile_content.go:243] key failed with:
missing content for CA bundle "client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
E1231 10:34:22.710836 1 configmap_cafile_content.go:243] kube-system/extension-apiserver-authentication failed with:
missing content for CA bundle "client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
E1231 10:34:31.978769 1 configmap_cafile_content.go:243] key failed with:
missing content for CA bundle "client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file"
```

根据错误日志信息，可以知道是缺少认证的证书文件，导致不能访问 `kube-apiserver` 而出现的问题。

出现这个错误是因为 kube-apiserver 没有开启 `API` 聚合功能。所以需要配置 `kube-apiserver` 参数，开启聚合功能即可。

为了能够将用户自定义的 API 注册到 `Master` 的 `API Server` 中，首先需要在 Master 节点所在服务器，配置 `kube-apiserver` 应用的启动参数来启用 `API 聚合` 功能，参数如下：

```bash
--runtime-config=api/all=true
--requestheader-allowed-names=aggregator
--requestheader-group-headers=X-Remote-Group
--requestheader-username-headers=X-Remote-User
--requestheader-extra-headers-prefix=X-Remote-Extra-
--requestheader-client-ca-file=/etc/kubernetes/pki/ca.pem
--proxy-client-cert-file=/etc/kubernetes/pki/proxy-client.pem
--proxy-client-key-file=/etc/kubernetes/pki/proxy-client-key.pem
```

如果 `kube-apiserver` 所在的主机上没有运行 `kube-proxy`，即无法通过服务的 `ClusterIP` 进行访问，那么还需要设置以下启动参数：

```bash
--enable-aggregator-routing=true
```

在设置完成重启 `kube-apiserver` 服务，就启用 `API 聚合` 功能了。

```bash
systemctl daemon-reload && systemctl restart kube-apiserver
```

### 开启API聚合功能

按照上面的解决问题思路，我们可以开启 API 聚合功能，然后重启 Metrics Server 服务，步骤如下：

安装 cfssl 工具

```bash
## 下载三个组件
$ wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64 -O cfssl
$ wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64  -O cfssljson
$ wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64  -O cfssl-certinfo

## 复制到 bin 目录下
$ chmod +x ./cfssl*
$ mv ./cfssl* /usr/local/bin/
```

### 创建 cfssl 配置文件

创建 proxy-client-csr.json 文件：

```bash
{
  "CN": "aggregator",
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
      "O": "system:masters",
      "OU": "System"
    }
  ]
}
```

生成证书和秘钥：

```bash
cfssl gencert   -profile=kubernetes   -ca=/etc/kubernetes/pki/ca.pem   -ca-key=/etc/kubernetes/pki/ca-key.pem   proxy-client-csr.json | cfssljson -bare kube-proxy
```

```bash
ls -l

-rw-r--r-- 1 root root 1017 12月 31 11:20 proxy-client.csr
-rw-r--r-- 1 root root  236 12月 31 11:07 proxy-client-csr.json
-rw------- 1 root root 1675 12月 31 11:20 proxy-client-key.pem
-rw-r--r-- 1 root root 1411 12月 31 11:20 proxy-client.pem
```

将证书访问指定的目录下，这里我将其放到 /etc/kubernetes/pki 下：

```bash
 cp * /etc/kubernetes/pki/
```

修改 kube-apiserver 参数

```bash
--runtime-config=api/all=true \
--requestheader-allowed-names=aggregator \
--requestheader-group-headers=X-Remote-Group \
--requestheader-username-headers=X-Remote-User \
--requestheader-extra-headers-prefix=X-Remote-Extra- \
--requestheader-client-ca-file=/etc/kubernetes/pki/ca.pem \
--proxy-client-cert-file=/etc/kubernetes/pki/proxy-client.pem \
--proxy-client-key-file=/etc/kubernetes/pki/proxy-client-key.pem \
```

```
参数说明：

–requestheader-client-ca-file： 客户端 CA 证书。
–requestheader-allowed-names： 允许访问的客户端 common names 列表，通过 header 中 –requestheader-username-headers 参数指定的字段获取。客户端 common names 的名称需要在 client-ca-file 中进行设置，将其设置为空值时，表示任意客户端都可访问。
–requestheader-username-headers： 参数指定的字段获取。
–requestheader-extra-headers-prefix： 请求头中需要检查的前缀名。
–requestheader-group-headers 请求头中需要检查的组名。
–requestheader-username-headers 请求头中需要检查的用户名。
–proxy-client-cert-file： 在请求期间验证 Aggregator 的客户端 CA 证书。
–proxy-client-key-file： 在请求期间验证 Aggregator 的客户端私钥。
–requestheader-allowed-names： 允许访问的客户端 common names 列表，通过 header 中 –requestheader-username-headers 参数指定的字段获取。客户端 common names 的名称需要在 client-ca-file 中进行设置，将其设置为空值时，表示任意客户端都可访问。
```

重启 kube-apiserver 组件

```bash
 systemctl daemon-reload && systemctl restart kube-apiserver
```

## 2、用户无权限访问资源pod

报错

```bash
^C[root@k8s-master cfg]# kubectl top pod -A
Error from server (Forbidden): pods.metrics.k8s.io is forbidden: User "system:kube-proxy" cannot list resource "pods" in API group "metrics.k8s.io" at the cluster scope
[root@k8s-master cfg]# kubectl top pod 
Error from server (Forbidden): pods.metrics.k8s.io is forbidden: User "system:kube-proxy" cannot list resource "pods" in API group "metrics.k8s.io" in the namespace "default"
```

报错提示为RBAC权限问题，给kubernetes用户授权如下：

```
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: metrics-reader
rules:
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["nodes"]
  verbs: ["get", "watch", "list"]
 
---
 
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: system:kube-proxy  #用户名称
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: metrics-reader
  apiGroup: rbac.authorization.k8s.io
 
 
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: metrics-reader
rules:
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["nodes"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: metrics
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: metrics-reader
subjects:
- kind: User
  name: system:kube-proxy #用户名称
  apiGroup: rbac.authorization.k8s.io
```

问题就解决

![](http://image.ownit.top/csdn/20210801232304517.png)