---
author: 南宫乘风
categories:
- Traefik
date: 2021-03-29 20:31:53
description: 部署的中间件，灰度发布，流量复制基于上篇文章环境。部署应用和部署对象配置路由创建一个访问应用的对象中间件中间件是中一个非常有特色的功能，我们可以根据自己的各种需求去选择不同的中间件来满足服务，官方已经。。。。。。。
image: ../../title_pic/34.jpg
slug: '202103292031'
tags:
- kubernetes
- 中间件
- docker
- traefik
title: Traefik的中间件，灰度发布，流量复制
---

<!--more-->

# [Kubernetes 1.18.3 部署 Traefik2.2](https://blog.csdn.net/heian_99/article/details/115304849)

Traefik的中间件，灰度发布，流量复制基于上篇文章环境。

## 1.部署`whoami` 应用和SVC

```bash
apiVersion: v1
kind: Service
metadata:
  name: whoami
spec:
  ports:
    - protocol: TCP
      name: web
      port: 80
  selector:
    app: whoami
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: whoami
  labels:
    app: whoami
spec:
  replicas: 2
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
        - name: whoami
          image: containous/whoami
          ports:
            - name: web
              containerPort: 80
```

## 2.部署 IngressRoute 对象

```
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: simpleingressroute
spec:
  entryPoints:
    - web
  routes:
  - match: Host(`who.heian.com`) && PathPrefix(`/notls`)
    kind: Rule
    services:
    - name: whoami
      port: 80
```

### ![](../../image/20210329191217238.png)

## 3.配置 HTTPS 路由

```bash
[root@k8s-master1 who]# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=who.heian.com" 
Generating a 2048 bit RSA private key
..........................................................................+++
..........+++
writing new private key to 'tls.key'
-----
[root@k8s-master1 who]#  kubectl create secret tls who-tls --cert=tls.crt --key=tls.key
secret/who-tls created
```

创建一个 HTTPS 访问应用的 IngressRoute 对象

```
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: ingressroutetls
spec:
  entryPoints:
    - websecure
  routes:
  - match: Host(`who.heian.com`) && PathPrefix(`/tls`)
    kind: Rule
    services:
    - name: whoami
      port: 80
  tls:
    secretName: who-tls
```

![](../../image/20210329193802251.png)

## 4 . 中间件

中间件是 Traefik2.0 中一个非常有特色的功能，我们可以根据自己的各种需求去选择不同的中间件来满足服务，Traefik 官方已经内置了许多不同功能的中间件，其中一些可以修改请求，头信息，一些负责重定向，一些添加身份验证等等，而且中间件还可以通过链式组合的方式来适用各种情况。

![traefik middleware overview](../../image/dc561bf67c3bc666dd4a4ad2c4a66e24.png)

同样比如上面我们定义的 whoami 这个应用，我们可以通过 `https://who.heian.com/tls` 来访问到应用，但是如果我们用 `http` 来访问的话呢就不行了，就会404了，因为我们根本就没有简单80端口这个入口点，

所以要想通过 `http` 来访问应用的话自然我们需要监听下 `web` 这个入口点：

```
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: ingressroutetls-http
spec:
  entryPoints:
    - web
  routes:
  - match: Host(`who.heian.com`) && PathPrefix(`/tls`)
    kind: Rule
    services:
    - name: whoami
      port: 80
```

注意这里我们创建的 IngressRoute 的 entryPoints 是 `web`，然后创建这个对象，这个时候我们就可以通过 http 访问到这个应用了。

但是我们如果只希望用户通过 https 来访问应用的话呢？按照以前的知识，我们是不是可以让 http 强制跳转到 https 服务去，对的，在 Traefik 中也是可以配置强制跳转的，只是这个功能现在是通过中间件来提供的了。

如下所示，我们使用 `redirectScheme` 中间件来创建提供强制跳转服务：

```bash
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: redirect-https
spec:
  redirectScheme:
    scheme: https
```

然后将这个中间件附加到 http 的服务上面去，因为 https 的不需要跳转：

```bash
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: ingressroutetls-http
spec:
  entryPoints:
    - web
  routes:
  - match: Host(`who.heian.com`) && PathPrefix(`/tls`)
    kind: Rule
    services:
    - name: whoami
      port: 80
    middlewares: 
    - name: redirect-https
```

