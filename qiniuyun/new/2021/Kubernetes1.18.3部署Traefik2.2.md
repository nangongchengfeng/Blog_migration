---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-29 17:15:18
description: 部署官方文档：介绍是一款反向代理、负载均衡服务，使用实现的。和最大的不同是，它支持自动化更新反向代理和负载均衡配置。在微服务架构越来越流行的今天，一个业务恨不得有好几个数据库、后台服务和，开发团队拥有。。。。。。。
image: http://image.ownit.top/4kdongman/89.jpg
tags:
- Traefik
- kubernetes
- docker
- 运维
- traefik
title: Kubernetes 1.18.3 部署 Traefik2.2
---

<!--more-->

# Kubernetes 1.18.3 部署 Traefik2.0

> Centos 3.10.0-693.el7.x86\_64
> 
> Kubernetes 1.18.3
> 
> Traefik 2.2

```bash
[root@k8s-master1 traefik]# kubectl get cs
NAME                 STATUS    MESSAGE             ERROR
controller-manager   Healthy   ok                  
scheduler            Healthy   ok                  
etcd-0               Healthy   {"health":"true"}   
etcd-2               Healthy   {"health":"true"}   
etcd-1               Healthy   {"health":"true"}   
[root@k8s-master1 traefik]# kubectl get nodes
NAME         STATUS   ROLES    AGE    VERSION
k8s-master   Ready    <none>   6d1h   v1.18.3
k8s-node1    Ready    <none>   6d     v1.18.3
k8s-node2    Ready    <none>   6d     v1.18.3
[root@k8s-master1 traefik]# uname -a
Linux k8s-master1 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

```

Traefik 2.0 官方文档：https://docs.traefik.io/v2.0/

# 1.Traefik 介绍

traefik 是一款反向代理、负载均衡服务，使用 golang 实现的。和 nginx 最大的不同是，它支持自动化更新反向代理和负载均衡配置。在微服务架构越来越流行的今天，一个业务恨不得有好几个数据库、后台服务和 webapp，开发团队拥有一款 “智能” 的反向代理服务，为他们简化服务配置。traefik 就是为了解决这个问题而诞生的。

> Traefik 2.2新增的功能如下：  
> 1\. 支持了udp  
> 2\. traefik2.2 支持使用K/V存储做为动态配置的源，分别是 consul, etcd, Redis, zookeeper  
> 3\. 能够使用kubernetes CRD自定义资源定义UDP负载平衡 IngressRouteUDP。  
> 4\. 能够使用 rancher， consul catalog， docker和 marathon中的标签定义UDP的负载平衡  
> 5\. 增加了对ingress注解的主持  
> 6\. 将TLS存储功能 TLSStores添加到Kubernetes CRD中，使kubernetes用户无需使用配置文件和安装证书即可提供默认证书。  
> 7\. 在日志中增加了http的请求方式,是http还是https  
> 8\. 因为TLS的配置可能会影响CPU的使用率，因此增加了 TLS version和 TLS cipher使用的指标信息  
> 9\. 当前的WRR算法对于权重不平衡端点存在严重的偏差问题，将EDF调度算法用于WeightedRoundRobin， Envoy也是使用了 EOF调度算法  
> 10\. 支持请求主体用于流量镜像  
> 11\. 增加了 ElasticAPM作为traefik的tracing系统。  
> 12\. Traefik的Dashboard增加了UDP的页面  
> 13\. Traefik也增加了黑暗主题

# 2.部署 Traefik 2.0

`在 traefik v2.0 版本后，开始使用 CRD（Custom Resource Definition）来完成路由配置等，所以需要提前创建 CRD 资源。`

下面进行安装过程。

> 注：我们这里是将traefik部署在ingress-traefik命名空间，如果你需要部署在其他命名空间，需要更改资源清单，如果你是部署在和我同样的命令空间中，你需要创建该命名空间。

创建命名空间：

```bash
kubectl create ns ingress-traefik
```

创建CRD资源

Traefik 2.0版本后开始使用CRD来对资源进行管理配置，所以我们需要先创建CRD资源。

### traefik-crd.yaml

