---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-01-10 19:37:49
description: 概述是什么是在年开源的一个容器集群管理系统，简称。用于容器化应用程序的部署，扩展和管理。提供了容器编排，资源调度，弹性伸缩，部署管理，服务发现等一系列功能。目标是让部署容器化应用简单高效。官方网站：特。。。。。。。
image: http://image.ownit.top/4kdongman/50.jpg
tags:
- Kubernetes
- 集群
- 二进制
title: 二进制包安装Kubernetes集群环境完整版
---

<!--more-->

# Kubernetes 概述

## 1\. Kubernetes是什么

-  Kubernetes是Google在2014年开源的一个容器集群管理系统，Kubernetes简称K8S。
- K8S用于容器化应用程序的部署，扩展和管理。
-  K8S提供了容器编排，资源调度，弹性伸缩，部署管理，服务发现等一系列功能。
-  Kubernetes目标是让部署容器化应用简单高效。

官方网站：http://www.kubernetes.io

## 2\. Kubernetes特性

**自我修复**  
在节点故障时重新启动失败的容器，替换和重新部署，保证预期的副本数量；杀死健康检查失败的容器，并且在未准备好之前不会处理客户端请求，确保线上服务不中断。  
** 弹性伸缩**  
使用命令、UI或者基于CPU使用情况自动快速扩容和缩容应用程序实例，保证应用业务高峰并发时的高可用性；业务低峰时回收资源，以最小成本运行服务。  
** 自动部署和回滚**  
K8S采用滚动更新策略更新应用，一次更新一个Pod，而不是同时删除所有Pod，如果更新过程中出现问题，将回滚更改，确保升级不受影响业务。  
**服务发现和负载均衡**  
K8S为多个容器提供一个统一访问入口（内部IP地址和一个DNS名称），并且负载均衡关联的所有容器，使得用户无需考虑容器IP问题。  
** 机密和配置管理**  
管理机密数据和应用程序配置，而不需要把敏感数据暴露在镜像里，提高敏感数据安全性。并可以将一些常用的配置存储在K8S中，方便应用程序使用。  
** 存储编排**  
挂载外部存储系统，无论是来自本地存储，公有云（如AWS），还是网络存储（如NFS、GlusterFS、Ceph）都作为集群资源的一部分使用，极大提高存储使用灵活性。  
**批处理**  
提供一次性任务，定时任务；满足批量数据处理和分析的场景。

## 3\. Kubernetes集群架构与组件