这个时候我们再去访问 http 服务可以发现就会自动跳转到 https 去了。关于更多中间件的用法可以查看文档 [Traefik Docs](https://www.qikqiak.com/traefik-book/middlewares/overview/)。

![](../../image/20210329194405112.png)![](../../image/20210329194443542.png)

## 5\. 灰度发布

Traefik2.0 的一个更强大的功能就是灰度发布，灰度发布我们有时候也会称为金丝雀发布（Canary），主要就是让一部分测试的服务也参与到线上去，经过测试观察看是否符号上线要求。

![canary deployment](../../image/2fb0b6c154bfbb5c9c3c2a55af72407d.png)

比如现在我们有两个名为 `appv1` 和 `appv2` 的服务，我们希望通过 Traefik 来控制我们的流量，将 3⁄4 的流量路由到 appv1，¼ 的流量路由到 appv2 去，这个时候就可以利用 Traefik2.0 中提供的**带权重的轮询（WRR）**来实现该功能

首先在 Kubernetes 集群中部署上面的两个服务。

为了对比结果我们这里提供的两个服务一个是 heian99/myapp:v2，一个是heian99/myapp:v1，方便测试。

appv1 服务的资源清单如下所示：（appv1.yaml）heian99/myapp:v1

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appv1
spec:
  selector:
    matchLabels:
      app: appv1
  template:
    metadata:
      labels:
        use: test
        app: appv1
    spec:
      containers:
      - name: myappv1
        image: heian99/myapp:v1
        ports:
        - containerPort: 80
          name: portv1
---
apiVersion: v1
kind: Service
metadata:
  name: appv1
spec:
  selector:
    app: appv1
  ports:
  - name: http
    port: 80
    targetPort: portv1
```

 

appv2 服务的资源清单如下所示：（appv2.yaml）heian99/myapp:v2

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appv2
spec:
  selector:
    matchLabels:
      app: appv2
  template:
    metadata:
      labels:
        use: test
        app: appv2
    spec:
      containers:
      - name: myappv2
        image: heian99/myapp:v2
        ports:
        - containerPort: 80
          name: portv2
---
apiVersion: v1
kind: Service
metadata:
  name: appv2
spec:
  selector:
    app: appv2
  ports:
  - name: http
    port: 80
    targetPort: portv2
```

直接创建上面两个服务：

```bash

[root@k8s-master1 test]# kubectl apply -f .
deployment.apps/appv1 created
service/appv1 created
deployment.apps/appv2 created
service/appv2 created

[root@k8s-master1 test]# kubectl get pods -l use=test
NAME                     READY   STATUS    RESTARTS   AGE
appv1-597bbc966f-chwpj   1/1     Running   0          69s
appv2-5f5489b4c5-7gsnd   1/1     Running   0          69s

```

 

在 Traefik2.1 中新增了一个 `TraefikService` 的 CRD 资源，我们可以直接利用这个对象来配置 WRR，之前的版本需要通过 File Provider，比较麻烦，新建一个描述 WRR 的资源清单：\(wrr.yaml\)

```bash
apiVersion: traefik.containo.us/v1alpha1
kind: TraefikService
metadata:
  name: app-wrr
spec:
  weighted:
    services:
      - name: appv1
        weight: 3  # 定义权重
        port: 80
        kind: Service  # 可选，默认就是 Service
      - name: appv2
        weight: 1
        port: 80
```

然后为我们的灰度发布的服务创建一个 IngressRoute 资源对象：\(ingressroute.yaml\)

```
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: wrringressroute
  namespace: default
spec:
  entryPoints:
    - web
  routes:
  - match: Host(`app.heian.com`)
    kind: Rule
    services:
    - name: app-wrr
      kind: TraefikService
```

不过需要注意的是现在我们配置的 Service 不再是直接的 Kubernetes 对象了，而是上面我们定义的 TraefikService 对象，直接创建上面的两个资源对象，这个时候我们对域名 `app.heian.com` 做上解析，去浏览器中连续访问 4 次，我们可以观察到 appv1 这应用会收到 3 次请求，而 appv2 这个应用只收到 1 次请求，符合上面我们的 `3:1` 的权重配置。

![](../../image/20210329201249896.png)![](../../image/20210329201258604.png)

## 6\. 流量复制

除了灰度发布之外，Traefik 2.0 还引入了流量镜像服务，是一种可以将流入流量复制并同时将其发送给其他服务的方法，镜像服务可以获得给定百分比的请求同时也会忽略这部分请求的响应。

![traefik mirror](../../image/3ef582f18b961679cb228f6d3a60e999.png)

同样的在 2.0 中只能通过 FileProvider 进行配置，在 2.1 版本中我们已经可以通过 `TraefikService` 资源对象来进行配置了，现在我们部署两个 whoami 的服务，资源清单文件如下所示：

```bash
apiVersion: v1
kind: Service
metadata:
  name: v1
spec:
  ports:
    - protocol: TCP
      name: web
      port: 80
  selector:
    app: v1
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: v1
  labels:
    app: v1
spec:
  selector:
    matchLabels:
      app: v1
  template:
    metadata:
      labels:
        app: v1
    spec:
      containers:
        - name: v1
          image: heian99/myapp:v1
          ports:
            - name: web
              containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: v2
spec:
  ports:
    - protocol: TCP
      name: web
      port: 80
  selector:
    app: v2
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: v2
  labels:
    app: v2
spec:
  selector:
    matchLabels:
      app: v2
  template:
    metadata:
      labels:
        app: v2
    spec:
      containers:
        - name: v2
          image: heian99/myapp:v2
          ports:
            - name: web
              containerPort: 80
```

![](../../image/20210329201913622.png)

现在我们创建一个 IngressRoute 对象，将服务 v1 的流量复制 50\% 到服务 v2，如下资源对象所示：\(mirror-ingress-route.yaml\)

```
apiVersion: traefik.containo.us/v1alpha1
kind: TraefikService
metadata:
  name: app-mirror
spec:
  mirroring:
    name: v1 # 发送 100% 的请求到 K8S 的 Service "v1"
    port: 80
    mirrors:
    - name: v2 # 然后复制 50% 的请求到 v2
      percent: 50
      port: 80
---
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: mirror-ingress-route
  namespace: default
spec:
  entryPoints:
  - web
  routes:   
  - match: Host(`mirror.heian.com`)
    kind: Rule
    services:
    - name: app-mirror
      kind: TraefikService # 使用声明的 TraefikService 服务，而不是 K8S 的 Service
```

这个时候我们在浏览器中去连续访问4次 `mirror.heian.com` 可以发现有一半的请求也出现在了 `v2` 这个服务中：

![](../../image/20210329202228445.png)

![](../../image/20210329202240576.png)