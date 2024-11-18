---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-04-07 16:57:04
description: 实战模拟一基础版实战模拟二高可用实战模拟三健康检查和服务质量实战模拟四升级更新实战模拟五的自动扩缩容源码地址：实战模拟五，已经构建的自动扩缩容，可以面对业务并发版本思路：想和，交互连接时，需要账号和密。。。。。。。
image: ../../title_pic/58.jpg
slug: '202104071657'
tags:
- Kubernetes项目实战
- kubernetes
- mysql
- 数据库
title: Kubernetes实战模拟六（wordpress的账号信息加密）
---

<!--more-->

# [Kubernetes实战模拟一（wordpress基础版）](https://blog.csdn.net/heian_99/article/details/115422455)

# [Kubernetes实战模拟二（wordpress高可用）](https://blog.csdn.net/heian_99/article/details/115422781)

# [Kubernetes实战模拟三（wordpress健康检查和服务质量QoS）](https://blog.csdn.net/heian_99/article/details/115433372)

# [Kubernetes实战模拟四（wordpress升级更新）](https://blog.csdn.net/heian_99/article/details/115468779)

# [Kubernetes实战模拟五（wordpress的HPA自动扩缩容）](https://blog.csdn.net/heian_99/article/details/115477746)

源码地址：<https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example>

**Kubernetes实战模拟五，已经构建wordpress的HPA自动扩缩容，可以面对业务并发**

 

# 版本6

**思路：想mysql和wordpress，交互连接时，需要账号和密码，我们不希望明文显示，这里我们可以使用secrets加密，然后挂载到env环境中。**

安全性这个和具体的业务应用有关系，比如我们这里的 Wordpress 也就是数据库的密码属于比较私密的信息，我们可以使用 Kubernetes 中的 Secret 资源对象来存储比较私密的信息

 

# secrets

**db-secrets.yaml**

```bash
apiVersion: v1
data:
  WORDPRESS_DB_HOST: d29yZHByZXNzLW15c3FsOjMzMDY=
  WORDPRESS_DB_PASSWORD: d29yZHByZXNz
  WORDPRESS_DB_USER: d29yZHByZXNz
  MYSQL_ROOT_PASSWORD: cm9vdFBhc3NXMHJk
  MYSQL_DATABASE: d29yZHByZXNz
kind: Secret
metadata:
  name: db.conf
  namespace: kube-example
type: Opaque
```

这边当时遇见一个问题  <https://blog.csdn.net/heian_99/article/details/115486589>  已经解决，可以参照这个。

然后将Deployment 资源对象中的数据库密码环境变量通过 Secret 对象读取

**mysql.yaml**

```bash
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
          #环境注入
          env:
          - name: MYSQL_ROOT_PASSWORD
            valueFrom:
              secretKeyRef:
                key: MYSQL_ROOT_PASSWORD
                name: db.conf
          - name: MYSQL_DATABASE
            valueFrom:
              secretKeyRef:
                key: MYSQL_DATABASE
                name: db.conf
          - name: MYSQL_USER
            valueFrom:
              secretKeyRef:
                key: WORDPRESS_DB_USER
                name: db.conf
          - name: MYSQL_PASSWORD
            valueFrom:
              secretKeyRef:
                key: WORDPRESS_DB_PASSWORD
                name: db.conf
          imagePullPolicy: IfNotPresent
          resources:
            limits:
              cpu: 1000m
              memory: 400Mi
            requests:
              cpu: 1000m
              memory: 400Mi
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

**wordpress.yaml**

```bash
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
  replicas: 3   #多副本+pod的反亲合力可以实现pod的高可用
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
          # 环境注入
          env:
          - name: WORDPRESS_DB_HOST
            valueFrom:
              secretKeyRef:
                key: WORDPRESS_DB_HOST
                name: db.conf
          - name: WORDPRESS_DB_USER
            valueFrom:
              secretKeyRef:
                key: WORDPRESS_DB_USER
                name: db.conf
          - name: WORDPRESS_DB_PASSWORD
            valueFrom:
              secretKeyRef:
                key: WORDPRESS_DB_PASSWORD
                name: db.conf
          imagePullPolicy: IfNotPresent
          resources:
            limits:
              cpu: 800m
              memory: 150Mi
            requests:
              cpu: 800m
              memory: 150Mi
          startupProbe:  #首次启动探测（如果没有成功，不会运行下面livenessProbe）
            httpGet:
              port: 80
            failureThreshold: 2    #探测成功后，最少连续探测失败多少次才被认定为失败。默认是3。最小值是1。
            initialDelaySeconds: 20  # 容器启动后第一次执行探测是需要等待多少秒
            timeoutSeconds: 10 #  探测超时时间。默认1秒，最小1秒。
            periodSeconds: 5  # 执行探测的频率。默认是10秒，最小1秒。

          readinessProbe:  # （就绪检查） # 如果检查失败，kubernetes会把Pod从service endpoints中剔除
            tcpSocket:
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

 

这样我们就不会在 YAML 文件中看到明文的数据库密码了，当然安全性都是相对的，Secret 资源对象也只是简单的将密码做了一次 Base64 编码而已，对于一些特殊场景安全性要求非常高的应用，就需要使用其他功能更加强大的密码系统来进行管理了，比如 [Vault](https://www.vaultproject.io/)。

我们的配置也让Secret管理，也方便修改和配置

![](../../image/20210407162606423.png)