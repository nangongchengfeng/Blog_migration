---
author: 南宫乘风
categories:
- Jenkins
date: 2022-05-26 15:48:35
description: 前文安装部署使用南宫乘风的博客博客安装部署使用南宫乘风的博客博客入门配置南宫乘风的博客博客入门配置南宫乘风的博客博客集成南宫乘风的博客博客集成南宫乘风的博客博客的流水线的流水线流水线整合钉钉南宫乘风的。。。。。。。
image: ../../title_pic/20.jpg
slug: '202205261548'
tags:
- jenkins
- kubernetes
- docker
title: Kubernetes安装Jenkins
---

<!--more-->

# 前文

[Jenkins安装部署使用\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858 "Jenkins安装部署使用_南宫乘风的博客-CSDN博客")

[Jenkins入门配置\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124809338 "Jenkins入门配置_南宫乘风的博客-CSDN博客")

[Jenkins集成Sonar Qube\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124814780 "Jenkins集成Sonar Qube_南宫乘风的博客-CSDN博客")

[Jenkins的流水线（Pipeline）](https://blog.csdn.net/heian_99/article/details/124815450 "Jenkins的流水线（Pipeline）")

[Jenkins流水线整合钉钉\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124816190?spm=1001.2014.3001.5501 "Jenkins流水线整合钉钉_南宫乘风的博客-CSDN博客") 

**目录**

[环境](#%E7%8E%AF%E5%A2%83)

[思路](#%E6%80%9D%E8%B7%AF)

[1、NFS（动态存储）](#1%E3%80%81NFS%EF%BC%88%E5%8A%A8%E6%80%81%E5%AD%98%E5%82%A8%EF%BC%89)

[2、helm安装nfs-client](#2%E3%80%81helm%E5%AE%89%E8%A3%85nfs-client)

[3、创建namespace ](#3%E3%80%81%E5%88%9B%E5%BB%BAnamespace%C2%A0)

[4、持久化Jenkins数据](#4%E3%80%81%E6%8C%81%E4%B9%85%E5%8C%96Jenkins%E6%95%B0%E6%8D%AE)

[5、创建service account](<#5、创建service account>)

[6、安装Jenkins](#6%E3%80%81%E5%AE%89%E8%A3%85Jenkins)

[7、授权对Jenkins服务的访问权限](#7%E3%80%81%E6%8E%88%E6%9D%83%E5%AF%B9Jenkins%E6%9C%8D%E5%8A%A1%E7%9A%84%E8%AE%BF%E9%97%AE%E6%9D%83%E9%99%90)

[8、打开浏览器IP:31400/](#8%E3%80%81%E6%89%93%E5%BC%80%E6%B5%8F%E8%A7%88%E5%99%A8IP%3A31400%2F)

---

---

## 环境

生产实践-k8s安装Jenkins和Jenkins Kubernetes插件  
环境要求：你需要一个正常可以使用的Kubernetes集群，集群中可以使用的内存大于等于4G。  
Kubernetes版本1.18

## 思路

Jenkins插件可以在Kubernetes集群中运行动态jenkins-slave代理。

基于Kubernetes的docker，自动化在Kubernetes中运行的Jenkins-slave代理的缩放。

该插件为每个jenkins-slave代理创建Kubernetes Pod，并在每个构建后停止它。

在Kubernetes中jenkins-slave代理启动，会自动连接到Jenkins主控制器。 对于某些环境变量，会自动注入：

Jenkins\_URL：Jenkins Web界面URL  
jenkins\_secret：身份验证的秘密密钥  
jenkins\_agent\_name：jenkins代理的名称  
jenkins\_name：jenkins代理的名称（已弃用。仅用于向后兼容性）  
不需要在Kubernetes内运行Jenkins Controller。

## 1、NFS（动态存储）

```bash
#安装
yum install -y nfs-utils rpcbind
 
mkdir -p /data/nfsdata
 
# 修改配置
$ vim /etc/exports
/data/nfsdata 192.168.31.* (rw,async,no_root_squash)
 
# 使配置生效
$ exportfs -r
 
# 服务端查看下是否生效
$ showmount -e localhost
 
Export list for localhost:
/data/nfsdata (everyone)
```

## 2、helm安装nfs-client

```bash
stable       	https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
helm添加这个源
```

```bash
下载helm包
helm pull aliyuncs/nfs-client-provisioner
解压
tar -zxvf nfs-client-provisioner-1.2.8.tgz
 
修复values.yaml 三处
image:
  repository: quay.io/external_storage/nfs-client-provisioner
  tag: v3.1.0-k8s1.11
  pullPolicy: IfNotPresent
 
nfs:
  server: 192.168.31.73
  path: /data/nfsdata
 
 
  reclaimPolicy: Retain
```

 ![](../../image/9475e0d59fc842f38b056d4766e0e606.png)

## 3、创建namespace 

```bash
kubectl create namespace jenkins
kubectl get namespaces
```

## 4、持久化Jenkins数据

pvc.yaml

```bash

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jenkins-pvc
  namespace: jenkins
spec:
  storageClassName: "nfsdata"
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```

通过kubectl部署volume

```bash
kubectl apply -f pvc.yaml
```

## 5、创建service account

创建pod时，如果不指定服务账户，则会自动为其分配一个名为default的同一namespace中的服务账户。但是通常应用程序时存在权限不足的情况，所以需要我们自己创建一个服务账户。  
①下载jenkins-sa.yaml

```
wget https://raw.githubusercontent.com/jenkins-infra/jenkins.io/master/content/doc/tutorials/kubernetes/installing-jenkins-on-kubernetes/jenkins-sa.yaml
```

②通过kubectl部署jenkins-sa.yaml

```
kubectl apply -f jenkins-sa.yaml
```

或者使用下面的文件

jenkins-sa.yaml 

```bash

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins
  namespace: jenkins
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: jenkins
rules:
- apiGroups:
  - '*'
  resources:
  - statefulsets
  - services
  - replicationcontrollers
  - replicasets
  - podtemplates
  - podsecuritypolicies
  - pods
  - pods/log
  - pods/exec
  - podpreset
  - poddisruptionbudget
  - persistentvolumes
  - persistentvolumeclaims
  - jobs
  - endpoints
  - deployments
  - deployments/scale
  - daemonsets
  - cronjobs
  - configmaps
  - namespaces
  - events
  - secrets
  verbs:
  - create
  - get
  - watch
  - delete
  - list
  - patch
  - update
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
  - update
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: jenkins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: jenkins
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:serviceaccounts:jenkins
```

## 6、安装Jenkins

jenkins-deployment.yaml 

```bash

apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins
  namespace: jenkins
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      serviceAccountName: jenkins   #指定我们前面创建的服务账号
      containers:
      - name: jenkins
        image: registry.cn-hangzhou.aliyuncs.com/s-ops/jenkins:2.346
        ports:
        - containerPort: 8080
        - containerPort: 50000
        volumeMounts:
        - name: jenkins-home
          mountPath: /var/jenkins_home
      volumes:
      - name: jenkins-home
        persistentVolumeClaim:
          claimName: jenkins-pvc     #指定前面创建的PVC
```

通过kubectl部署jenkins-deployment.yaml

```
kubectl create -f jenkins-deployment.yaml -n jenkins
```

## 7、授权对Jenkins服务的访问权限

  
主要目的暴露外部访问Jenkins的8080端口，我将31400定义为8080的映射端口。

jenkins-service.yaml

```bash
apiVersion: v1
kind: Service
metadata:
  name: jenkins
  namespace: jenkins
spec:
  type: NodePort
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    nodePort: 31400
  - name: agent
    port: 50000
    targetPort: 50000
    nodePort: 31401
  selector:
    app: jenkins
```

通过kubectl部署服务

```
kubectl create -f jenkins-service.yaml -n jenkins
```

## 8、打开浏览器IP:31400/

查看密码

```bash
kubectl get pod -n jenkins  //查询podname
kubectl logs podname -n jenkins

*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

cf8d9da9de0346fd90461be366915d76

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

*************************************************************
```

选择推荐插件安装，创建管理员\~完成！

![](../../image/160c828b8b82433699b8ecd834d22f33.png)