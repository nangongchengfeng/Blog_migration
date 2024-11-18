---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2021-04-05 01:05:46
description: 实战模拟一基础版实战模拟二高可用实战模拟三健康检查和服务质量实战模拟四升级更新源码地址：实战模拟二，已经优化架构，已经采取分离，可以实现高可用，并优化软策略，防止单点故障接下来，慢慢实现健康检查和服务。。。。。。。
image: ../../title_pic/04.jpg
slug: '202104050105'
tags:
- Kubernetes
- kubernetes
- 数据库
- docker
- mysql
title: Kubernetes实战模拟三（wordpress健康检查和服务质量QoS）
---

<!--more-->

 

# [Kubernetes实战模拟一（wordpress基础版）](https://blog.csdn.net/heian_99/article/details/115422455)

# [Kubernetes实战模拟二（wordpress高可用）](https://blog.csdn.net/heian_99/article/details/115422781)

# [Kubernetes实战模拟三（wordpress健康检查和服务质量QoS）](https://blog.csdn.net/heian_99/article/details/115433372)

# [Kubernetes实战模拟四（wordpress升级更新）](https://blog.csdn.net/heian_99/article/details/115468779)

源码地址：<https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example>

Kubernetes实战模拟二，已经优化架构，已经采取分离，可以实现高可用，并优化软策略，防止单点故障

接下来，慢慢实现健康检查和服务质量

# 版本3

思路：分别对2个pod的进行端口检查，判断pod是否正常和流量提供，测试性能，设置资源限制

健康检查：主要检查pod提供正常服务

资源限制：后期可以根据这个设置HPA。防止宿主资源不足，被驱逐

**1、Pod的健康检查，也叫做探针，探针的种类有两种。**

1）、livenessProbe，健康状态检查，周期性检查服务是否存活，检查结果失败，将重启容器。  
2）、readinessProbe，可用性检查，周期性检查服务是否可用，不可用将从service的endpoints中移除。

