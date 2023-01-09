+++
author = "南宫乘风"
title = "Kubernetes（k8s）的Service Ingress详细介绍"
date = "2020-02-06 22:48:16"
tags=['Kubernetes', 'k8s', 'service', 'ingress']
categories=[]
image = "post/4kdongman/65.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104201990](https://blog.csdn.net/heian_99/article/details/104201990)

**在 Kubernetes v1.0 版本， Service 是 “4层”（TCP/UDP over IP）概念。 在 Kubernetes v1.1 版本，新增了 Ingress API（beta 版），用来表示 “7层”（HTTP）服务 **

**资料信息 【可实现7层代理】<br> Ingress-Nginx github 地址：[https://github.com/kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)**

**Ingress-Nginx 官方网站：[https://kubernetes.github.io/ingress-nginx/](https://github.com/kubernetes/ingress-nginx)**<br>![20200206204556322.png](https://img-blog.csdnimg.cn/20200206204556322.png)

# 部署 Ingress-Nginx 

下载Ingress-Nginx 文件

```
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.28.0/deploy/static/mandatory.yaml

```

运行配置文件

![20200206211027100.png](https://img-blog.csdnimg.cn/20200206211027100.png)

```
​​​​chmod -R 777 /var/lib/docker

```

给docker权限，不然会出现问题。

我遇见这个问题，[链接](https://blog.csdn.net/ht1032279753/article/details/103867138)，你们可以参考一下

```
kubectl get pod -n ingress-nginx 

```

![20200206213254850.png](https://img-blog.csdnimg.cn/20200206213254850.png)

下载ingress-nginx暴露端口配置文件

```
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.28.0/deploy/static/provider/baremetal/service-nodeport.yaml

```

```
 kubectl apply -f service-nodeport.yaml 
```

![2020020621350067.png](https://img-blog.csdnimg.cn/2020020621350067.png)

# Ingress HTTP 代理访问 

**deployment、Service、Ingress Yaml 文件 **

```
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

![20200206215043893.png](https://img-blog.csdnimg.cn/20200206215043893.png)

```
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

![20200206215342957.png](https://img-blog.csdnimg.cn/20200206215342957.png)

# 实验

![20200206220038549.png](https://img-blog.csdnimg.cn/20200206220038549.png)

### deployment1.yaml 

```
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

```
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

```
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

```
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj 
"/CN=nginxsvc/O=nginxsvc"
kubectl create secret tls tls-secret --key tls.key --cert tls.crt

```

deployment、Service、Ingress Yaml 文件 

```
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

```
yum -y install httpd
htpasswd -c auth foo
kubectl create secret generic basic-auth --from-file=auth

```

```
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
|名称|描述|值
|nginx.ingress.kubernetes.io/rewritetarget|必须重定向流量的目标URI |串
|nginx.ingress.kubernetes.io/sslredirect<br>  |指示位置部分是否仅可访问SSL（当Ingress包含证书时 默认为True）<br>  |布尔
|nginx.ingress.kubernetes.io/forcessl-redirect|即使Ingress未启用TLS，也强制重定向到HTTPS<br>  |布尔
|nginx.ingress.kubernetes.io/approot|定义Controller必须重定向的应用程序根，如果它在'/'上 下文中<br>  |串
|nginx.ingress.kubernetes.io/useregex|指示Ingress上定义的路径是否使用正则表达式<br>  |布尔

```
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

 

 