```bash
## IngressRoute
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: ingressroutes.traefik.containo.us
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: IngressRoute
    plural: ingressroutes
    singular: ingressroute
---
## IngressRouteTCP
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: ingressroutetcps.traefik.containo.us
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: IngressRouteTCP
    plural: ingressroutetcps
    singular: ingressroutetcp
---
## Middleware
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: middlewares.traefik.containo.us
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: Middleware
    plural: middlewares
    singular: middleware
---
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: tlsoptions.traefik.containo.us
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: TLSOption
    plural: tlsoptions
    singular: tlsoption
---
## TraefikService
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: traefikservices.traefik.containo.us
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: TraefikService
    plural: traefikservices
    singular: traefikservice

---
## TraefikTLSStore
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: tlsstores.traefik.containo.us
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: TLSStore
    plural: tlsstores
    singular: tlsstore

---
## IngressRouteUDP
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: ingressrouteudps.traefik.containo.us 
spec:
  scope: Namespaced
  group: traefik.containo.us
  version: v1alpha1
  names:
    kind: IngressRouteUDP
    plural: ingressrouteudps
    singular: ingressrouteudp
```

部署 CRD 资源

```bash
kubectl apply -f traefik-crd.yaml
```

创建 RBAC 权限

Kubernetes 在 1.6 以后的版本中引入了基于角色的访问控制（RBAC）策略，方便对 Kubernetes 资源和 API 进行细粒度控制。Traefik 需要一定的权限，所以这里提前创建好 Traefik ServiceAccount 并分配一定的权限。

### traefik-rbac.yaml

```bash
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: ingress-traefik 
  name: traefik-ingress-controller
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
rules:
  - apiGroups: [""]
    resources: ["services","endpoints","secrets"]
    verbs: ["get","list","watch"]
  - apiGroups: ["extensions"]
    resources: ["ingresses"]
    verbs: ["get","list","watch"]
  - apiGroups: ["extensions"]
    resources: ["ingresses/status"]
    verbs: ["update"]
  - apiGroups: ["traefik.containo.us"]
    resources: ["middlewares"]
    verbs: ["get","list","watch"]
  - apiGroups: ["traefik.containo.us"]
    resources: ["ingressroutes","traefikservices"]
    verbs: ["get","list","watch"]
  - apiGroups: ["traefik.containo.us"]
    resources: ["ingressroutetcps","ingressrouteudps"]
    verbs: ["get","list","watch"]
  - apiGroups: ["traefik.containo.us"]
    resources: ["tlsoptions","tlsstores"]
    verbs: ["get","list","watch"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: traefik-ingress-controller
subjects:
  - kind: ServiceAccount
    name: traefik-ingress-controller
    namespace: ingress-traefik
```

部署 Traefik RBAC 资源

```bash
kubectl apply -f traefik-rbac.yaml 
```

 

创建 Traefik 配置文件

由于 Traefik 配置很多，使用 CLI 定义操作过于繁琐，尽量使用将其配置选项放到配置文件中，然后存入 ConfigMap，将其挂入 traefik 中。

### traefik-config.yaml

```bash
kind: ConfigMap
apiVersion: v1
metadata:
  name: traefik-config
  namespace: ingress-traefik
data:
  traefik.yaml: |-
    serversTransport:
      insecureSkipVerify: true
    api:
      insecure: true
      dashboard: true
      debug: true
    metrics:
      prometheus: ""
    entryPoints:
      web:
        address: ":80"
      websecure:
        address: ":443"
    providers:
      kubernetesCRD: ""
      kubernetesingress: ""
    log:
      filePath: ""
      level: error
      format: json
    accessLog:
      filePath: ""
      format: json
      bufferingSize: 0
      filters:
        retryAttempts: true
        minDuration: 20
      fields:
        defaultMode: keep
        names:
          ClientUsername: drop
        headers:
          defaultMode: keep
          names:
            User-Agent: redact
            Authorization: drop
            Content-Type: keep
```

部署 Traefik ConfigMap 资源

```bash
kubectl apply -f traefik-config.yaml -n kube-system
```

设置Label标签

由于使用的Kubernetes DeamonSet方式部署Traefik，所以需要提前给节点设置Label，当程序部署Pod会自动调度到设置 Label的node节点上。

### 节点设置 Label 标签

```bash
kubectl label nodes k8s-node-1 IngressProxy=true
```

验证是否成功

```bash
[root@k8s-master1 traefik]# kubectl get node --show-labels 
NAME         STATUS   ROLES    AGE    VERSION   LABELS
k8s-master   Ready    <none>   6d1h   v1.18.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master,kubernetes.io/os=linux
k8s-node1    Ready    <none>   6d1h   v1.18.3   IngressProxy=true,beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node1,kubernetes.io/os=linux
k8s-node2    Ready    <none>   6d     v1.18.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,ingress=true,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node2,kubernetes.io/os=linux
```

节点删除Label标签

```bash
kubectl label nodes k8s-node-1 IngressProxy-
```

Kubernetes 部署 Traefik

