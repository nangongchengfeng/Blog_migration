---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-02-06 22:48:16
description: 在版本，是层概念。在版本，新增了版，用来表示层服务资料信息可实现层代理地址：官方网站：部署下载文件运行配置文件给权限，不然会出现问题。我遇见这个问题，链接，你们可以参考一下下载暴露端口配置文件代理访问。。。。。。。
image: ../../title_pic/06.jpg
slug: '202002062248'
tags:
- Kubernetes
- k8s
- service
- ingress
title: Kubernetes（k8s）的Service Ingress详细介绍
---

<!--more-->

**在 Kubernetes v1.0 版本， Service 是 “4层”（TCP/UDP over IP）概念。 在 Kubernetes v1.1 版本，新增了 Ingress API（beta 版），用来表示 “7层”（HTTP）服务 **

**资料信息 【可实现7层代理】  
Ingress-Nginx github 地址：<https://github.com/kubernetes/ingress-nginx>**

**Ingress-Nginx 官方网站：[https://kubernetes.github.io/ingress-nginx/](https://github.com/kubernetes/ingress-nginx)**  
![](../../image/20200206204556322.png)

# 部署 Ingress-Nginx 

下载Ingress-Nginx 文件

```bash
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.28.0/deploy/static/mandatory.yaml
```

运行配置文件

![](../../image/20200206211027100.png)

```
​​​​chmod -R 777 /var/lib/docker
```

给docker权限，不然会出现问题。

我遇见这个问题，[链接](https://blog.csdn.net/ht1032279753/article/details/103867138)，你们可以参考一下

```
kubectl get pod -n ingress-nginx 
```

![](../../image/20200206213254850.png)

下载ingress-nginx暴露端口配置文件

```
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.28.0/deploy/static/provider/baremetal/service-nodeport.yaml
```

```
 kubectl apply -f service-nodeport.yaml 
```

![](../../image/2020020621350067.png)

# Ingress HTTP 代理访问 

**deployment、Service、Ingress Yaml 文件 **

```bash
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-dm
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - name: nginx
          image: wangyanglinux/myapp:v1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  selector:
    name: nginx
```

![](../../image/20200206215043893.png)

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  rules:
    - host: www.heian.com
      http:
        paths:
        - path: /
          backend:
            serviceName: nginx-svc
            servicePort: 80
```

![](../../image/20200206215342957.png)

# 实验

![](../../image/20200206220038549.png)

### deployment1.yaml 

```bash
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: deployment1
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - name: nginx
          image: wangyanglinux/myapp:v1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-1
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  selector:
    name: nginx
```

### deployment2.yaml 

```bash
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: deployment2
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx2
    spec:
      containers:
        - name: nginx2
          image: wangyanglinux/myapp:v1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-2
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  selector:
    name: nginx2
```

### ingress-nginx

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress1
spec:
  rules:
    - host: www.heian.com
      http:
        paths:
        - path: /
          backend:
            serviceName: svc-1
            servicePort: 80
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress2
spec:
  rules:
    - host: www2.heian.com
      http:
        paths:
        - path: /
          backend:
            serviceName: svc-2
            servicePort: 80
```

# Ingress  HTTPS 代理访问 

创建证书，以及 cert 存储方式 

```bash
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj 
"/CN=nginxsvc/O=nginxsvc"
kubectl create secret tls tls-secret --key tls.key --cert tls.crt
```

deployment、Service、Ingress Yaml 文件 

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  tls:
    - hosts:
      - foo.bar.com
      secretName: tls-secret
  rules:
    - host: foo.bar.com
      http:
        paths:
        - path: /
          backend:
            serviceName: nginx-svc
            servicePort: 80
```

 

 

Nginx 进行 BasicAuth 

```bash
yum -y install httpd
htpasswd -c auth foo
kubectl create secret generic basic-auth --from-file=auth
```

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-with-auth
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - foo'
spec:
  rules:
  - host: foo2.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```

### Nginx 进行重写 

<table border="1" cellpadding="1" cellspacing="1" style="width:500px;"><tbody><tr><td>名称</td><td>描述</td><td>值</td></tr><tr><td>nginx.ingress.kubernetes.io/rewritetarget</td><td>必须重定向流量的目标URI&nbsp;</td><td>串</td></tr><tr><td>nginx.ingress.kubernetes.io/sslredirect<br>&nbsp;</td><td>指示位置部分是否仅可访问SSL（当Ingress包含证书时 默认为True）<br>&nbsp;</td><td>布尔</td></tr><tr><td>nginx.ingress.kubernetes.io/forcessl-redirect</td><td>即使Ingress未启用TLS，也强制重定向到HTTPS<br>&nbsp;</td><td>布尔</td></tr><tr><td>nginx.ingress.kubernetes.io/approot</td><td>定义Controller必须重定向的应用程序根，如果它在'/'上 下文中<br>&nbsp;</td><td>串</td></tr><tr><td>nginx.ingress.kubernetes.io/useregex</td><td>指示Ingress上定义的路径是否使用正则表达式<br>&nbsp;</td><td>布尔</td></tr></tbody></table>

```bash
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: http://foo.bar.com:31795/hostname.html
spec:
  rules:
  - host: foo10.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```