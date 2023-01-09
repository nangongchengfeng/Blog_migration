+++
author = "南宫乘风"
title = "Kubernetes（k8s）Pod的生命周期"
date = "2020-02-03 22:08:53"
tags=['Kubernetes\xa0', 'Pod', '生命周期', 'init']
categories=['Kubernetes']
image = "post/4kdongman/72.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104162175](https://blog.csdn.net/heian_99/article/details/104162175)

# Kubernetes pod 初始化

![20200203210606608.png](https://img-blog.csdnimg.cn/20200203210606608.png)init C ：初始换容器

Pod 能够具有多个容器，应用运行在容器里面，但是它也可能有一个或多个先于应用容器启动的  Init容器

Init 容器与普通的容器非常像，除了如下两点：  
- Ø Init 容器总是运行到成功完成为止  - Ø 每个 Init 容器都必须在下一个 Init 容器启动之前成功完成  
**如果 Pod 的 Init 容器失败，Kubernetes 会不断地重启该 Pod，直到  Init 容器成功为止。然而**

### **因为 Init 容器具有与应用程序容器分离的单独镜像，所以它们的启动相关代码具有如下优势：**

![20200203212713217.png](https://img-blog.csdnimg.cn/20200203212713217.png)

 

# Init 容器  

**init 模板 **

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo The app is running! &amp;&amp; sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; 
done;']
  - name: init-mydb
    image: busybox
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']

```

![20200203215837563.png](https://img-blog.csdnimg.cn/20200203215837563.png)

等待init的初始化。

```
kind: Service
apiVersion: v1
metadata:
  name: myservice
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376

```

![20200203220232560.png](https://img-blog.csdnimg.cn/20200203220232560.png)

```
kind: Service
apiVersion: v1
metadata:
  name: mydb
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9377
```

![20200203220452435.png](https://img-blog.csdnimg.cn/20200203220452435.png)

**两个initC已经初始换完成**

![20200203220626352.png](https://img-blog.csdnimg.cn/20200203220626352.png)

![20200203220642103.png](https://img-blog.csdnimg.cn/20200203220642103.png)

 