**livenessProbe \(存活检查） # 如果检查失败，将杀死容器，根据Pod的restartPolicy来操作**

**readinessProbe（就绪检查） # 如果检查失败，kubernetes会把Pod从service endpoints中剔除**

 

**2、探针的检测方法。**

1）、exec，执行一段命令。  
2）、httpGet，检测某个http请求的返回状态码。  
3）、tcpSocket，测试某个端口是否能够连接。

 

**3、startupProbe检测**

判断容器内的应用程序是否已启动。如果提供了启动探测，则禁用所有其他探测，直到它成功为止。如果启动探测失败，kubelet将杀死容器，容器将服从其重启策略。如果容器没有提供启动探测，则默认状态为成功。

**注意：不要将startupProbe和readinessProbe混淆。**

 

 

 

> ## 配置Probe
> 
> Probe中有很多精确和详细的配置，通过它们你能准确的控制liveness和readiness检查：
> 
> - `initialDelaySeconds`：容器启动后第一次执行探测是需要等待多少秒。
> 
> - `periodSeconds`：执行探测的频率。默认是10秒，最小1秒。
> 
> - `timeoutSeconds`：探测超时时间。默认1秒，最小1秒。
> 
> - `successThreshold`：探测失败后，最少连续探测成功多少次才被认定为成功。默认是1。对于liveness必须是1。最小值是1。
> 
> - `failureThreshold`：探测成功后，最少连续探测失败多少次才被认定为失败。默认是3。最小值是1。
> 
> HTTP probe中可以给 `httpGet`设置其他配置项：
> 
> - `host`：连接的主机名，默认连接到pod的IP。你可能想在http header中设置”Host”而不是使用IP。
> 
> - `scheme`：连接使用的schema，默认HTTP。
> 
> - `path`: 访问的HTTP server的path。
> 
> - `httpHeaders`：自定义请求的header。HTTP运行重复的header。
> 
> - `port`：访问的容器的端口名字或者端口号。端口号必须介于1和65525之间。

 

# 命名空间：\(namespace.yaml\)

```bash
apiVersion: v1
kind: Namespace
metadata:
  name: kube-example
```

# mysql资源清单

**mysql.yaml**

```
apiVersion: v1
kind: Service
metadata:
  name: wordpress-mysql
  namespace: kube-example
  labels:
    app: wordpress
spec:
  selector:
    app: wordpress
    tier: mysql
  ports:
    - port: 3306
      targetPort: dbport

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress-mysql
  namespace: kube-example
  labels:
    app: wordpress
    tier: mysql
spec:
  replicas: 1
  template:
    metadata:
      name: wordpress-mysql
      labels:
        app: wordpress
        tier: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:5.7
          args:
          - --default_authentication_plugin=mysql_native_password
          - --character-set-server=utf8mb4
          - --collation-server=utf8mb4_unicode_ci
          ports:
            - containerPort: 3306
              name: dbport
          env:
          - name: MYSQL_ROOT_PASSWORD
            value: rootPassW0rd
          - name: MYSQL_DATABASE
            value: wordpress
          - name: MYSQL_USER
            value: wordpress
          - name: MYSQL_PASSWORD
            value: wordpress
          imagePullPolicy: IfNotPresent
          startupProbe:  #首次启动探测（如果没有成功，不会运行下面livenessProbe）
            tcpSocket:
              port: 3306
            failureThreshold: 2    #探测成功后，最少连续探测失败多少次才被认定为失败。默认是3。最小值是1。
            initialDelaySeconds: 20  # 容器启动后第一次执行探测是需要等待多少秒
            timeoutSeconds: 10  # 探测超时时间。默认1秒，最小1秒。
            periodSeconds: 10   # 执行探测的频率。默认是10秒，最小1秒。

         
      restartPolicy: Always
  selector:
    matchLabels:
      app: wordpress
      tier: mysql
```

因为这个是模拟环境，现在数据没有持续化，如果加上下面的检测，如果pod的有问题，直接重启，数据都会丢失，这个后期数据持久化，我们可以加上面

```bash
 livenessProbe:
            tcpSocket:
              port: 3306  # 访问的容器的端口名字或者端口号
            initialDelaySeconds: 10
            timeoutSeconds: 5
            failureThreshold: 5
            periodSeconds: 5
            successThreshold: 3  #探测失败后，最少连续探测成功多少次才被认定为成功。默认是1。对于liveness必须是1。最小值是1。
```

# Wordpress 清单

**wordpress.yaml**

我们的应用现在还有一个非常重要的功能没有提供，那就是健康检查，我们知道健康检查是提高应用健壮性非常重要的手段，当我们检测到应用不健康的时候我们希望可以自动重启容器，当应用还没有准备好的时候我们也希望暂时不要对外提供服务，所以我们需要添加我们前面经常提到的 `liveness probe` 和 `rediness probe` 两个健康检测探针，检查探针的方式有很多，我们这里当然可以认为如果容器的 80 端口可以成功访问那么就是健康的，对于一般的应用提供一个健康检查的 URL 会更好，这里我们添加一个如下所示的可读性探针，为什么不添加存活性探针呢？这里其实是考虑到线上错误排查的一个问题，如果当我们的应用出现了问题，然后就自动重启去掩盖错误的话，可能这个错误就会被永远忽略掉了，所以其实这是一个折衷的做法，不使用存活性探针，而是结合监控报警，保留错误现场，方便错误排查，但是可读写探针是一定需要添加的：

```
apiVersion: v1
kind: Service
metadata:
  name: wordpress
  namespace: kube-example
spec:
  selector:
    app: wordpress
    tier: frontend
  ports:
    - port: 80
      name: web
      targetPort: wdport
  type: ClusterIP

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  namespace: kube-example
  labels:
    app: wordpress
    tier: frontend
spec:
  selector:
    matchLabels:
      app: wordpress
      tier: frontend
  replicas: 4 #多副本+pod的反亲合力可以实现pod的高可用
  template:
    metadata:
      name: wordpress
      labels:
        app: wordpress
        tier: frontend
    spec:
      containers:
        - name: wordpress
          image: wordpress:5.3.2-apache
          ports:
            - containerPort: 80
              name: wdport
          env:
          - name: WORDPRESS_DB_HOST
            value: wordpress-mysql:3306
          - name: WORDPRESS_DB_USER
            value: wordpress
          - name: WORDPRESS_DB_PASSWORD
            value: wordpress
          imagePullPolicy: IfNotPresent

          startupProbe:  #首次启动探测（如果没有成功，不会运行下面livenessProbe）
            httpGet:
              port: 80
            failureThreshold: 2    #探测成功后，最少连续探测失败多少次才被认定为失败。默认是3。最小值是1。
            initialDelaySeconds: 10  # 容器启动后第一次执行探测是需要等待多少秒
            timeoutSeconds: 10 #  探测超时时间。默认1秒，最小1秒。
            periodSeconds: 5  # 执行探测的频率。默认是10秒，最小1秒。

          readinessProbe:  # （就绪检查） # 如果检查失败，kubernetes会把Pod从service endpoints中剔除
            httpGet:
              port: 80
            initialDelaySeconds: 10
            timeoutSeconds: 5
            failureThreshold: 5
            periodSeconds: 5
            successThreshold: 3
      affinity:
        podAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 1
              podAffinityTerm:
                topologyKey: kubernetes.io/hostname
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - wordpress
      restartPolicy: Always

```

上面为什么不用livenessProbe检测，首先如果livenessProbe检测失败，会直接重启pod的，会毁坏错误的信息，不方便我们排查问题。我们有多个副本，如果一个出问题，其余会正常工作

```bash
          livenessProbe:  #(存活检查） # 如果检查失败，将杀死容器，根据Pod的restartPolicy来操作
            httpGet:
              port: 80
            initialDelaySeconds: 15
            timeoutSeconds: 5
            periodSeconds: 5
            failureThreshold: 5
```

# PDB策略

**pdb.yaml**

```bash
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  name: wordpress-pdb
  namespace: kube-example
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: wordpress
      tier: frontend
```

 

# 服务质量 QoS

`QoS` 是 `Quality of Service` 的缩写，即服务质量。为了实现资源被有效调度和分配的同时提高资源利用率，Kubernetes 针对不同服务质量的预期，通过 `QoS` 来对 Pod 进行服务质量管理。对于一个 Pod 来说，服务质量体现在两个具体的指标：CPU 和内存。当节点上内存资源紧张时，Kubernetes 会根据预先设置的不同 `QoS` 类别进行相应处理。

`QoS` 主要分为 `Guaranteed`、`Burstable` 和 `Best-Effort`三类，优先级从高到低。我们先分别来介绍下这三种服务类型的定义。

**Guaranteed\(有保证的\)**

属于该级别的 Pod 有以下两种：

- Pod 中的**所有容器**都且**仅**设置了 CPU 和内存的 **limits**
- Pod 中的所有容器都设置了 CPU 和内存的 requests 和 limits ，且单个容器内的`requests==limits`（requests不等于0）

**Burstable\(不稳定的\)**

Pod 中只要有一个容器的 requests 和 limits 的设置不相同，那么该 Pod 的 QoS 即为 Burstable。

**Best-Effort\(尽最大努力\)**

如果 Pod 中所有容器的 resources 均未设置 requests 与 limits，该 Pod 的 QoS 即为 Best-Effort。

# fortio 部署

```
wget https://github.com/fortio/fortio/releases/download/v1.4.4/fortio-1.4.4-1.x86_64.rpm
rpm -ivh fortio-1.4.4-1.x86_64.rpm
nohup fortio server &
tail -f nohup.out
```

开始测压

命令行

> fortio load \-c 5 \-n 20 \-qps 0 http://www.baidu.com  
> #命令解释如下：  
>  \-c 表示并发数  
>  \-n 一共多少请求  
>  \-qps 每秒查询数，0 表示不限制

Web控制台

   web 控制台方式就是提供给习惯使用 web 界面操作的同学一个途径来使用 Fortio。因为是基于 web  方式，所以就需要首先启动一个 web server，这样客户端浏览器才可以访问到 web server 提供的操作界面进行负载压测。默认情况 fortio server 会启动 8080 端口，如下图所示：

   打开浏览器，输入 [http://IP:8080/fortio](http://192.168.10.11:8080/fortio)，访问 Fortio server：

根据实现生成环境访问人数和次数模拟

![](../../image/20210405005634842.png)

测试前

![](../../image/20210405005707289.png)

测试后

![](../../image/20210405005917148.png)

![](../../image/2021040500585839.png)

# 资源限制

采用**Guaranteed\(有保证的\)，防止宿主机资源不够被优先驱逐**

**wordpress**

```bash
          resources:
            limits:
              cpu: 800m
              memory: 150Mi
            requests:
              cpu: 800m
              memory: 150Mi
```

**mysql**

```bash
          resources:
            limits:
              cpu: 1000m
              memory: 400Mi
            requests:
              cpu: 1000m
              memory: 400Mi
```

此版本实现健康检查和服务质量QoS

# 问题

（1）自动扩缩容

（2）滚动更新策略

（3）数据持久化

（4）mysql账号密码注入等

这些一些列问题，都会在后面的版本架构中优化