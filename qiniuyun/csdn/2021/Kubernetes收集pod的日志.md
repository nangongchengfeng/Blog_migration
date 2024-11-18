---
author: 南宫乘风
categories:
- Kubernetes应用
date: 2021-10-12 17:58:22
description: 背景环境：开发频繁查看日志，登录服务器导出日志比较耗费时间，搭建一款轻量又简单的日志查询工具供开发查询容器日志。方案选型：适用于日志体系比较大的场景，且比较消耗服务器资源。轻量级特点：简洁明了，安装部。。。。。。。
image: ../../title_pic/40.jpg
slug: '202110121758'
tags:
- linux
- docker
- k8s
title: Kubernetes收集pod的日志
---

<!--more-->

背景环境：  
开发频繁查看日志，登录服务器导出日志比较耗费时间，搭建一款轻量又简单的日志查询工具供开  
发查询容器日志。  
方案选型：  
（1）ELK（EFK）适用于日志体系比较大的场景，且比较消耗服务器资源。  
（2）Loki---->轻量级（特点：简洁明了，安装部署简单）----->适用于当前环境

```bash
#1.安装helm
首先安装helm管理工具（官网）：https://helm.sh/docs/intro/install/
[root@k8s-node01 ~]# wget https://get.helm.sh/helm-v3.3.3-linux-amd64.tar.gz
[root@k8s-node01 ~]# tar xf helm-v3.3.3-linux-amd64.tar.gz
[root@k8s-node01 ~]# mv linux-amd64/helm /usr/local/bin/helm
[root@k8s-node01 ~]# helm version
version.BuildInfo{Version:"v3.3.3",
GitCommit:"55e3ca022e40fe200fbc855938995f40b2a68ce0", GitTreeState:"clean",
GoVersion:"go1.14.9"}

[root@k8s-node01 ~]# mkdir loki
[root@k8s-node01 ~]# ls
anaconda-ks.cfg helm-v3.3.3-linux-amd64.tar.gz linux-amd64 loki thirdservice
[root@k8s-node01 ~]# cd loki/
[root@k8s-node01 loki]# helm repo add loki https://grafana.github.io/loki/charts
&& helm repo update
[root@k8s-node01 loki]# helm pull loki/loki-stack
[root@k8s-node01 loki]# tar xf loki-stack-2.1.2.tgz
[root@k8s-node01 loki]# helm install loki -n loki loki-stack/


#创建grafana文件
[root@k8s-node01 loki]# cat grangfan.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  labels:
    app: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        volumeMounts:
        - name: timezone
          mountPath: /etc/localtime
      volumes:
        - name: timezone
          hostPath:
            path: /usr/share/zoneinfo/Asia/Shanghai

---

apiVersion: v1
kind: Service
metadata:
  name: grafana-svc
  #namespace: test
spec:
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 3303
  type: NodePort
  selector:
    app: grafana
```

浏览器访问 IP:3003 账号密码：admin admin  
数据源配置

![](../../image/20211012175645983.png)

loki:3100 

![](../../image/20211012175700336.png)

容器日志查询   

![](../../image/20211012175715924.png)

依次点击实时查看容器日志 

![](../../image/20211012175728609.png)

效果图

![](../../image/20211012175749979.png)