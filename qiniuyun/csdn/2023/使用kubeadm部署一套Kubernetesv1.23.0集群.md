---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2023-12-11 10:30:51
description: 使用部署一套集群、前置知识点生产环境可部署集群的两种方式目前生产部署集群主要有两种方式：是一个部署工具，提供和，用于快速部署集群。二进制包从下载发行版的二进制包，手动部署每个组件，组成集群。这里采用搭。。。。。。。
image: ../../title_pic/27.jpg
slug: '202312111030'
tags:
- Kubernetes
title: 使用kubeadm部署一套Kubernetes v1.23.0集群
---

<!--more-->

# 使用kubeadm部署一套Kubernetes v1.23.0集群

# 1、前置知识点

### 1.1 生产环境可部署Kubernetes集群的两种方式

目前生产部署Kubernetes集群主要有两种方式：

•
<span style="font-weight: bold;" data-type="strong">kubeadm</span>

Kubeadm是一个K8s部署工具，提供kubeadm init和kubeadm join，用于快速部署Kubernetes集群。

•
<span style="font-weight: bold;" data-type="strong">二进制包</span>

从github下载发行版的二进制包，手动部署每个组件，组成Kubernetes集群。

这里采用kubeadm搭建集群。

kubeadm工具功能：

•      <span style="font-weight: bold;" data-type="strong">kubeadm init：</span>  初始化一个Master节点

•      <span style="font-weight: bold;" data-type="strong">kubeadm join：</span>  将工作节点加入集群

•      <span style="font-weight: bold;" data-type="strong">kubeadm upgrade：</span>  升级K8s版本

•      <span style="font-weight: bold;" data-type="strong">kubeadm token：</span>  管理 kubeadm join 使用的令牌

•      <span style="font-weight: bold;" data-type="strong">kubeadm reset：</span>  清空 kubeadm init 或者 kubeadm  join 对主机所做的任何更改

•      <span style="font-weight: bold;" data-type="strong">kubeadm version：</span>  打印 kubeadm 版本

•      <span style="font-weight: bold;" data-type="strong">kubeadm alpha：</span>  预览可用的新功能

### 1.2 准备环境

服务器要求：

•
建议最小硬件配置：2核CPU、2G内存、20G硬盘

•
服务器最好可以访问外网，会有从网上拉取镜像需求，如果服务器不能上网，需要提前下载对应镜像并导入节点

软件环境：

|<span style="font-weight: bold;" data-type="strong">软件</span>|<span style="font-weight: bold;" data-type="strong">版本</span>|
| ------------| -------------------------|
|操作系统|CentOS7.9_x64  （mini）|
|Docker|20-ce|
|Kubernetes|1.23|

服务器规划：

|角色|IP|
| ------------| ---------------|
|k8s-master|192.168.31.71|
|k8s-node1|192.168.31.72|
|k8s-node2|192.168.31.73|

架构图：

![image](../../image/3a92fc8986d042d3a424f10f89b295f8.png)​

### 1.3 操作系统初始化配置【所有节点】

```bash
# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

# 关闭selinux
sed -i 's/enforcing/disabled/' /etc/selinux/config  # 永久
setenforce 0  # 临时

# 关闭swap
swapoff -a  # 临时
sed -ri 's/.*swap.*/#&/' /etc/fstab    # 永久

# 根据规划设置主机名
hostnamectl set-hostname <hostname>

# 在master添加hosts
cat >> /etc/hosts << EOF
192.168.31.71 k8s-master
192.168.31.72 k8s-node1
192.168.31.73 k8s-node2
EOF

# 将桥接的IPv4流量传递到iptables的链
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system  # 生效

# 时间同步
yum install ntpdate -y
ntpdate time.windows.com

```

# 2. 安装Docker/kubeadm/kubelet

【所有节点】

这里使用Docker作为容器引擎，也可以换成别的，例如containerd

### 2.1 安装Docker

```bash
wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo
yum -y install docker-ce
systemctl enable docker && systemctl start docker

```

配置镜像下载加速器：

```bash
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://b9pmyelo.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF

systemctl restart docker
docker info

```

### 2.2 添加阿里云YUM软件源

```bash
cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

```

### 2.3 安装kubeadm，kubelet和kubectl

由于版本更新频繁，这里指定版本号部署：

```bash
yum install -y kubelet-1.23.0 kubeadm-1.23.0 kubectl-1.23.0
systemctl enable kubelet

```

‍

# 3. 部署Kubernetes Master

在192.168.31.71（Master）执行。

