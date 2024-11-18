---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-02-04 13:08:30
description: 的探针探针是由对容器执行的定期诊断。要执行诊断，调用由容器实现的。有三种类型的处理程序：：在容器内执行指定命令。如果命令退出时返回码为则认为诊断成功。：对指定端口上的容器的地址进行检查。如果端口打开，。。。。。。。
image: http://image.ownit.top/4kdongman/04.jpg
tags:
- Kubernetes
- k8s
- readness
- liveness
- 探针
title: Kubernetes（k8s）pod的探针liveness、readiness详细教程
---

<!--more-->

# Kubernetes pod的探针

**探针是由  kubelet 对容器执行的定期诊断。要执行诊断，kubelet 调用由容器实现的  Handler。有三种类型的处理程序：**

- Ø ExecAction：在容器内执行指定命令。如果命令退出时返回码为 0 则认为诊断成功。
- Ø TCPSocketAction：对指定端口上的容器的 IP 地址进行 TCP 检查。如果端口打开，则诊断被认为是成功的。
- Ø HTTPGetAction：对指定的端口和路径上的容器的 IP 地址执行 HTTP Get 请求。如果响应的状态码大于等于200 且小于 400，则诊断被认为是成功的  
 

**每次探测都将获得以下三种结果之一： **

-  成功：容器通过了诊断。
- 失败：容器未通过诊断。
- 未知：诊断失败，因此不会采取任何行动

1.  **livenessProbe：指示容器是否正在运行。如果存活探测失败，则 kubelet 会杀死容器，并且容器将受到其 重启策略 的影响。如果容器不提供存活探针，则默认状态为 Success**
2.  **readinessProbe：指示容器是否准备好服务请求。如果就绪探测失败，端点控制器将从与 Pod 匹配的所有 Service 的端点中删除该 Pod 的 IP 地址。初始延迟之前的就绪状态默认为 Failure。如果容器不提供就绪探针，则默认状态为 Success**  
 

## 检测探针 - 就绪检测 

**readinessProbe-httpget **

```bash
apiVersion: v1
kind: Pod
metadata:
  name: readiness-httpget-pod
  namespace: default
spec:
  containers:
  - name: readiness-httpget-container
    image: wangyanglinux/myapp:v1
    imagePullPolicy: IfNotPresent
    readinessProbe:
      httpGet:
        port: 80
        path: /index1.html
      initialDelaySeconds: 1
      periodSeconds: 3
```

**因为这nginx下的80那里，没有index1.html这个界面**

![](http://image.ownit.top/csdn/20200204121952595.png)

**查看Pod的详细描述**

```
 kubectl describe pod readiness-httpget-pod
```

![](http://image.ownit.top/csdn/20200204122317758.png)

**查看Pod的日志【一直不断的探测】**

```bash
kubectl log  readiness-httpget-pod
```

![](http://image.ownit.top/csdn/20200204122442176.png)

# 解决办法

**进入这个容器**

```
kubectl exec  readiness-httpget-pod -it -- /bin/sh
```

```bash
[root@master k8s]# kubectl exec  readiness-httpget-pod -it -- /bin/sh
/ # cd /usr/share/nginx/html/
/usr/share/nginx/html # ls
50x.html    index.html
/usr/share/nginx/html # echo "123" >> index1.html
/usr/share/nginx/html # exit
```

![](http://image.ownit.top/csdn/20200204122935264.png)

 

## 检测探针 - 存活检测 

**livenessProbe-exec **

```bash
apiVersion: v1
kind: Pod
metadata:
  name: liveness-exec-pod
  namespace: default
spec:
  containers:
  - name: liveness-exec-container
    image: busybox
    imagePullPolicy: IfNotPresent
    command: ["/bin/sh","-c","touch /tmp/live ; sleep 60; rm -rf /tmp/live; sleep
3600"]
    livenessProbe:
      exec:
        command: ["test","-e","/tmp/live"]
      initialDelaySeconds: 1
      periodSeconds: 3
```

**检测/tmp/live，每隔60秒就会被删除，liveness检测，如果被删除，就会返回失败，重启pod。陷入无限循环**。

![](http://image.ownit.top/csdn/20200204124123664.png)

**livenessProbe-httpget **

```bash
apiVersion: v1
kind: Pod
metadata:
  name: liveness-httpget-pod
  namespace: default
spec:
  containers:
  - name: liveness-httpget-container
    image: wangyanglinux/myapp:v1
    imagePullPolicy: IfNotPresent
    ports:
    - name: http
      containerPort: 80
    livenessProbe:
      httpGet:
        port: http
        path: /index.html
      initialDelaySeconds: 1
      periodSeconds: 3
      timeoutSeconds: 10
```

![](http://image.ownit.top/csdn/20200204125038560.png)

**现在进入容器，删除index.html文件**

```bash
 kubectl exec liveness-httpget-pod -it -- /bin/sh
```

![](http://image.ownit.top/csdn/20200204125449729.png)

![](http://image.ownit.top/csdn/20200204125620349.png)

**livenessProbe-tcp **

```bash
apiVersion: v1
kind: Pod
metadata:
  name: probe-tcp
spec:
  containers:
  - name: nginx
    image: wangyanglinux/myapp:v1
    livenessProbe:
      initialDelaySeconds: 5
      timeoutSeconds: 1
      tcpSocket:
        port: 8080
      periodSeconds: 3
```

**检测8080端口，但是那个端口没有，就会一直检测，重启。**

![](http://image.ownit.top/csdn/20200204130208953.png)

**启动、退出动作** 

```
apiVersion: v1
kind: Pod
metadata:
  name: lifecycle-demo
spec:
  containers:
  - name: lifecycle-demo-container
    image: wangyanglinux/myapp:v1
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo Hello from the postStart handler > 
/usr/share/message"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "echo Hello from the poststop handler > 
/usr/share/message"]

```

![](http://image.ownit.top/csdn/20200204132105564.png)