![](http://image.ownit.top/csdn/2020011009171635.png)

 

### Master组件

- kube-apiserver Kubernetes API  集群的统一入口，各组件协调者，以 RESTful API提供接口服务，所有对象资源的增删改查和监听 操作都交给APIServer处理后再提交给Etcd存储。
- kube-controller-manager 处理集群中常规后台任务，一个资源对应一个控制器，而 ControllerManager就是负责管理这些控制器的。
- kube-scheduler 根据调度算法为新创建的Pod选择一个Node节点，可以任意 部署,可以部署在同一个节点上,也可以部署在不同的节点上。
- etcd 分布式键值存储系统。用于保存集群状态数据，比如Pod、 Service等对象信息。

### Node组件

- kubelet kubelet 是Master在Node节点上的Agent，管理本机运行容器 的生命周期，比如创建容器、Pod挂载数据卷、下载secret、获 取容器和节点状态等工作。
- kubelet   将每个Pod转换成一组容器。
- kube-proxy 在Node节点上实现Pod网络代理，维护网络规则和四层负载均 衡工作。 docker或rocket 容器引擎，运行容器

## 4\. Kubernetes核心概念

###  **Pod**

- 最小部署单元
-  一组容器的集合
- 一个Pod中的容器共享网络命名空间
-  Pod是短暂的

### Controllers

- ReplicaSet ： 确保预期的Pod副本数量 
- Deployment ： 无状态应用部署 
- StatefulSet ： 有状态应用部署
- DaemonSet ： 确保所有Node运行同一个Pod 
- Job ： 一次性任务 
- Cronjob ： 定时任务
- 更高级层次对象，部署和管理Pod

###  Service

- 防止Pod失联
-  定义一组Pod的访问策略

### Label

- 标签，附加到某个资源上，用于关联对象、查询和筛选

### Namespace 

- 命名空间，将对象逻辑上隔离

# 搭建一个 Kubernetes 集群

## 1\. 官方提供的三种部署方式

- **minikube**

Minikube是一个工具，可以在本地快速运行一个单点的Kubernetes，尝试Kubernetes或日常开发的用户使用。不能用于生产环境。

官方地址：[https://kubernetes.io/docs/setup/minikube/](https://kubernetes.io/docs/setup/minikube/)

- **kubeadm**

Kubeadm也是一个工具，提供kubeadm init和kubeadm join，用于快速部署Kubernetes集群。

官方地址：[https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm/](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm/)

- **二进制包**

从官方下载发行版的二进制包，手动部署每个组件，组成Kubernetes集群。

**小结：**  
生产环境中部署Kubernetes集群，只有Kubeadm和二进制包可选，Kubeadm降低部署门槛，但屏蔽了很多细节，遇到问题很难排查。我们这里使用二进制包部署Kubernetes集群，我也是推荐大家使用这种方式，虽然手动部署麻烦点，但学习很多工作原理，更有利于后期维护。

## 2\. Kubernetes集群环境规划

**软件环境**

| 
**软件**

 | 

**版本**

 |
| --- | --- |
| 

操作系统

 | 

CentOS7.5\_x64

 |
| 

Docker

 | 

18-ce

 |
| 

Kubernetes

 | 

1.12

 |

**服务器角色**

| 
**角色**

 | 

**IP**

 | 

**组件**

 |
| --- | --- | --- |
| 

k8s-master

 | 

192.168.116.129

 | 

kube-apiserver，kube-controller-manager，kube-scheduler，etcd

 |
| 

k8s-node1

 | 

192.168.116.130

 | 

kubelet，kube-proxy，docker，flannel，etcd

 |
| 

k8s-node2

 | 

192.168.116.131

 | 

kubelet，kube-proxy，docker，flannel，etcd

 |

**需要的软件和脚本，失效可联系我**

**链接: https://pan.baidu.com/s/1Vr8jOFgo4b8tQM9AUtXC\_A 提取码: yhhn **

**架构图**

## ![](http://image.ownit.top/csdn/20200110092520378.png)

## 3\. HTTPS证书介绍

**1、关闭selinux**

```
 sed -i 's/enforcing/disabled/' /etc/selinux/config 
 setenforce 0
```

**2、关闭防火墙**

```
systemctl stop firewalld
systemctl disable firewalld
```

**3、关闭swap**

```
swapoff -a
```

**4、修改主机名**

```
hostnamectl set-hostname 名字
```

**5、同步时间**

```
 yum install -y ntpdate && ntpdate time.windows.com
```

**以上步骤可以参考下方链接**

**[kubeadm部署Kubernetes（k8s）完整版详细教程](https://blog.csdn.net/heian_99/article/details/103888459)**

### **自签SSL证书**

![](http://image.ownit.top/csdn/20200110093817699.png)

准备使用etcd-cert生成证书

![](http://image.ownit.top/csdn/20200110095246702.png)

**上传cfssl.sh，运行脚本**

![](http://image.ownit.top/csdn/2020011009594425.png)

**生成下面两个文件，记住是tab补全查看**

![](http://image.ownit.top/csdn/20200110100050808.png)

**执行下面命令，生成两个文件**

```bash
cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "www": {
         "expiry": "87600h",
         "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ]
      }
    }
  }
}
EOF

cat > ca-csr.json <<EOF
{
    "CN": "etcd CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Beijing",
            "ST": "Beijing"
        }
    ]
}
EOF
```

![](http://image.ownit.top/csdn/20200110100356807.png)

执行

```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
```

![](http://image.ownit.top/csdn/2020011010052256.png)

```bash
cat etcd-cert.sh 
```

![](http://image.ownit.top/csdn/20200110100823401.png)

```bash
cat > server-csr.json <<EOF
{
    "CN": "etcd",
    "hosts": [
    "192.168.116.129",
    "192.168.116.130",
    "192.168.116.131"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "BeiJing",
            "ST": "BeiJing"
        }
    ]
}
EOF
```

![](http://image.ownit.top/csdn/20200110101040603.png)

**颁发证书**

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=www server-csr.json | cfssljson -bare server
```

## ![](http://image.ownit.top/csdn/20200110101348951.png)

## 4\. Etcd数据库集群部署

## 上传etcd安装包

【etcd-v3.3.10-linux-amd64.tar.gz】

![](http://image.ownit.top/csdn/20200110101621852.png)

解压

```bash
 tar zxvf etcd-v3.3.10-linux-amd64.tar.gz 
```

## ![](http://image.ownit.top/csdn/20200110101844730.png)

为了方便安装，创建下面目录安装。

```bash
[root@master etcd-v3.3.10-linux-amd64]# mkdir -p  /opt/etcd/{cfg,bin,ssl}
[root@master etcd-v3.3.10-linux-amd64]# ls /opt/etcd/
bin  cfg  ssl
[root@master etcd-v3.3.10-linux-amd64]# mv etcd etcdctl /opt/etcd/bin/
[root@master etcd-v3.3.10-linux-amd64]# ls /opt/etcd/bin/
etcd  etcdctl
```

## ![](http://image.ownit.top/csdn/20200110102138508.png)

## 使用脚本部署etcd

![](http://image.ownit.top/csdn/20200110102351198.png)

```
chmod +x etcd.sh 
```

## 运行脚本

```bash
./etcd.sh etcd01 192.168.116.129 etcd02=https://192.168.116.130:2380,etcd03=https://192.168.116.131:2380
```

## ![](http://image.ownit.top/csdn/20200110105006392.png)

可以查看etcd的运行服务文件

```
cat /usr/lib/systemd/system/etcd.service 
```

![](http://image.ownit.top/csdn/20200110105358535.png)

拷贝证书

```
 cp /root/k8s/etcd-cert/{ca,server-key,server}.pem /opt/etcd/ssl/
```

![](http://image.ownit.top/csdn/20200110105603848.png)

## 启动etcd

```
systemctl start etcd
```

 

**已经部署一个成功，但是还有两个机器没有部署etcd。需要把/opt/的etcd目录移到其余节点配置**

**还有/usr/lib/systemd/system/etcd.service这个配置文件**

 

拷贝过去还需要修改配置文件才能启动。

```
vi /opt/etcd/cfg/etcd
```

这几个需要修改本机对于的ip

![](http://image.ownit.top/csdn/2020011011111949.png)

切忌要给下方的文件执行权限，不然会报错

```
/opt/etcd/bin
```

![](http://image.ownit.top/csdn/20200110112657217.png)

启动

```
systemctl daemon-reload
```

```
systemctl start etcd
```

已经完成启动

![](http://image.ownit.top/csdn/20200110112746981.png)

在node2也按照上方部署就行。

查看先前日志【没有报任何错误，已经成功搭建集群】

```bash
tail /var/log/messages -f
```

![](http://image.ownit.top/csdn/20200110112938482.png)

## 测试

```
/opt/etcd/bin/etcdctl --ca-file=/opt/etcd/ssl/ca.pem --cert-file=/opt/etcd/ssl/server.pem --key-file=/opt/etcd/ssl/server-key.pem --endpoints="https://192.168.116.129:2379,https://192.168.116.130:2379,https://192.168.116.131:2379"  cluster-health
```

## ![](http://image.ownit.top/csdn/20200110115352310.png)

## 5\. Node安装Docker

![](http://image.ownit.top/csdn/20200110133914952.png)

**安装依赖软件**

```
yum install -y yum-utils device-mapper-persistent-data lvm2
```

```
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

**安装docker-ce**

```
yum install docker-ce -y
```

**配置docker加速器**

```
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://bc437cce.m.daocloud.io
```

**启动docker**

```
 systemctl start docker
```

**开机自启**

```
systemctl enable docker
```

 

## 6\. Flannel容器集群网络部署

**Kubernetes网络模型设计基本要求：**

- 一个Pod一个IP
- 每个Pod独立IP，Pod内所有容器共享网络（同一个IP）
- 所有容器都可以与所有其他容器通信
- 所有节点都可以与所有有容器通信

**工作原理：**

![](http://image.ownit.top/csdn/20200110135434520.png)

**添加网段**

```
/opt/etcd/bin/etcdctl --ca-file=/opt/etcd/ssl/ca.pem --cert-file=/opt/etcd/ssl/server.pem --key-file=/opt/etcd/ssl/server-key.pem --endpoints="https://192.168.116.129:2379,https://192.168.116.130:2379,https://192.168.116.131:2379" set /coreos.com/network/config  '{ "Network": "172.17.0.0/16", "Backend": {"Type": "vxlan"}}'
```

![](http://image.ownit.top/csdn/20200110141155825.png)

```
/opt/etcd/bin/etcdctl --ca-file=/opt/etcd/ssl/ca.pem --cert-file=/opt/etcd/ssl/server.pem --key-file=/opt/etcd/ssl/server-key.pem --endpoints="https://192.168.116.129:2379,https://192.168.116.130:2379,https://192.168.116.131:2379" get /coreos.com/network/config 
```

![](http://image.ownit.top/csdn/20200110141310162.png)

**上传Flannel【在node上部署flannel】**

![](http://image.ownit.top/csdn/20200110142117253.png)

**方便管理flannel，创建下面文件**

```bash
mkdir -p /opt/kubernetes/{bin,cfg,ssl}
```

**使用flannel连接etcd形式执行脚本**

```
 ./flannel.sh https://192.168.116.129:2379,https://192.168.116.130:2379,https://192.168.116.131:2379
```

![](http://image.ownit.top/csdn/20200110142719774.png)

解压flannel-v0.10.0-linux-amd64.tar.gz

```
tar zxvf flannel-v0.10.0-linux-amd64.tar.gz
```

![](http://image.ownit.top/csdn/20200110143348452.png)

```
mv flanneld mk-docker-opts.sh /opt/kubernetes/bin/
```

**启动flannel，成功**

```
systemctl start flanneld
```

![](http://image.ownit.top/csdn/20200110143438113.png)

重启docker

```
systemctl restart docker
```

![](http://image.ownit.top/csdn/20200110143652124.png)

**安装openssh-clients，把flannel的配置文件复制到Node2上。**

```
 yum install -y openssh-clients
```

传输到Node2上

```
 scp -r /opt/kubernetes/ root@192.168.116.131:/opt/
```

```bash
scp /usr/lib/systemd/system/{flanneld,docker}.service root@192.168.116.131:/usr/lib/systemd/system/
```

![](http://image.ownit.top/csdn/20200110145102216.png)

**在Node2上启动flanneld**

```
 systemctl start flanneld
 systemctl start docker
```

## ![](http://image.ownit.top/csdn/2020011014535221.png)

## 7\. 部署Master组件

**1\. kube-apiserver**

**2\. kube-controller-manager**

**3\. kube-scheduler**

  
**配置文件 \-> systemd管理组件 \-> 启动**

**上传Master**

```
unzip master.zip 
```

![](http://image.ownit.top/csdn/20200110161100879.png)

**上传kubernetes-server-linux-amd64.tar.gz**

```
 tar zxvf kubernetes-server-linux-amd64.tar.gz
```

![](http://image.ownit.top/csdn/20200110173523120.png)

创建安装目录，方便使用

```
 mkdir -p /opt/kubernetes/{bin,cfg,ssl}
```

来到/root/k8s/soft/kubernetes/server/bin目录下拷贝文件

```
 cp kube-apiserver kube-controller-manager kube-scheduler /opt/kubernetes/bin/
```

![](http://image.ownit.top/csdn/20200110173804779.png)

**执行apiserver.sh 【脚本 masterip etcd的ip】**

```bash
./apiserver.sh 192.168.116.129 https://192.168.116.129:2379,https://192.168.116.130:2379,https://192.168.116.131:2379
```

查看生成的配文件

```
cat /opt/kubernetes/cfg/kube-apiserver 
```

![](http://image.ownit.top/csdn/20200110174803331.png)

**上传k8s-cert.sh，生成证书**

![](http://image.ownit.top/csdn/20200110180201635.png)

```
 bash k8s-cert.sh
```

![](http://image.ownit.top/csdn/20200110180239481.png)

复制证书到/opt/kubernetes/ssl/里

```
cp ca.pem ca-key.pem server.pem server-key.pem /opt/kubernetes/ssl/
```

![](http://image.ownit.top/csdn/20200110180449436.png)

**上传token配置文件，生成token。**

![](http://image.ownit.top/csdn/20200110180753569.png)

```
BOOTSTRAP_TOKEN=0fb61c46f8991b718eb38d27b605b008

cat > token.csv <<EOF
${BOOTSTRAP_TOKEN},kubelet-bootstrap,10001,"system:kubelet-bootstrap"
EOF
```

## ![](http://image.ownit.top/csdn/20200110180856922.png)

## 生成token.csv

![](http://image.ownit.top/csdn/20200110180950628.png)

## 文件移动

```
mv token.csv /opt/kubernetes/cfg/
```

## ![](http://image.ownit.top/csdn/2020011018115476.png)

**启动kube-apiserver**

```bash
systemctl restart kube-apiserver
```

![](http://image.ownit.top/csdn/20200110181327729.png)

**查看监听端口**

```bash
[root@master k8s-cert]# netstat -ano | grep 8080
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      off (0.00/0/0)
[root@master k8s-cert]# netstat -ano | grep 6443
tcp        0      0 192.168.116.129:6443    0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 192.168.116.129:44594   192.168.116.129:6443    ESTABLISHED keepalive (9.93/0/0)
tcp        0      0 192.168.116.129:6443    192.168.116.129:44594   ESTABLISHED keepalive (109.64/0/0)
```

![](http://image.ownit.top/csdn/20200110182052356.png)

**运行controller-manager.sh**

```bash
 ./controller-manager.sh 127.0.0.1
./scheduler.sh 127.0.0.1

```

```
[root@master k8s]# ls
apiserver.sh  controller-manager.sh  etcd-cert  etcd.sh  flannel.sh  k8s-cert  master.zip  scheduler.sh  soft
[root@master k8s]# ./controller-manager.sh 127.0.0.1
Created symlink from /etc/systemd/system/multi-user.target.wants/kube-controller-manager.service to /usr/lib/systemd/system/kube-controller-manager.service.
[root@master k8s]# ./scheduler.sh 127.0.0.1
Created symlink from /etc/systemd/system/multi-user.target.wants/kube-scheduler.service to /usr/lib/systemd/system/kube-scheduler.service.
```

![](http://image.ownit.top/csdn/20200110182349745.png)

**创建kubectl管理工具**

```
 cp kubectl /usr/bin/
```

![](http://image.ownit.top/csdn/20200110182826411.png)

**查看集群健康状态**

```
 kubectl get cs
```

## ![](http://image.ownit.top/csdn/20200110182934988.png)

**查看资源名字简写**

```
kubectl api-resources
```

## 8\. 部署Node组件

![](http://image.ownit.top/csdn/20200110183409499.png)

## 1\. 将kubelet-bootstrap用户绑定到系统集群角色

```bash
kubectl create clusterrolebinding kubelet-bootstrap \
--clusterrole=system:node-bootstrapper \
--user=kubelet-bootstrap
```

## ![](http://image.ownit.top/csdn/20200110183302971.png)

## 2\. 创建kubeconfig文件

```bash
#----------------------

APISERVER=$1
SSL_DIR=$2
#需要先前创建的token
BOOTSTRAP_TOKEN=0fb61c46f8991b718eb38d27b605b008

# 创建kubelet bootstrapping kubeconfig 
export KUBE_APISERVER="https://$APISERVER:6443"

# 设置集群参数
kubectl config set-cluster kubernetes \
  --certificate-authority=$SSL_DIR/ca.pem \
  --embed-certs=true \
  --server=${KUBE_APISERVER} \
  --kubeconfig=bootstrap.kubeconfig

# 设置客户端认证参数
kubectl config set-credentials kubelet-bootstrap \
  --token=${BOOTSTRAP_TOKEN} \
  --kubeconfig=bootstrap.kubeconfig

# 设置上下文参数
kubectl config set-context default \
  --cluster=kubernetes \
  --user=kubelet-bootstrap \
  --kubeconfig=bootstrap.kubeconfig

# 设置默认上下文
kubectl config use-context default --kubeconfig=bootstrap.kubeconfig

#----------------------

# 创建kube-proxy kubeconfig文件

kubectl config set-cluster kubernetes \
  --certificate-authority=$SSL_DIR/ca.pem \
  --embed-certs=true \
  --server=${KUBE_APISERVER} \
  --kubeconfig=kube-proxy.kubeconfig

kubectl config set-credentials kube-proxy \
  --client-certificate=$SSL_DIR/kube-proxy.pem \
  --client-key=$SSL_DIR/kube-proxy-key.pem \
  --embed-certs=true \
  --kubeconfig=kube-proxy.kubeconfig

kubectl config set-context default \
  --cluster=kubernetes \
  --user=kube-proxy \
  --kubeconfig=kube-proxy.kubeconfig

kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig
```

**执行脚本**

```bash
 bash kubeconfig.sh 192.168.116.129 /root/k8s/k8s-cert/
```

## ![](http://image.ownit.top/csdn/20200110184023555.png)

**把这两个文件拷贝到2个Node的/opt/kubernetes/cfg/**

```bash
scp bootstrap.kubeconfig kube-proxy.kubeconfig root@192.168.116.130:/opt/kubernetes/cfg/
scp bootstrap.kubeconfig kube-proxy.kubeconfig root@192.168.116.131:/opt/kubernetes/cfg/
```

## ![](http://image.ownit.top/csdn/20200110185122210.png)  
3\. 部署kubelet，kube-proxy组件

**上传node包**

![](http://image.ownit.top/csdn/20200110185242451.png)

**把matser里面的kubelet和kube-poxy拷贝过来**

```bash
scp kubelet kube-proxy root@192.168.116.130:/opt/kubernetes/bin/
scp kubelet kube-proxy root@192.168.116.131:/opt/kubernetes/bin/
```

## ![](http://image.ownit.top/csdn/20200110190055469.png)

## 运行 kubelet.sh

```
 bash kubelet.sh 192.168.116.130
```

## ![](http://image.ownit.top/csdn/2020011019035585.png)

## Master节点颁发csr

```
kubectl get csr
```

```
kubectl certificate approve node-csr-96wka1dqU6bV1MMXD1nNUw14Av8NU6H6IW11ecJlYM0
```

![](http://image.ownit.top/csdn/20200110190737168.png)

**运行proxy.sh**

```
bash proxy.sh 192.168.116.130
```

![](http://image.ownit.top/csdn/20200110191024318.png)

## 9\. 部署多个Node操作

**复制粘贴Node1已经部署好的文件**

```bash
scp -r /opt/kubernetes/ root@192.168.116.131:/opt/
```

![](http://image.ownit.top/csdn/20200110191924709.png)

```bash
scp /usr/lib/systemd/system/{kubelet,kube-proxy}.service root@192.168.116.131:/usr/lib/systemd/system/
```

![](http://image.ownit.top/csdn/20200110192155760.png)

删除复制过来的证书

![](http://image.ownit.top/csdn/2020011019235152.png)

修改Node2上配置文件的IP地址

![](http://image.ownit.top/csdn/20200110192454661.png)

修改完毕，重启即可。

```
[root@node2 cfg]# systemctl restart kubelet
[root@node2 cfg]# systemctl restart kube-proxy
[root@node2 cfg]# ps -ef | grep kube
```

 

![](http://image.ownit.top/csdn/20200110192744279.png)

去Master节点颁发证书

```
kubectl certificate approve node-csr-96wka1dqU6bV1MMXD1nNUw14Av8NU6H6IW11ecJlYM0
```