```python
kubeadm init \
  --apiserver-advertise-address=192.168.31.71 \
  --image-repository registry.aliyuncs.com/google_containers \
  --kubernetes-version v1.23.0 \
  --service-cidr=10.96.0.0/12 \
  --pod-network-cidr=10.244.0.0/16 \
  --ignore-preflight-errors=all

pod
172.20.20.0/20

svc
172.21.20.0/20


```

•	--apiserver-advertise-address 集群通告地址  
•	--image-repository 由于默认拉取镜像地址k8s.gcr.io国内无法访问，这里指定阿里云镜像仓库地址  
•	--kubernetes-version K8s版本，与上面安装的一致  
•	--service-cidr 集群内部虚拟网络，Pod统一访问入口  
•	--pod-network-cidr Pod网络，与下面部署的CNI网络组件yaml中保持一致

‍

初始化完成后，最后会输出一个join命令，先记住，下面用。

拷贝kubectl使用的连接k8s认证文件到默认路径：

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

查看工作节点：

```bash
kubectl get nodes
NAME               STATUS     ROLES            AGE   VERSION
localhost.localdomain   NotReady   control-plane,master   20s   v1.23.0
```

注：由于网络插件还没有部署，还没有准备就绪 NotReady，先继续

参考资料：

[https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file](https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file)

