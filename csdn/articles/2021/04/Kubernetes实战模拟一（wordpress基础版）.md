+++
author = "南宫乘风"
title = "Kubernetes实战模拟一（wordpress基础版）"
date = "2021-04-03 23:47:45"
tags=['kubernetes', 'mysql', 'docker']
categories=[' Kubernetes项目实战', 'Kubernetes']
image = "post/4kdongman/05.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/115422455](https://blog.csdn.net/heian_99/article/details/115422455)

# [Kubernetes实战模拟一（wordpress基础版）](https://blog.csdn.net/heian_99/article/details/115422455)

# [Kubernetes实战模拟二（wordpress高可用）](https://blog.csdn.net/heian_99/article/details/115422781)

# [Kubernetes实战模拟三（wordpress健康检查和服务质量QoS）](https://blog.csdn.net/heian_99/article/details/115433372)

# [Kubernetes实战模拟四（wordpress升级更新）](https://blog.csdn.net/heian_99/article/details/115468779)

Kubernetes是现在比较流行的容器化软件。我们日常也比较使用的多，我们都是慢慢的从陌生到熟悉的进阶，只有不断的学习，才能有收获。

Kubernetes专栏：[https://blog.csdn.net/heian_99/category_9652886.html](https://blog.csdn.net/heian_99/category_9652886.html)

Kubernetes官网地址：[https://kubernetes.io/](https://kubernetes.io/)

这个专栏，模拟Kubernetes的日常发布流程。

源码地址：[https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example](https://github.com/nangongchengfeng/Kubernetes/tree/main/wordpress-example)

里面包含多个版本，现在是演示v1版本。

# 环境

>  
 Kubernetes：v1.18.3 
 docker：19.03.9 
 mysql：5.7 
 wordpress：5.3.2-apache 


# 版本1

思路：由于wordpress和mysql需要进行交互。版本1就把wordpress和mysql集成到一个pod运行，测试访问效果

# 原理

### Wordpress 

Wordpress 是一个基于 PHP 和 MySQL 的流行的开源内容管理系统，拥有丰富的插件和模板系统。一个能够解析 PHP 的程序和 MySQL 数据库。官方提供了镜像 [https://hub.docker.com/_/wordpress](https://hub.docker.com/_/wordpress)

可以通过一系列环境变量去指定 MySQL 数据库的配置，只需要将这些参数配置上直接运行即可。

我们知道 Wordpress 应用本身会频繁的和 MySQL 数据库进行交互，这种情况下如果将二者用容器部署在同一个 Pod 下面是不是要高效很多

因为一个 Pod 下面的所有容器是共享同一个 network namespace 的，下面我们就来部署我们的应用

 

# 命名空间：(namespace.yaml)

```
apiVersion: v1
kind: Namespace
metadata:
  name: kube-example
```

# 应用清单：（deployment.yaml）

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  namespace: kube-example
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      containers:
      - name: wordpress
        image: wordpress:5.3.2-apache
        ports:
        - containerPort: 80
          name: wdport
        env:
        - name: WORDPRESS_DB_HOST
          value: localhost:3306
        - name: WORDPRESS_DB_USER
          value: wordpress
        - name: WORDPRESS_DB_PASSWORD
          value: wordpress
      - name: mysql
        image: mysql:5.7
        imagePullPolicy: IfNotPresent
        args:  # 新版本镜像有更新，需要使用下面的认证插件环境变量配置才会生效
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
```

由于我们这里 MySQL 和 Wordpress 在同一个 Pod 下面，所以在 Wordpress 中我们指定数据库地址的时候是用的 `localhost:3306`，因为这两个容器已经共享同一个 network namespace 了，这点很重要，然后如果我们要想把这个服务暴露给外部用户还得创建一个 Service 或者 Ingress 对象

# NodePort 类型的 Service：(service.yaml)

```
apiVersion: v1
kind: Service
metadata:
  name: wordpress
  namespace: kube-example
spec:
  selector:
    app: wordpress
  type: NodePort
  ports:
  - name: web
    port: 80
    targetPort: wdport
```

因为只需要暴露 Wordpress 这个应用，所以只匹配了一个名为 `wdport` 的端口，现在我们来创建上面的几个资源对象

```
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

接下来就是等待拉取镜像，启动 Pod:

```
$ kubectl get pods -n kube-example
NAME                         READY   STATUS    RESTARTS   AGE
wordpress-77dcdb64c6-zdlb8   2/2     Running   0          12m
$ kubectl get svc -n kube-example
NAME        TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
wordpress   NodePort   10.106.237.157   &lt;none&gt;        80:30892/TCP   2m2s
```

# 测试

当 Pod 启动完成后，可以通过上面的 `http://&lt;任意节点IP&gt;:30892` 这个 NodePort 端口来访问应用了

安装界面

![20210403230947740.png](https://img-blog.csdnimg.cn/20210403230947740.png)

![20210403231016271.png](https://img-blog.csdnimg.cn/20210403231016271.png)

# 问题

（1）pod中没有先后顺序

（2）单节点问题，没有高可用

（3）Wordpress 是无状态服务器，如果增加节点，mysql也会增加，数据不独立

（4）数据没有持久化

等等一些列的问题。

此版本1，为最简单的问题，我们将在此版本上改进架构，不断的优化

 

 

 
