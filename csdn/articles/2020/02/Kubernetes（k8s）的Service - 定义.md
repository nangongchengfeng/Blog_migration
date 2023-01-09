+++
author = "南宫乘风"
title = "Kubernetes（k8s）的Service - 定义"
date = "2020-02-06 17:06:27"
tags=['Kubernetes', 'k8s', 'Service', '定义']
categories=[]
image = "post/4kdongman/13.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104198552](https://blog.csdn.net/heian_99/article/details/104198552)

# Service 的概念 

**Kubernetes  Service  定义了这样一种抽象：一个  Pod  的逻辑分组，一种可以访问它们的策略 —— 通常称为微 服务。 这一组  Pod  能够被  Service  访问到，通常是通过  Label Selector**<br>![20200206164845536.png](https://img-blog.csdnimg.cn/20200206164845536.png)

**Service能够提供负载均衡的能力，但是在使用上有以下限制：**

只提供 4 层负载均衡能力，而没有 7 层功能，但有时我们可能需要更多的匹配规则来转发请求，这点上 4 层 负载均衡是不支持的

## **Service 的类型 **

**Service 在 K8s 中有以下四种类型 **
- **ClusterIp：默认类型，自动分配一个仅 Cluster 内部可以访问的虚拟 IP**
![20200206170439502.png](https://img-blog.csdnimg.cn/20200206170439502.png)
- **NodePort：在 ClusterIP 基础上为 Service 在每台机器上绑定一个端口，这样就可以通过 : NodePort 来访问该服务**
![20200206170453370.png](https://img-blog.csdnimg.cn/20200206170453370.png)
- **LoadBalancer：在 NodePort 的基础上，借助 cloud provider 创建一个外部负载均衡器，并将请求转发到: NodePort**
![20200206170511278.png](https://img-blog.csdnimg.cn/20200206170511278.png)
- **ExternalName：把集群外部的服务引入到集群内部来，在集群内部直接使用。没有任何类型代理被创建，这只有 kubernetes 1.7 或更高版本的 kube-dns 才支持**
![2020020617055647.png](https://img-blog.csdnimg.cn/2020020617055647.png)

![20200206165100169.png](https://img-blog.csdnimg.cn/20200206165100169.png)
