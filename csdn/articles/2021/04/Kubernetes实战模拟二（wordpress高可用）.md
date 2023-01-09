+++
author = "南宫乘风"
title = "Kubernetes实战模拟二（wordpress高可用）"
date = "2021-04-03 23:50:52"
tags=['kubernetes', '数据库', 'mysql', 'docker']
categories=[' Kubernetes项目实战', 'Kubernetes']
image = "post/4kdongman/98.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/115422781](https://blog.csdn.net/heian_99/article/details/115422781)

#  

# [Kubernetes实战模拟一（wordpress基础版）](https://blog.csdn.net/heian_99/article/details/115422455)

# [Kubernetes实战模拟二（wordpress高可用）](https://blog.csdn.net/heian_99/article/details/115422781)

# [Kubernetes实战模拟三（wordpress健康检查和服务质量QoS）](https://blog.csdn.net/heian_99/article/details/115433372)

# [Kubernetes实战模拟四（wordpress升级更新）](https://blog.csdn.net/heian_99/article/details/115468779)

源码地址：[https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example](https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example)

上一篇文件我们使用pod的构建两个容器，但是问题也是一大堆，根本不适合生产方面。

所以我们慢慢解决上面的问题，优化架构。

# 版本2

思路：将 Pod 中的两个容器进行拆分，将 Wordpress 和 MySQL 分别部署

Wordpress 用多个副本进行部署就可以实现应用的高可用了

由于 MySQL 是有状态应用，一般来说需要用 StatefulSet 来进行管理，但是我们这里部署的 MySQL 并不是集群模式，而是单副本的，所以用 Deployment 也是没有问题的。如果生产环境的话，一般都是集群的，分别在宿主机上部署。

 

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
      restartPolicy: Always
  selector:
    matchLabels:
      app: wordpress
      tier: mysql

```

这里给 MySQL 应用添加了一个 Service 对象，是因为 Wordpress 应用需要来连接数据库，之前在同一个 Pod 中用 `localhost` 即可，现在需要通过 Service 的 DNS 形式的域名进行连接。直接创建上面资源对象

```
# kubectl apply -f mysql.yaml    
service/wordpress-mysql created
deployment.apps/wordpress-mysql created
```

# Wordpress 清单

**wordpress.yaml**

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
  type: NodePort

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
  replicas: 4 
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
      restartPolicy: Always


```

注意这里的环境变量 `WORDPRESS_DB_HOST` 的值将之前的 `localhost` 地址更改成了上面 MySQL 服务的 DNS 地址，完整的域名应该是 `wordpress-mysql.kube-example.svc.cluster.local:3306`，由于这两个应该都处于同一个命名空间，所以直接简写成 `wordpress-mysql:3306` 也是可以的。

 

```
[root@k8s-master1 v2]# kubectl apply -f wordpress.yaml 
service/wordpress created
deployment.apps/wordpress created
[root@k8s-master1 v2]# kubectl get pods -l app=wordpress -n kube-example
NAME                              READY   STATUS    RESTARTS   AGE
wordpress-ddb4ff6cf-g2xf8         1/1     Running   0          9s
wordpress-ddb4ff6cf-jjt5k         1/1     Running   0          9s
wordpress-ddb4ff6cf-zmbc4         1/1     Running   0          9s
wordpress-mysql-d9b4b8985-bqv2b   1/1     Running   0          32s

```

# 测试

可以看到都已经是 `Running` 状态了，然后我们需要怎么来验证呢？是不是我们能想到的就是去访问下我们的 Wordpress 服务就可以了，我们这里还是使用的一个 NodePort 类型的 Service 来暴露服务：

```
[root@k8s-master1 v2]# kubectl get svc,ep -n kube-example 
NAME                      TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)        AGE
service/wordpress         NodePort    10.0.0.49    &lt;none&gt;        80:30455/TCP   92s
service/wordpress-mysql   ClusterIP   10.0.0.142   &lt;none&gt;        3306/TCP       115s

NAME                        ENDPOINTS                                       AGE
endpoints/wordpress         10.244.0.5:80,10.244.1.135:80,10.244.1.136:80   92s
endpoints/wordpress-mysql   10.244.1.134:3306                               115s

```

