+++
author = "南宫乘风"
title = "CentOS7的Yum安装Kubernetes（k8s）完整版详细教程"
date = "2020-01-11 12:04:17"
tags=['Kubberbetes', 'Yum', 'Centos7', '容器']
categories=['Kubernetes']
image = "post/4kdongman/06.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103933928](https://blog.csdn.net/heian_99/article/details/103933928)

[kubeadm部署Kubernetes（k8s）完整版详细教程    ](https://blog.csdn.net/heian_99/article/details/103888459)

容易配置，但出问题却很难发现。

[二进制包安装Kubernetes集群环境完整版](https://blog.csdn.net/heian_99/article/details/103918683)

配置麻烦，但不容易出现问题，也容易排查。

 

对于上面安装Kubernetes方法，有兴趣的可以参考一下。

下面这种方法，容易配置，也不容易出现问题。

 

# **环境配置**

准备3台服务器（我用的是CentOS7系统）：

Master：192.168.116.129

Node1：192.168.116.130

Node2：192.168.116.131

 

### k8s的全生命周期管理：

  在k8s进行管理应用的时候，基本步骤是：创建集群，部署应用，发布应用，扩展应用，更新应用

### k8s的主要组件，以及它们主要是用来干什么的：

**etcd：**一款开源软件。提供可靠的分布式数据存储服务，用于持久化存储K8s集群的配置和状态

**apiservice：**用户程序（如kubectl）、K8s其它组件之间通信的接口。K8s其它组件之间不直接通信，而是通过API server通信的。这一点在上图的连接中可以体现，例如，只有API server连接了etcd，即其它组件更新K8s集群的状态时，只能通过API server读写etcd中的数据。

**Scheduler：**排程组件，为用户应用的每一可部署组件分配工作结点。

**controller-manager：**执行集群级别的功能，如复制组件、追踪工作结点状态、处理结点失败等。Controller Manager组件是由多个控制器组成的，其中很多控制器是按K8s的资源类型划分的，如Replication Manager（管理ReplicationController 资源），ReplicaSet Controller，PersistentVolume controller。

**kube-proxy：**在应用组件间负载均衡网络流量。

**kubelet：**管理工作结点上的容器。

**Contriner runtime Docker**， rkt等实际运行容器的组件

上面都是些k8s集群所要用到的组件

## **master主机上必须要有的组件：**

**etcd **：提供分布式数据存储的数据库吧，用于持久化存储k8s集群的配置和状态

**kube-apiserver**：api service提供了http rest接口，是整个集群的入口，K8s其它组件之间不直接通信，而是通过API server通信的。（只有API server连接了etcd，即其它组件更新K8s集群的状态时，只能通过API server读写etcd中的数据）

**kube-scheduler**：scheduler负责资源的调度

**kube-controller-manager**：整个集群的管理控制中心，此组件里面是由多个控制器组成的，如：Replication Manager（管理ReplicationController 资源），ReplicaSet Controller，PersistentVolume controller。主要作用用来复制组件、追踪工作结点状态、处理失败结点

## **node节点机上必须要有的组件：**

**flannel：**好像是用来支持网络通信的吧

**kube-proxy：**用来负载均衡网络流量

**kubelet：**用来管理node节点机上的容器

**docker：**运行项目镜像容器的组件

### k8s的整个集群运行原理：

master主机上的**kube-controller-manager**是整个集群的控制管理中心，**kube-controler-manager**中的node controller模块 通过**apiservice**提供的监听接口，实时监控node机的状态信息。

 当某个node机器宕机，**controller-manager**就会及时排除故障并自动修复。

node节点机上的kubelet进程每隔一段时间周期就会调用一次apiservice接口报告自身状态，**apiservice**接口接受到这些信息后将节点状态更新到**ectd**中。kubelet也通过**apiservice**的监听接口监听**pod**信息，如果监控到新的pod副本被调度绑定到本节点，则执行pod对应的容器的创建和启动，如果监听到pod对象被删除，则删除本节点对应的pod容器。

# Kubernetes安装步骤：

## 1、所有机器上执行以下命令，准备安装环境：(注意是所有机器，主机master，从机node都要安装)

安装epel-release源

```
yum -y install epel-release
```

所有机器关闭防火墙

```
systemctl stop firewalld

systemctl disable firewalld

setenforce 0

#查看防火墙状态
firewall-cmd --state
```

关闭swap

```
swapoff -a
```

## 2、现在开始master主机上安装kubernetes Master

```
yum -y install etcd kubernetes-master

```

## **etcd.conf**

编辑：**vi /etc/etcd/etcd.conf**文件，修改结果如下：

![20200111105036265.png](https://img-blog.csdnimg.cn/20200111105036265.png)

## apiserver

配置：**vi /etc/kubernetes/apiserver**文件，配置结果如下：

![20200111105318312.png](https://img-blog.csdnimg.cn/20200111105318312.png)

启动etcd、kube-apiserver、kube-controller-manager、kube-scheduler等服务，并设置开机启动。

```
for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler; do systemctl restart $SERVICES;systemctl enable $SERVICES;systemctl status $SERVICES ; done
```

在etcd中定义flannel网络

```
etcdctl mk /atomic.io/network/config '{"Network":"172.17.0.0/16"}'
```

![20200111105441620.png](https://img-blog.csdnimg.cn/20200111105441620.png)

### 以上master主机上的配置安装什么的都弄完

 

## 3、在node机上安装kubernetes Node和flannel组件应用

```
yum -y install flannel kubernetes-node
```

## flanneld

为flannel网络指定etcd服务，修改**/etc/sysconfig/flanneld**文件，配置结果如下图：

![20200111110129299.png](https://img-blog.csdnimg.cn/20200111110129299.png)

 

## **config**

修改：**vi /etc/kubernetes/config**文件，配置结果如下图：

![20200111110248825.png](https://img-blog.csdnimg.cn/20200111110248825.png)

## **kubelet**

修改node机的kubelet配置文件**/etc/kubernetes/kubelet**

![20200111110526409.png](https://img-blog.csdnimg.cn/20200111110526409.png)

node节点机上启动kube-proxy,kubelet,docker,flanneld等服务，并设置开机启动。

```
for SERVICES in kube-proxy kubelet docker flanneld;do systemctl restart $SERVICES;systemctl enable $SERVICES;systemctl status $SERVICES; done
```

## 4、在master主机上执行如下命令，查看运行的node节点机器：

```
kubectl get nodes

```

![20200111111037563.png](https://img-blog.csdnimg.cn/20200111111037563.png)

## k8s的安装算是完成

## 5、部署 Dashboard

也可以使用我给配置文件 https://www.lanzous.com/i8jjpij

默认镜像国内无法访问，修改镜像地址为： lizhenliang/kubernetes-dashboard-amd64:v1.10.1

默认Dashboard只能集群内部访问，修改Service为NodePort类型，暴露到外部：

![20200111111208983.png](https://img-blog.csdnimg.cn/20200111111208983.png)

**先Docker拉去镜像**

```
docker pull  lizhenliang/kubernetes-dashboard-amd64:v1.10.1
```

**执行kubernetes-dashboard.yaml 文件**

```
 kubectl apply -f kubernetes-dashboard.yaml
```

安装成功

![20200111111230668.png](https://img-blog.csdnimg.cn/20200111111230668.png)

查看暴露的端口

```
kubectl get pods,svc -n kube-system
```

![20200111111248761.png](https://img-blog.csdnimg.cn/20200111111248761.png)

## 6. 访问 Dashboard的web界面

**访问地址：https://NodeIP:30001 【必须是https】**

![20200111111308708.png](https://img-blog.csdnimg.cn/20200111111308708.png)

**创建service account并绑定默认cluster-admin管理员集群角色：【依次执行】**

```
kubectl create serviceaccount dashboard-admin -n kube-system
```

```
 kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin
```

```
 kubectl describe secrets -n kube-system $(kubectl -n kube-system get secret | awk '/dashboard-admin/{print $1}')
```

![20200111111415701.png](https://img-blog.csdnimg.cn/20200111111415701.png)<br>**已经部署完成。**

![20200111111424766.png](https://img-blog.csdnimg.cn/20200111111424766.png)

 
