---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-20 17:38:51
description: 、什么是在时添加暴露从集群外到集群内服务的或路由。定义在资源上的规则控制流量的路由。一个可以配置用于提供外部可访问的服务、负载均衡流量、终端和提供虚拟主机名配置。负责实现通常使用负载均衡器入口。但是它。。。。。。。
image: http://image.ownit.top/4kdongman/98.jpg
tags:
- Kubernetes应用
- nginx
- kubernetes
- ingress
title: Kubernetes Ingress-nginx高级用法
---

<!--more-->

## 1、什么是ingress

ngress（在kubernetes v1.1时添加）暴露从集群外到集群内服务的`HTTP`或`HTTPS`路由。定义在`ingress`资源上的规则控制流量的路由。

```
    internet
        |
   [ Ingress ]
   --|-----|--
   [ Services ]
```

一个`ingress`可以配置用于提供外部可访问的服务url、负载均衡流量、SSL终端和提供虚拟主机名配置。`ingress controller`负责实现（通常使用负载均衡器\(loadbalancer\)）入口（ingress）。但是它也可以配置你的边缘路由器或额外的前端来帮助处理流量。  
`ingress`不暴露任何端口或协议。将HTTP和HTTPS之外的服务公开到因特网通常使用类型是NodePort或loadbalance的service。

 

