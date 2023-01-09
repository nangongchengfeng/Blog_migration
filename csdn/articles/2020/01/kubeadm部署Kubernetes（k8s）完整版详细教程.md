+++
author = "南宫乘风"
title = "kubeadm部署Kubernetes（k8s）完整版详细教程"
date = "2020-01-08 16:49:12"
tags=['Kubernetes', 'k8s', '容器', 'kubeadm']
categories=[]
image = "post/4kdongman/74.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103888459](https://blog.csdn.net/heian_99/article/details/103888459)

 

**kubeadm是官方社区推出的一个用于快速部署kubernetes集群的工具。**

这个工具能通过两条指令完成一个kubernetes集群的部署：

```
# 创建一个 Master 节点
$ kubeadm init

# 将一个 Node 节点加入到当前集群中
$ kubeadm join &lt;Master节点的IP和端口 &gt;

```

<img alt="" class="has" src="https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy82NTM0ODg3LWFkNThjYTMzOWM0MDNhNGIucG5n?x-oss-process=image/format,png">

# **1. ****安装要求**

在开始之前，部署Kubernetes集群机器需要满足以下几个条件：
- 一台或多台机器，操作系统 CentOS7.x-86_x64- 硬件配置：2GB或更多RAM，2个CPU或更多CPU，硬盘30GB或更多- 集群中所有机器之间网络互通- 可以访问外网，需要拉取镜像- 禁止swap分区
## **环境：**

master      192.168.116.129【最低是2核的，不然安装会保存】

node1      192.168.116.130

node2      192.168.116.131