按照以前Traefik1.7部署方式，使用DaemonSet类型部署，以便于在多服务器间扩展，使用 hostport 方式占用服务器 80、443 端口，方便流量进入。

### traefik-deploy.yaml

```bash
apiVersion: v1
kind: Service
metadata:
  name: traefik
  namespace: ingress-traefik
spec:
  ports:
    - name: web
      port: 80
    - name: websecure
      port: 443
    - name: admin
      port: 8080
  selector:
    app: traefik
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: traefik-ingress-controller
  namespace: ingress-traefik
  labels:
    app: traefik
spec:
  selector:
    matchLabels:
      app: traefik
  template:
    metadata:
      name: traefik
      labels:
        app: traefik
    spec:
      serviceAccountName: traefik-ingress-controller
      terminationGracePeriodSeconds: 1
      containers:
        - image: traefik:2.2.0
          name: traefik-ingress-lb
          ports:
            - name: web
              containerPort: 80
              hostPort: 80           #hostPort方式，将端口暴露到集群节点
            - name: websecure
              containerPort: 443
              hostPort: 443          #hostPort方式，将端口暴露到集群节点
            - name: admin
              containerPort: 8080
          resources:
            limits:
              cpu: 2000m
              memory: 1024Mi
            requests:
              cpu: 1000m
              memory: 1024Mi
          securityContext:
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
          args:
            - --configfile=/config/traefik.yaml
          volumeMounts:
            - mountPath: "/config"
              name: "config"
      volumes:
        - name: config
          configMap:
            name: traefik-config
      tolerations:              #设置容忍所有污点，防止节点被设置污点
        - operator: "Exists"
      nodeSelector:             #设置node筛选器，在特定label的节点上启动
        IngressProxy: "true"
```

部署 Traefik

```bash
kubectl apply -f traefik-deploy.yaml 
```

# 3.Traefik 路由规则基础配置

配置 HTTP 路由规则 （Traefik Dashboard 为例）

Traefik 应用已经部署完成，但是想让外部访问 Kubernetes 内部服务，还需要配置路由规则，这里开启了 Traefik Dashboard 配置，所以首先配置 Traefik Dashboard 看板的路由规则，使外部能够访问 Traefik Dashboard。

### traefik-dashboard-route.yaml

```bash
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-dashboard-route
  namespace: ingress-traefik
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`traefik.example.cn`)
      kind: Rule
      services:
        - name: traefik
          port: 8080
```

部署Traefik Dashboard 路由规则对象

```
kubectl apply -f traefik-dashboard-route.yaml
```

```bash
接下来配置dnsmasq，客户端想通过域名访问服务，必须要进行DNS解析，我使用的本地 DNS 服务器进行域名解析，将 Traefik 指定节点的 IP 和自定义 域名 绑定，重启dnsmasq服务即可。
打开任意浏览器输入地址：http://traefik.example.cn进行访问，此处没有配置验证登录，如果想配置验证登录，使用middleware即可。
```

![](http://image.ownit.top/csdn/20210329165939125.png)

# 4\. 配置 HTTPS 路由规则（Kubernetes Dashboard）

这里我们创建 Kubernetes 的 Dashboard，它是 基于 Https 协议方式访问，由于它是需要使用 Https 请求，所以我们需要配置 Https 的路由规则并指定证书。

[测试域名：kuboard.heian.com](http://kuboard.heian.com/)  （内网建立的）

创建证书文件

```bash
# 创建自签名证书
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=kuboard.heian.com"

# 将证书存储到Kubernetes Secret中，新建的k8dash-sa-tls必须与k8dash-route中的tls: secretName一致。
kubectl create secret tls k8dash-sa-tls --key=tls.key --cert=tls.crt -n kube-system
```

### k8dash-route.yaml

```bash
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: k8dash-sa-route
  namespace: kube-system
spec:
  entryPoints:
    - websecure
  tls:
    secretName: k8dash-sa-tls
  routes:
    - match: Host(`kuboard.heian.com`)
      kind: Rule
      services:
# 此处的services是Kubernetes中的svc name 与 端口 可以使用kubectl get svc --namespace=kube-system获取
        - name: kuboard
          port: 80
```

打开任意浏览器输入地址：https://[kuboard.heian.com](http://kuboard.heian.com/)进行访问 

 

![](http://image.ownit.top/csdn/202103291713116.png)![](http://image.ownit.top/csdn/20210329171353971.png)

![](http://image.ownit.top/csdn/20210329171851530.png)

![](http://image.ownit.top/csdn/20210329171908946.png)