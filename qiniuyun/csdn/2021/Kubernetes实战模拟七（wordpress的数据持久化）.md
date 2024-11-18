---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-04-08 00:01:28
description: 实战模拟一基础版实战模拟二高可用实战模拟三健康检查和服务质量实战模拟四升级更新实战模拟五的自动扩缩容实战模拟六的账号信息加密源码地址：实战模拟六，已经构建的账号信息加密，和时间校准。版本思路：想和的数。。。。。。。
image: ../../title_pic/12.jpg
slug: '202104080001'
tags:
- Kubernetes项目实战
- kubernetes
- 数据库
- mysql
- nfs
title: Kubernetes实战模拟七（wordpress的数据持久化）
---

<!--more-->

# [Kubernetes实战模拟一（wordpress基础版）](https://blog.csdn.net/heian_99/article/details/115422455)

# [Kubernetes实战模拟二（wordpress高可用）](https://blog.csdn.net/heian_99/article/details/115422781)

# [Kubernetes实战模拟三（wordpress健康检查和服务质量QoS）](https://blog.csdn.net/heian_99/article/details/115433372)

# [Kubernetes实战模拟四（wordpress升级更新）](https://blog.csdn.net/heian_99/article/details/115468779)

# [Kubernetes实战模拟五（wordpress的HPA自动扩缩容）](https://blog.csdn.net/heian_99/article/details/115477746)

# [Kubernetes实战模拟六（wordpress的账号信息加密）](https://blog.csdn.net/heian_99/article/details/115488011)

源码地址：<https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example>

**Kubernetes实战模拟六，已经构建wordpress的账号信息加密，和时间校准。**

 

# 版本6

**思路：想mysql和wordpress的数据持久化，总不能把数据放到容器中，如果容器重启或者删除，那么数据将都会消失的。接下来我们采用nfs实践（其实后端存储使用ceph比较好，安全性和高可用。这边方便演示采用nfs）**

 

# NFS

```
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

# helm安装nfs-client

```
stable       	https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
helm添加这个源
```

```
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

```
安装
helm install nfs-client-provisioner -n nfs .

卸载
helm uninstall -n nfs nfs-client-provisioner
```

![](../../image/20210407234925257.png)

# **mysql**数据持久化

### **mysql-nfs.yaml.yaml**

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-nfs
  namespace: kube-example
  labels:
    app: mysql
spec:
  storageClassName: "nfs-client"  #存储后端
  accessModes:
    - ReadWriteOnce  #允许一个容器连接，读写
  resources:
    requests:
      storage: 1G  #存储量
```

### mysql.yaml

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
          image: mysql:5.6
          args:
          - --character-set-server=utf8mb4
          - --collation-server=utf8mb4_unicode_ci

          volumeMounts:
            - mountPath: /var/lib/mysql
              name: mysql-nfs
          ports:
            - containerPort: 3306
              name: dbport
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
      volumes:
        - name: mysql-nfs
          persistentVolumeClaim:
            claimName: mysql-nfs
  selector:
    matchLabels:
      app: wordpress
      tier: mysql
```

# wordpress数据持久化

### wordpress-nfs.yaml

但是由于 Wordpress 应用是多个副本，所以需要同时在多个节点进行读写，也就是 `accessModes` 需要 `ReadWriteMany` 模式

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wordpress-nfs
  namespace: kube-example
  labels:
    app: wordpress
spec:
  storageClassName: "nfs-client"
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 2G
```

### wordpress.yaml

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
          #pvc挂载到容器目录
          volumeMounts:
            - mountPath: /var/www/html
              name: wordpress-nfs
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
      #挂载的pvc
      volumes:
        - name: wordpress-nfs
          persistentVolumeClaim:
            claimName: wordpress-nfs

```

# 测试

![](../../image/20210407235714928.png)

 

![](../../image/20210407235735554.png)

 

现在删除或者重启pod的数据都不会丢失，我们已经把数据放在固定的节点，通过网络进行访问

但是，NFS只适合测试环境，或者数据不重要的前提下。如果数据重要，我们需要使用ceph来作为Kubernetes的存储后端

好了，我们wordpress模拟接近尾声，但是我这些只完成一版，生产环境远远比这复杂和安全，我们后期可以不断慢慢的完善