可以看到 wordpress 服务产生了一个 30455的端口，现在我们就可以通过 `http://&lt;任意节点的NodeIP&gt;:30012` 访问我们的应用了，在浏览器中打开，如果看到 wordpress 跳转到了安装页面，证明我们的安装是正确的，如果没有出现预期的效果，那么就需要去查看下 Pod 的日志来排查问题了，根据页面提示，填上对应的信息，点击`“安装”`即可，最终安装成功后

![20210403233421893.png](https://img-blog.csdnimg.cn/20210403233421893.png)

# 避免单点故障

为什么会有单点故障的问题呢？

我们不是部署了多个副本的 Wordpress 应用吗？

当我们设置 `replicas=1` 的时候肯定会存在单点故障问题，如果大于 1 但是所有副本都调度到了同一个节点的是不是同样就会存在单点问题了

这个节点挂了所有副本就都挂了，所以我们不仅需要设置多个副本数量，还需要让这些副本调度到不同的节点上，来打散避免单点故障

![20210403233825187.png](https://img-blog.csdnimg.cn/20210403233825187.png)

 Pod 反亲和性来实现了，我们可以防止单点故障出现。

但是要考虑要用**弱策略**还是**硬策略**

**我们首先弱的，如果硬策略，如果节点有问题，pod就不会被创建**

![2021040323393294.png](https://img-blog.csdnimg.cn/2021040323393294.png)

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
      affinity: #pod的反亲和力
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

# PDB策略

**PDB能够限制同时中断的pod的数量,以保证集群的高可用性**

有些时候线上的某些节点需要做一些维护操作，比如要升级内核，这个时候我们就需要将要维护的节点进行驱逐操作，驱逐节点首先是将节点设置为不可调度，这样可以避免有新的 Pod 调度上来，然后将该节点上的 Pod 全部删除，ReplicaSet 控制器检测到 Pod 数量减少了就会重新创建一个新的 Pod，调度到其他节点上面的，这个过程是先删除，再创建，并非是滚动更新，因此更新过程中，如果一个服务的所有副本都在被驱逐的节点上，则可能导致该服务不可用。

如果服务本身存在单点故障，所有副本都在同一个节点，驱逐的时候肯定就会造成服务不可用了，这种情况我们使用上面的反亲和性和多副本就可以解决这个问题。但是如果我们的服务本身就被打散在多个节点上，这些节点如果都被同时驱逐的话，那么这个服务的所有实例都会被同时删除，这个时候也会造成服务不可用了，这种情况下我们可以通过配置 PDB（PodDisruptionBudget）对象来避免所有副本同时被删除，比如我们可以设置在驱逐的时候 wordpress 应用最多只有一个副本不可用，其实就相当于逐个删除并在其它节点上重建

**pdb.yaml**

```
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

```
[root@k8s-master1 v2]# kubectl apply -f pdb.yaml 
poddisruptionbudget.policy/wordpress-pdb created
[root@k8s-master1 v2]# kubectl get pdb -n kube-example 
NAME            MIN AVAILABLE   MAX UNAVAILABLE   ALLOWED DISRUPTIONS   AGE
wordpress-pdb   N/A             1                 1                     15s

```

 PDB 的更多详细信息可以查看官方文档：[https://kubernetes.io/docs/tasks/run-application/configure-pdb/](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)。

 

此版本实现高可用，但是还有一些问题

# 问题

（1）pod的健康检查，如果没有这些，pod额度重启策略都无法执行

（2）内存，cpu等资源限制，服务质量Qos

（3）数据持久化

（4）mysql账号密码注入等

这些一些列问题，都会在后面的版本架构中优化