![](http://image.ownit.top/csdn/20200206204556322.png)

## 2、Ingress区别

差别：<https://github.com/nginxinc/kubernetes-ingress/blob/master/docs/nginx-ingress-controllers.md>

### Ingress-nginx

Ingress-nginx：kubernetes官方维护的ingress

Ingress-nginx的官方文档：<https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#rewrite>

Ingress-nginx Github：<https://github.com/kubernetes/ingress-nginx>

### Nginx-ingress

Nginx-ingress：nginx官方维护的ingress

Nginx-ingress的官方文档：<https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/>

Nginx-ingress Github：<https://github.com/nginxinc/kubernetes-ingress/blob/master/docs/nginx-ingress-controllers.md>

 

类似的还有：Traefik、HAProxy、Istio

 

## 3、Ingress-nginx部署

[（1）yaml部署Ingress-nginx](https://blog.csdn.net/heian_99/article/details/104201990)

[（2）helm部署Ingress-nginx](https://www.cnblogs.com/bigberg/p/13926052.html)

 

Ingress-nginx的高级介绍，我这边以Kubernetes的那个插件为主。

## 4、Ingress-nginx创建流程

（1）首先创建pod

（2）创建service

（3）创建ingress-nginx

![](http://image.ownit.top/csdn/20210319223654383.png)

```bash
kubectl create ns heian
#创建命名空间后，运行下面yaml，就可以实现上面三个步骤的工作

---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: heian
  name: ingress-heian
  annotations:
    k8s.kuboard.cn/workload: ingress-heian
    deployment.kubernetes.io/revision: '1'
    k8s.kuboard.cn/service: ClusterIP
    k8s.kuboard.cn/ingress: 'true'
  labels:
    app: ingress-heian
spec:
  selector:
    matchLabels:
      app: ingress-heian
  revisionHistoryLimit: 10
  template:
    metadata:
      labels:
        app: ingress-heian
    spec:
      affinity: {}
      securityContext:
        seLinuxOptions: {}
      imagePullSecrets: []
      restartPolicy: Always
      initContainers: []
      containers:
        - image: 'wangyanglinux/myapp:v1'
          imagePullPolicy: IfNotPresent
          name: ingress-heian
          volumeMounts:
            - name: tz-config
              mountPath: /usr/share/zoneinfo/Asia/Shanghai
            - name: tz-config
              mountPath: /etc/localtime
            - name: timezone
              mountPath: /etc/timezone
          resources:
            limits:
              cpu: 100m
              memory: 100Mi
            requests:
              cpu: 10m
              memory: 10Mi
          env:
            - name: TZ
              value: Asia/Shanghai
            - name: LANG
              value: C.UTF-8
          lifecycle: {}
          ports:
            - name: web
              containerPort: 80
              protocol: TCP
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
      volumes:
        - name: tz-config
          hostPath:
            path: /usr/share/zoneinfo/Asia/Shanghai
            type: ''
        - name: timezone
          hostPath:
            path: /etc/timezone
            type: ''
      dnsPolicy: ClusterFirst
      dnsConfig:
        options: []
      schedulerName: default-scheduler
      terminationGracePeriodSeconds: 30
  progressDeadlineSeconds: 600
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  replicas: 1

---
apiVersion: v1
kind: Service
metadata:
  namespace: heian
  name: ingress-heian
  annotations:
    k8s.kuboard.cn/workload: ingress-heian
  labels:
    app: ingress-heian
spec:
  selector:
    app: ingress-heian
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
      name: ingress-web-1
      nodePort: 0
  sessionAffinity: None

---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  namespace: heian
  name: ingress-heian
  annotations:
    k8s.kuboard.cn/workload: ingress-heian
  labels:
    app: ingress-heian
spec:
  rules:
    - host: ingress.heian.com
      http:
        paths:
          - path: /
            backend:
              serviceName: ingress-heian
              servicePort: 80

```

效果截图：

![](http://image.ownit.top/csdn/20210319230652392.png)

## 5、Ingress-nginx的域名重定向（Redirect）

**annotations声明**

```bash
#重定向，就是这一句 ，现在访问这个域名，会重定向到我的博客地址
annotations:
    nginx.ingress.kubernetes.io/permanent-redirect: 'https://blog.csdn.net/heian_99'
```

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/permanent-redirect: 'https://blog.csdn.net/heian_99'
  name: ingress-heian
  namespace: heian
spec:
  rules:
    - host: ingress.heian.com
      http:
        paths:
          - backend:
              serviceName: ingress-heian
              servicePort: 80
            path: /
            pathType: ImplementationSpecific
```

这个是ingress-nginx里面nginx的配置

![](http://image.ownit.top/csdn/20210319232247458.png)

 

## 6、Ingress-nginx的前后端分离（Rewrite）

```bash
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
```

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  name: ingress-heian
  namespace: heian
spec:
  rules:
    - host: ingress.heian.com
      http:
        paths:
          - backend:
              serviceName: ingress-heian
              servicePort: 80
            path: /something(/|$)(.*)
            pathType: ImplementationSpecific
```

![](http://image.ownit.top/csdn/20210319233725336.png)

![](http://image.ownit.top/csdn/20210319233746567.png)

## 7、Ingress-nginx的SSL配置

官网：<https://kubernetes.github.io/ingress-nginx/user-guide/tls/>

创建自建证书（主：浏览器不认可的）

Ingress-nginx配置了SSL，会自动跳转到https的网页的

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.cert -subj "/CN=ingress.heian.com/O=ingress.heian.com"

kubectl create secret tls ca-ceart --key tls.key --cert tls.cert -n heian
```

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  name: ingress-heian
  namespace: heian
spec:
  rules:
    - host: ingress.heian.com
      http:
        paths:
          - backend:
              serviceName: ingress-heian
              servicePort: 80
            path: /something(/|$)(.*)
            pathType: ImplementationSpecific
  tls:
    - hosts:
        - ingress.heian.com
      secretName: ca-ceart
```

```bash
  tls:
    - hosts:
        - ingress.heian.com
      secretName: ca-ceart
```

![](http://image.ownit.top/csdn/20210319235729737.png)

**禁用https强制跳转**

```bash
  annotations:
     nginx.ingress.kubernetes.io/ssl-redirect: "false"
```

设置默认证书：\--default-ssl-certificate=default/foo-tls

更改的ingress-controller的启动参数

## 8、Ingress-nginx的黑白名单

       Annotations：只对指定的ingress生效

       ConfigMap：全局生效

黑名单可以使用ConfigMap去配置，白名单建议使用Annotations去配置。

### （1）、白名单 添加白名单的方式可以直接写annotation，也可以配置在ConfigMap中。

写在annotation中：

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/whitelist-source-range: 192.168.0.100
  name: ingress-heian
  namespace: heian
spec:
  rules:
    - host: ingress.heian.com
      http:
        paths:
          - backend:
              serviceName: ingress-heian
              servicePort: 80
            path: /
            pathType: ImplementationSpecific
```

![](http://image.ownit.top/csdn/20210320111859311.png)

![](http://image.ownit.top/csdn/20210320111926614.png)

也可以写固定IP，也可以写网段。 配置到ConfigMap中：

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    helm.sh/chart: ingress-nginx-2.1.0
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 0.32.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
data:
  whitelist-source-range: 10.1.10.0/24
```

### （2）、黑名单 黑名单就只能通过ConfigMap来配置

ConfigMap配置如下：

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    helm.sh/chart: ingress-nginx-2.1.0
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 0.32.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
data:
  whitelist-source-range: 10.1.10.0/24
  block-cidrs: 10.1.10.100
```

annotation配置

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/server-snippet: |-
      deny 192.168.0.1;
      deny 192.168.0.100;
      allow all;
  creationTimestamp: null
  name: ingress-heian
spec:
  rules:
  - host: ingress.heian.com
    http:
      paths:
      - backend:
          serviceName: ingress-heian
          servicePort: 80
        path: /
        pathType: ImplementationSpecific
status:
  loadBalancer: {}
```

## 9、Ingress-nginx的匹配请求头

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/server-snippet: |-
      set $agentflag 0;

              if ($http_user_agent ~* "(iPhone)" ){
                set $agentflag 1;
              }

              if ( $agentflag = 1 ) {
                return 301 https://m.heian.com;
              }
  creationTimestamp: null
  name: ingress-heian
spec:
  rules:
  - host: ingress.heian.com
    http:
      paths:
      - backend:
          serviceName: ingress-heian
          servicePort: 80
        path: /
        pathType: ImplementationSpecific
status:
  loadBalancer: {}
```

![](http://image.ownit.top/csdn/20210320113534150.png)

 

## 10、Ingress-nginx的速率限制

```bash
限速¶
这些注释定义了对连接和传输速率的限制。这些可以用来减轻DDoS攻击。

nginx.ingress.kubernetes.io/limit-connections：单个IP地址允许的并发连接数。超出此限制时，将返回503错误。
nginx.ingress.kubernetes.io/limit-rps：每秒从给定IP接受的请求数。突发限制设置为此限制乘以突发乘数，默认乘数为5。当客户端超过此限制时，将 返回limit-req-status-code默认值： 503。
nginx.ingress.kubernetes.io/limit-rpm：每分钟从给定IP接受的请求数。突发限制设置为此限制乘以突发乘数，默认乘数为5。当客户端超过此限制时，将 返回limit-req-status-code默认值： 503。
nginx.ingress.kubernetes.io/limit-burst-multiplier：突发大小限制速率的倍数。默认的脉冲串乘数为5，此注释将覆盖默认的乘数。当客户端超过此限制时，将 返回limit-req-status-code默认值： 503。
nginx.ingress.kubernetes.io/limit-rate-after：最初的千字节数，在此之后，对给定连接的响应的进一步传输将受到速率的限制。必须在启用代理缓冲的情况下使用此功能。
nginx.ingress.kubernetes.io/limit-rate：每秒允许发送到给定连接的千字节数。零值禁用速率限制。必须在启用代理缓冲的情况下使用此功能。
nginx.ingress.kubernetes.io/limit-whitelist：客户端IP源范围要从速率限制中排除。该值是逗号分隔的CIDR列表。
```

```bash
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: ingress-nginx
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/limit-rate: 100K
    nginx.ingress.kubernetes.io/limit-whitelist: 10.1.10.100
    nginx.ingress.kubernetes.io/limit-rps: 1
    nginx.ingress.kubernetes.io/limit-rpm: 30
spec:
  rules:
  - host: iphone.coolops.cn 
    http:
      paths:
      - path: 
        backend:
          serviceName: ng-svc
          servicePort: 80



nginx.ingress.kubernetes.io/limit-rate：限制客户端每秒传输的字节数
nginx.ingress.kubernetes.io/limit-whitelist：白名单中的IP不限速
nginx.ingress.kubernetes.io/limit-rps：单个IP每秒的连接数
nginx.ingress.kubernetes.io/limit-rpm：单个IP每分钟的连接数
```

 

## 11、Ingress-nginx的基本认证

有些访问是需要认证访问的，比如dubbo-admin，我们在访问的时候会先叫你输入用户名和密码。ingress nginx也可以实现这种。

### （1）、创建密码，我这里用http的命令工具来生成

```bash
[root@k8s-master01 ingress]# htpasswd -c auth heian
New password: 
Re-type new password: 
Adding password for user heian
[root@k8s-master01 ingress]# ls
auth  tls.cert  tls.key
[root@k8s-master01 ingress]# cat auth 
heian:$apr1$8LffOJL7$ZIGV4XRNSuginqO5GMxAZ.
[root@k8s-master01 ingress]# 
```

### （2）、创建secret

```bash
[root@k8s-master01 ingress]# kubectl create secret generic basic-auth --from-file=auth -n heian 
secret/basic-auth created
```

### （3）、配置Ingress

```bash
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/auth-realm: Need to longin
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-type: basic
  creationTimestamp: null
  name: ingress-heian
spec:
  rules:
  - host: ingress.heian.com
    http:
      paths:
      - backend:
          serviceName: ingress-heian
          servicePort: 80
        path: /
        pathType: ImplementationSpecific
status:
  loadBalancer: {}
```

![](http://image.ownit.top/csdn/2021032013214395.png)

## 12、Ingress-nginx实现灰度金丝雀发布

 

![](http://image.ownit.top/csdn/20210320132622913.png)

 

> Nginx Annotations 支持以下 4 种 Canary 规则：
> 
> - `nginx.ingress.kubernetes.io/canary-by-header`：基于 Request Header 的流量切分，适用于灰度发布以及 A/B 测试。当 Request Header 设置为 `always`时，请求将会被一直发送到 Canary 版本；当 Request Header 设置为 `never`时，请求不会被发送到 Canary 入口；对于任何其他 Header 值，将忽略 Header，并通过优先级将请求与其他金丝雀规则进行优先级的比较。
> - `nginx.ingress.kubernetes.io/canary-by-header-value`：要匹配的 Request Header 的值，用于通知 Ingress 将请求路由到 Canary Ingress 中指定的服务。当 Request Header 设置为此值时，它将被路由到 Canary 入口。该规则允许用户自定义 Request Header 的值，必须与上一个 annotation \(即：canary-by-header）一起使用。
> - `nginx.ingress.kubernetes.io/canary-weight`：基于服务权重的流量切分，适用于蓝绿部署，权重范围 0 - 100 按百分比将请求路由到 Canary Ingress 中指定的服务。权重为 0 意味着该金丝雀规则不会向 Canary 入口的服务发送任何请求。权重为 100 意味着所有请求都将被发送到 Canary 入口。
> - `nginx.ingress.kubernetes.io/canary-by-cookie`：基于 Cookie 的流量切分，适用于灰度发布与 A/B 测试。用于通知 Ingress 将请求路由到 Canary Ingress 中指定的服务的cookie。当 cookie 值设置为 `always`时，它将被路由到 Canary 入口；当 cookie 值设置为 `never`时，请求不会被发送到 Canary 入口；对于任何其他值，将忽略 cookie 并将请求与其他金丝雀规则进行优先级的比较。 定义两个版本的代码。

创建两个同域名的ingress

**v2版**

```bash
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: heian
    nginx.ingress.kubernetes.io/canary-by-header-value: v2
    nginx.ingress.kubernetes.io/canary-weight: "50"
  name: ingress-heian2
  namespace: heian
spec:
  rules:
  - host: ingress.heian.com
    http:
      paths:
      - backend:
          serviceName: ingress-heian2
          servicePort: 80
        path: /
        pathType: ImplementationSpecific
```

![](http://image.ownit.top/csdn/20210320135014976.png)

 

## 13、Ingress-nginx自定义错误页面

github地址：<https://github.com/kubernetes/ingress-nginx/blob/master/docs/examples/customization/custom-errors/custom-default-backend.yaml>

```bash
kubectl apply -f error.yaml -n heian
```

修改ds配置文件，添加这个

```bash
        - --default-backend-service=heian/nginx-errors
```

![](http://image.ownit.top/csdn/20210320173720693.png)

 

![](http://image.ownit.top/csdn/20210320173801591.png)

验证

执行 `kubectl get pod \-n ingress-nginx` 查看pod是否已经重启过， 如果没有自动重启，需要杀掉pod。  
打开一个不存在的链接， 查看是否显示的是定义的错误页面。  
部分浏览器不支持页面显示，如谷歌浏览器会显示“无法显示此网站”