![20200108134510529.png](https://img-blog.csdnimg.cn/20200108134510529.png)

# **2. ****学习目标**
1. **在所有节点上安装Docker和kubeadm**1. **部署Kubernetes Master**1. **部署容器网络插件**1. **部署 Kubernetes Node，将节点加入Kubernetes集群中**1. **部署Dashboard Web页面，可视化查看Kubernetes资源**
 

# **3. ****准备环境**

**1、关闭防火墙：**

```
systemctl stop firewalld
systemctl disable firewalld

```

**2、关闭selinux：**

```
 sed -i 's/enforcing/disabled/' /etc/selinux/config 
 setenforce 0

```

**3、关闭swap：**

```
swapoff -a # 临时关闭
sed -ri 's/.*swap.*/#&amp;/' /etc/fstab  #永久关闭
```

**4、修改主机名称**

```
hostnamectl set-hostname 名字
```

**5、添加主机名与IP对应关系（记得设置主机名）：**

```
cat /etc/hosts
192.168.116.129 master
192.168.116.130 note1
192.168.116.131 note2

```

**6、将桥接的IPv4流量传递到iptables的链**

```
 cat &gt; /etc/sysctl.d/k8s.conf &lt;&lt; EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

```

```
 sysctl --system
```

# **4. ****所有节点安装****Docker/kubeadm/kubelet**

**xshell可以使用发送键盘所有会话来安装。比较省事**

![20200108135752343.png](https://img-blog.csdnimg.cn/20200108135752343.png)

![20200108135728432.png](https://img-blog.csdnimg.cn/20200108135728432.png)

**Kubernetes默认CRI（容器运行时）为Docker，因此先安装Docker。**

## **1、安装Docker**

**安装Docker源**

```
yum install -y wget &amp;&amp; wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo

```

**安装Docker**

```
yum -y install docker-ce-18.06.1.ce-3.el7
```

**开启自启和启动**

```
systemctl enable docker &amp;&amp; systemctl start docker
```

**查看版本**

```
docker --version

```

## 2、** ****安装****kubeadm****，****kubelet****和****kubectl**

**1、添加阿里云YUM的软件源**

```
cat &gt; /etc/yum.repos.d/kubernetes.repo &lt;&lt; EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

```

2、**安装kubeadm，kubelet和kubectl**

**由于版本更新频繁，这里指定版本号部署：**

```
yum install -y kubelet-1.15.0 kubeadm-1.15.0 kubectl-1.15.0
```

**设置开机自启**

```
systemctl enable kubelet
```

# 5、**部署Kubernetes Master**

在192.168.116.129（Master）执行

```
kubeadm init \
--apiserver-advertise-address=192.168.116.129 \
--image-repository registry.aliyuncs.com/google_containers \
--kubernetes-version v1.15.0 \
--service-cidr=10.1.0.0/16 \
--pod-network-cidr=10.244.0.0/16

```

![2020010814064484.png](https://img-blog.csdnimg.cn/2020010814064484.png)

由于默认拉取镜像地址k8s.gcr.io国内无法访问，这里指定阿里云镜像仓库地址。

![20200108140759201.png](https://img-blog.csdnimg.cn/20200108140759201.png)

**已经初始化完成**![20200108140916701.png](https://img-blog.csdnimg.cn/20200108140916701.png)

**使用kubectl工具：**

```
mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

```

# **6. ****安装****Pod****网络插件（****CNI****）**

```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml
```

确保能够访问到quay.io这个registery。

如果下载失败，可以改成这个镜像地址：lizhenliang/flannel:v0.11.0-amd64

也可以使用我给配置文件 [https://www.lanzous.com/i8jjpij](https://www.lanzous.com/i8jjpij)

这里，我是用的是我的配置文件。

![20200108141405260.png](https://img-blog.csdnimg.cn/20200108141405260.png)

```
kubectl apply -f kube-flannel.yml
```

![20200108141559390.png](https://img-blog.csdnimg.cn/20200108141559390.png)

# **7. ****加入****Kubernetes Node**

**在node上安装flannel**

```
docker pull lizhenliang/flannel:v0.11.0-amd64

```

在192.168.116.130（Node）执行。

向集群添加新节点，执行在kubeadm init输出的kubeadm join命令：

```
kubeadm join 192.168.116.129:6443 --token iz96vy.f5ukew9geeome5is \
    --discovery-token-ca-cert-hash sha256:72b689426bfc34512294c29b39ea3b2af3a94e39f62c4434f3a49f16d51a1382 
```

![20200108142415759.png](https://img-blog.csdnimg.cn/20200108142415759.png)

查看Node

```
 kubectl get node

```

![20200108151656809.png](https://img-blog.csdnimg.cn/20200108151656809.png)

添加一下node2，命令如上。切记，先执行**在node上安装flannel**

![2020010815181254.png](https://img-blog.csdnimg.cn/2020010815181254.png)

已经完全准备完成。

```
kubectl get pods -n kube-system

```

![20200108152313199.png](https://img-blog.csdnimg.cn/20200108152313199.png)

# **8. ****测试****kubernetes****集群**

**在Kubernetes集群中创建一个pod，验证是否正常运行：**

**创建nginx容器**

```
 kubectl create deployment nginx --image=nginx
```

**暴露对外端口**

```
 kubectl expose deployment nginx --port=80 --type=NodePort
```

**查看nginx是否运行成功**

```
 kubectl get pod,svc
```

![20200108152607842.png](https://img-blog.csdnimg.cn/20200108152607842.png)

在浏览器访问。三个结点都可访问，说明集群已经搭建完成，

![20200108152655274.png](https://img-blog.csdnimg.cn/20200108152655274.png)

![20200108152708610.png](https://img-blog.csdnimg.cn/20200108152708610.png)

![20200108152722680.png](https://img-blog.csdnimg.cn/20200108152722680.png)

 

扩容nginx副本wei3个，成功

```
kubectl scale deployment nginx --replicas=3

```

![20200108153234116.png](https://img-blog.csdnimg.cn/20200108153234116.png)

```
kubectl get pods

```

![20200108153617737.png](https://img-blog.csdnimg.cn/20200108153617737.png)

 

# **9. ****部署**** Dashboard**

先前已经给配置配置文件。

也可以使用我给配置文件 [https://www.lanzous.com/i8jjpij](https://www.lanzous.com/i8jjpij)

默认镜像国内无法访问，修改镜像地址为： lizhenliang/kubernetes-dashboard-amd64:v1.10.1

默认Dashboard只能集群内部访问，修改Service为NodePort类型，暴露到外部：

![20200108153956631.png](https://img-blog.csdnimg.cn/20200108153956631.png)

**先Docker拉去镜像**

```
docker pull  lizhenliang/kubernetes-dashboard-amd64:v1.10.1

```

**执行kubernetes-dashboard.yaml 文件**

```
 kubectl apply -f kubernetes-dashboard.yaml 
```

**安装成功**

![2020010815404548.png](https://img-blog.csdnimg.cn/2020010815404548.png)

**查看暴露的端口**

```
kubectl get pods,svc -n kube-system

```

![20200108164453386.png](https://img-blog.csdnimg.cn/20200108164453386.png)

 

# **10. ****访问**** Dashboard的web界面**

访问地址：<u>[https://NodeIP:30001](https://NodeIP:30001) 【必须是https】</u>

![20200108164554291.png](https://img-blog.csdnimg.cn/20200108164554291.png)

 

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

![20200108164747779.png](https://img-blog.csdnimg.cn/20200108164747779.png)

已经部署完成。

![20200108164833885.png](https://img-blog.csdnimg.cn/20200108164833885.png)

 