[https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#initializing-your-control-plane-node](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#initializing-your-control-plane-node)

# 4. 加入Kubernetes Node

在192.168.31.72/73（Node）执行。

向集群添加新节点，执行在kubeadm init输出的kubeadm join命令：

```bash
kubeadm join 192.168.31.71:6443 --token 7gqt13.kncw9hg5085iwclx \
--discovery-token-ca-cert-hash sha256:66fbfcf18649a5841474c2dc4b9ff90c02fc05de0798ed690e1754437be35a01
```

默认token有效期为24小时，当过期之后，该token就不可用了。这时就需要重新创建token，可以直接使用命令快捷生成：

```bash
kubeadm token create --print-join-command
```

参考资料：[https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)

# 5. 部署容器网络（CNI）

Calico是一个纯三层的数据中心网络方案，是目前Kubernetes主流的网络方案。

下载YAML：

```bash
wget https://docs.projectcalico.org/manifests/calico.yaml
```

下载完后还需要修改里面定义Pod网络（CALICO_IPV4POOL_CIDR），与前面kubeadm  
init的 --pod-network-cidr指定的一样。

修改完后文件后，部署：

```bash
kubectl apply -f calico.yaml
kubectl get pods -n kube-system
```

等Calico  Pod都Running，节点也会准备就绪。

注：以后所有yaml文件都只在Master节点执行。

安装目录：/etc/kubernetes/

组件配置文件目录：/etc/kubernetes/manifests/

参考资料：[https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network)

# 6. 部署 Dashboard

Dashboard是官方提供的一个UI，可用于基本管理K8s资源。

YAML下载地址：

```
https://raw.githubusercontent.com/kubernetes/dashboard/v2.4.0/aio/deploy/recommended.yaml
```

课件中文件名是：kubernetes-dashboard.yaml

默认Dashboard只能集群内部访问，修改Service为NodePort类型，暴露到外部:

```bash
vi recommended.yaml
...
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      targetPort: 8443
      nodePort: 30001
  selector:
    k8s-app: kubernetes-dashboard
  type: NodePort
...

kubectl apply -f recommended.yaml
kubectl get pods -n kubernetes-dashboard
```

访问地址：[https://NodeIP:30001](https://NodeIP:30001)

创建service account并绑定默认cluster-admin管理员集群角色：

```
# 创建用户

kubectl create serviceaccount dashboard-admin -n kube-system

# 用户授权

kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin

# 获取用户Token

kubectl describe secrets -n kube-system $(kubectl -n kube-system get secret | awk '/dashboard-admin/{print $1}')
```

使用输出的token登录Dashboard。

‍

# 7.K8S 网络和局域网打通

参考文档：[办公环境下 kubernetes 网络互通方案](https://www.qikqiak.com/post/office-env-k8s-network/ "办公环境下 kubernetes 网络互通方案")

在 kubernetes 的网络模型中，基于官方默认的 CNI 网络插件 Flannel，这种 Overlay Network（覆盖网络）可以轻松的实现 pod 间网络的互通。当我们把基于 spring cloud 的微服务迁移到 k8s 中后，无须任何改动，微服务 pod 可以通过 Eureka 注册后可以互相轻松访问。除此之外，我们可以通过 ingress + ingress controller ，在每个节点上，把基于 http 80端口、https 443端口的用户请求流量引入到集群服务中。

但是实际使用中，我们出现了以下需求：

* 1.办公室网络 和 k8s pod 网络不通。开发在电脑完成某个微服务模块开发后，希望本地启动后，能注册到 k8s 中开发环境的服务中心进行调试，而不是本地起一堆依赖的服务。
* 2.办公室网络 和 k8s svc 网络不通。在 k8s 中运行的 mysql、redis 等，无法通过 ingress 7层暴露，电脑无法通过客户端工具直接访问；如果我们通过 service 的 NodePort 模式，会导致维护量工作量巨大。

## 网络互通配置

k8s 集群中新加一台配置不高（2核4G）的 node 节点（node-30）专门做路由转发，连接办公室网络和 k8s 集群 pod、svc

* node-30 IP 地址 192.168.102.30
* 内网 DNS IP 地址 192.168.102.20
* pod 网段 172.20.20.0/20，svc 网段 172.21.20.0/20
* 办公网段 192.168.0.0/16

给 node-30节点打上污点标签（taints），不让 k8s 调度 pod 来占用资源：

```bash
kubectl taint nodes node-30 forward=node-30:NoSchedule
```

node-30节点，做snat：

```bash
# 开启转发
# vim /etc/sysctl.d/k8s.conf
net.ipv4.ip_forward = 1
# sysctl -p

(kubeadm init   --apiserver-advertise-address=192.168.102.30   --image-repository registry.aliyuncs.com/google_containers   --kubernetes-version v1.23.0   --service-cidr=172.21.20.0/20   --pod-network-cidr=172.20.20.0/20   --ignore-preflight-errors=all
)
# 来自办公室访问pod、service snat
SVC
iptables -t nat -A POSTROUTING -s 192.168.0.0/16 -d 172.21.20.0/20 -j MASQUERADE   
POD
iptables -t nat -A POSTROUTING -s 192.168.0.0/16 -d 172.20.20.0/20 -j  MASQUERADE
```

在办公室的出口路由器上，设置静态路由，将 k8s pod 和 service 的网段，路由到 node-30 节点上

```bash
路由器上
ip route 172.20.0.0 255.255.255.0 192.168.102.30
ip route 172.21.0.0  255.255.255.0   192.168.102.30

Linux主机
route add -net 172.20.20.0/20 gw 192.168.102.30
route add -net 172.21.20.0/20 gw 192.168.102.30

sudo ip route add  172.20.0.0/16 via 192.168.102.30 dev eth0
```

![image](../../image/8378adf5ede64683bf0f766b1a3aa989.png)​

## DNS 解析配置

以上步骤操作后，我们就可以在本地电脑通过访问 pod ip 和 service ip 去访问服务。但是在 k8s 中，由于 pod ip 随时都可能在变化，service ip 也不是开发、测试能轻松获取到的。我们希望内网 DNS 在解析 `*.cluster.local`，去`coreDNS`寻找解析结果。

例如，我们约定将（项目A 、开发环境一 、数据库mysql）部署到 ProjectA-dev1 这个 namespace 下，由于本地到 k8s 集群 service 网络已经打通，我们在本地电脑使用 mysql 客户端连接时，只需要填写`mysql.ProjectA-dev1.svc.cluster.local`即可，DNS 查询请求到了内网DNS后，走向 CoreDNS，从而解析出 service ip。

由于内网 DNS 在解析 `*.cluster.local`，需要访问 CoreDNS 寻找解析结果。这就需要保证网络可达

‍

方案一， 最简单的做法，我们把内网DNS架设在node-30这台节点上，那么他肯定访问到kube-dns 10.96.0.10

```bash
# kubectl  get svc  -n kube-system |grep kube-dns
kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP   20d
```

方案二，由于我们实验场景内网DNS IP地址 192.168.102.20 ，并不在node-30上，我们需要打通192.168.102.20  访问 svc网段172.21.20.0/20 即可

```bash
#内网DNS（IP 192.168.102.20） 添加静态路由
route add -net 172.21.0.0/16  gw 192.168.102.30
route add -net 172.20.0.0/16  gw 192.168.102.30

# node-30（IP 192.168.102.30） 做snat
iptables -t nat -A POSTROUTING -s 192.168.102.30 -d 172.21.0.0/16 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 192.168.102.30 -d 172.20.0.0/16 -j MASQUERADE
```

* 方案三（实验选择），由于我们实验场景内网DNS IP 192.168.102.20  并不在node-30上，我们可以用nodeSelector在node-30部署 一个nginx ingress controller， 用4层暴露出来coredns 的TCP/UDP 53端口。
