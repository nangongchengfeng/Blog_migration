+++
author = "南宫乘风"
title = "Kubernetes（k8s）集群功能演示"
date = "2020-02-03 15:56:42"
tags=['k8s', 'Kubernetes', '命令', '功能']
categories=[]
image = "post/4kdongman/54.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104154643](https://blog.csdn.net/heian_99/article/details/104154643)

通过一段学习，我们的Kubernetes已经部署起来，现在就开始功能的演示。

如果又不会部署的小伙伴，可以看我以前的博客，都有详细的教程。

**目录**

[查看node的节点情况](#%E6%9F%A5%E7%9C%8Bnode%E7%9A%84%E8%8A%82%E7%82%B9%E6%83%85%E5%86%B5)

[查看pod的运行情况](#%E6%9F%A5%E7%9C%8Bpod%E7%9A%84%E8%BF%90%E8%A1%8C%E6%83%85%E5%86%B5)

[查看deployment情况](#%E6%9F%A5%E7%9C%8Bdeployment%E6%83%85%E5%86%B5)

[查看pod的运行详细信息](#%E6%9F%A5%E7%9C%8Bpod%E7%9A%84%E8%BF%90%E8%A1%8C%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)

[删除deployment](#%E5%88%A0%E9%99%A4deployment)

[删除一个pod应用](#%E5%88%A0%E9%99%A4%E4%B8%80%E4%B8%AApod%E5%BA%94%E7%94%A8)

[查看kubectl创建提示](#%E6%9F%A5%E7%9C%8Bkubectl%E5%88%9B%E5%BB%BA%E6%8F%90%E7%A4%BA)

[kubectl创建nginx应用](#kubectl%E5%88%9B%E5%BB%BAnginx%E5%BA%94%E7%94%A8)

[副本集扩容](#%E5%89%AF%E6%9C%AC%E9%9B%86%E6%89%A9%E5%AE%B9)

[应用pod的端口修改【把80端口改成了 30003】](#%E5%BA%94%E7%94%A8pod%E7%9A%84%E7%AB%AF%E5%8F%A3%E4%BF%AE%E6%94%B9%E3%80%90%E6%8A%8A80%E7%AB%AF%E5%8F%A3%E6%94%B9%E6%88%90%E4%BA%86%2030003%E3%80%91)

[修改nginx-deployment的ip类型【可以暴露端口，实现内部网访问】](#%E4%BF%AE%E6%94%B9nginx-deployment%E7%9A%84ip%E7%B1%BB%E5%9E%8B%E3%80%90%E5%8F%AF%E4%BB%A5%E6%9A%B4%E9%9C%B2%E7%AB%AF%E5%8F%A3%EF%BC%8C%E5%AE%9E%E7%8E%B0%E5%86%85%E9%83%A8%E7%BD%91%E8%AE%BF%E9%97%AE%E3%80%91)

[测速访问](#%E6%B5%8B%E9%80%9F%E8%AE%BF%E9%97%AE)

# **查看node的节点情况**

```
 kubectl get node

```

![20200203121135494.png](https://img-blog.csdnimg.cn/20200203121135494.png)

# **查看pod的运行情况**

```
kubectl get pod

```

![20200203121221880.png](https://img-blog.csdnimg.cn/20200203121221880.png)

# **查看deployment情况**

```
 kubectl get deployment
```

![20200203121410426.png](https://img-blog.csdnimg.cn/20200203121410426.png)

# **查看pod的运行详细信息**

```
 kubectl get pod -o wide
```

![20200203121513658.png](https://img-blog.csdnimg.cn/20200203121513658.png)

# **删除deployment**

```
kubectl delete deployment nginx

```

![20200203152245740.png](https://img-blog.csdnimg.cn/20200203152245740.png)

# **删除一个pod应用**

```
 kubectl delete pod nginx-deployment-5d9dfb999c-t6xdq

```

![20200203152732631.png](https://img-blog.csdnimg.cn/20200203152732631.png)

# **查看kubectl创建提示**

```
kubectl run --help

```

![20200203150826533.png](https://img-blog.csdnimg.cn/20200203150826533.png)

# **kubectl创建nginx应用**

```
kubectl run nginx-deployment --image=wangyanglinux/myapp:v1  --port=80 --replicas=1

```

![20200203151900438.png](https://img-blog.csdnimg.cn/20200203151900438.png)

![20200203152405396.png](https://img-blog.csdnimg.cn/20200203152405396.png)

![20200203152537550.png](https://img-blog.csdnimg.cn/20200203152537550.png)

```
[root@master ~]# kubectl get pod
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-5d9dfb999c-t6xdq   1/1     Running   0          5m43s
[root@master ~]# kubectl get pod -o wide
NAME                                READY   STATUS    RESTARTS   AGE     IP           NODE    NOMINATED NODE   READINESS GATES
nginx-deployment-5d9dfb999c-t6xdq   1/1     Running   0          5m51s   10.244.2.7   node1   &lt;none&gt;           &lt;none&gt;
[root@master ~]# curl 10.244.2.7
Hello MyApp | Version: v1 | &lt;a href="hostname.html"&gt;Pod Name&lt;/a&gt;
[root@master ~]# curl 10.244.2.7/hostname.html
nginx-deployment-5d9dfb999c-t6xdq

```

# **副本集扩容**

```
kubectl scale --replicas=3 deployment/nginx-deployment
```

![2020020315301424.png](https://img-blog.csdnimg.cn/2020020315301424.png)

![20200203153117393.png](https://img-blog.csdnimg.cn/20200203153117393.png)

# **应用pod的端口修改【把80端口改成了 30003】**

```
kubectl expose deployment nginx-deployment --port=30003 --target-port=80
```

![20200203154031868.png](https://img-blog.csdnimg.cn/20200203154031868.png)

# **修改nginx-deployment的ip类型【可以暴露端口，实现内部网访问】**

```
 kubectl edit svc nginx-deployment

```

![20200203155219994.png](https://img-blog.csdnimg.cn/20200203155219994.png)

![20200203155328240.png](https://img-blog.csdnimg.cn/20200203155328240.png)

# 测速访问

![2020020315535649.png](https://img-blog.csdnimg.cn/2020020315535649.png)

![20200203155406976.png](https://img-blog.csdnimg.cn/20200203155406976.png)
