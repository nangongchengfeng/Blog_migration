---
author: 南宫乘风
categories:
- Kubernetes
- ''
- Kubernetes应用
- ''
- Kubernetes项目实战
date: 2023-05-11 21:39:12
description: 、项目背景随着云原生技术的不断发展，容器化应用已成为企业构建云原生架构的重要方式。而随着集群规模不断扩大，跨主机通信的需求也越来越重要。在集群中，是最小的调度和管理单位，而网络也是中最重要的组成部分。。。。。。。。
image: ../../title_pic/06.jpg
slug: '202305112139'
tags:
- kubernetes
- 网络
- 云原生
title: Calico的BGP打通Kubernetes网络和局域网
---

<!--more-->

## 1、项目背景
随着云原生技术的不断发展，容器化应用已成为企业构建云原生架构的重要方式。而随着集群规模不断扩大，跨主机通信的需求也越来越重要。在 Kubernetes 集群中，Pod 是最小的调度和管理单位，而网络也是 Kubernetes 中最重要的组成部分。为了满足跨主机通信的需求，社区提供了各种各样的解决方案，其中 Calico 是一种利用 BGP 协议解决 Pod 与外部网络通信的解决方案。
## 2、简介
Calico 是一个开源的容器网络解决方案，可以通过使用 BGP 协议来管理容器网络。与传统的基于 VXLAN 的解决方案相比，使用 Calico 可以避免网络数据包的封装和解封过程，提高了网络传输的效率和吞吐量。在 Kubernetes 集群中，Calico 可以用来打通 Pod 和局域网的网络，从而实现跨主机通信。

## 3、背景
* 现状
  集群内pod&node可以通过pod ip直接进行访问，容器访问虚拟机没有问题，但是虚拟机不能访问容器，尤其是通过consul注册的服务，必须打通网络后才可以互相调用
* 目标
  打通pod和虚拟机的网络，使虚拟机可以访问pod ip
  官方文档：[https://docs.projectcalico.org/archive/v3.8/networking/bgp](https://docs.projectcalico.org/archive/v3.8/networking/bgp)

## 4、使用Calico打通Pod网络
1、[Kubernetes Master节点]安装calico控制命令calicoctl
```bash
curl -O -L  https://github.com/projectcalico/calicoctl/releases/download/v3.8.9/calicoctl
chmod +x calicoctl
mv calicoctl /usr/bin/calicoctl
```
2、 [calicoctl安装节点]添加calico配置
```bash
mkdir /etc/calico
cat > /etc/calico/calicoctl.cfg <<EOF
apiVersion: projectcalico.org/v3
kind: CalicoAPIConfig
metadata:
spec:
  datastoreType: "kubernetes"
  kubeconfig: "/root/.kube/config"
EOF


# 测试
calicoctl version
Client Version:    v3.8.9
Git commit:        0991d2fb
Cluster Version:   v3.8.9        # 出现此行代表配置正确
Cluster Type:      k8s,bgp,kdd   # 出现此行代表配置正确
```
3、 [calicoctl安装节点]配置集群路由反射器，node节点与master节点对等、master节点彼此对等
```bash
# 在本环境下将kubernetes master节点作为反射器使用
# 查看节点信息

[root@master1 node]# kubectl get node
NAME     STATUS   ROLES                  AGE     VERSION
master   Ready    control-plane,master   3h19m   v1.22.4
node1    Ready    <none>                 3h16m   v1.22.4
node2    Ready    <none>                 3h15m   v1.22.4


# 导出Master节点配置(多个导出)
calicoctl get node k8s-test-master-1.fjf --export -o yaml > k8s-test-master-1.yml
calicoctl get node k8s-test-master-2.fjf --export -o yaml > k8s-test-master-2.yml
calicoctl get node k8s-test-master-3.fjf --export -o yaml > k8s-test-master-3.yml

calicoctl get node master --export -o yaml > k8s-test-master-1.yml




# 在3个Master节点配置中添加以下配置用于标识该节点为反射器

metadata:
  ......
  labels:
    ......
    i-am-a-route-reflector: true
  ......
spec:
  bgp:
    ......
    routeReflectorClusterID: 224.0.0.1

# 更新节点配置
calicoctl apply -f k8s-test-master-1.yml



# 其他节点与反射器对等
calicoctl apply -f - <<EOF
kind: BGPPeer
apiVersion: projectcalico.org/v3
metadata:
  name: peer-to-rrs
spec:
  nodeSelector: "!has(i-am-a-route-reflector)"
  peerSelector: has(i-am-a-route-reflector)
EOF




# 反射器彼此对等
calicoctl apply -f - <<EOF
kind: BGPPeer
apiVersion: projectcalico.org/v3
metadata:
  name: rr-mesh
spec:
  nodeSelector: has(i-am-a-route-reflector)
  peerSelector: has(i-am-a-route-reflector)
EOF
```
![在这里插入图片描述](../../image/0e283bd56782408389f144e2b87a9e97.png)
4、 [calicoctl安装节点]配置Master节点与核心交换机对等
```bash
calicoctl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: BGPPeer
metadata:
  name: rr-border
spec:
  nodeSelector: has(i-am-a-route-reflector)
  peerIP: 192.168.83.1
  asNumber: 64512
EOF
# peerIP: 核心交换机IP
# asNumber: 用于和核心交换机对等的ID
```
5、 [192.168.83.1,设备型号：cisco 3650]配置核心交换与Master(反射器)节点对等，这一步需要在对端BGP设备上操作，这里是用核心交换机
```bash
router bgp 64512
bgp router-id 192.168.83.1
neighbor 192.168.83.36 remote-as 64512
neighbor 192.168.83.49 remote-as 64512
neighbor 192.168.83.54 remote-as 64512
```
6、查看BGP 对等状态
```bash
calicoctl node status
# INFO字段全部为Established 即为正常
Calico process is running.
 
IPv4 BGP status
+---------------+---------------+-------+----------+-------------+
| PEER ADDRESS  |   PEER TYPE   | STATE |  SINCE   |    INFO     |
+---------------+---------------+-------+----------+-------------+
| 192.168.83.1  | node specific | up    | 06:38:55 | Established |
| 192.168.83.54 | node specific | up    | 06:38:55 | Established |
| 192.168.83.22 | node specific | up    | 06:38:55 | Established |
| 192.168.83.37 | node specific | up    | 06:38:55 | Established |
| 192.168.83.49 | node specific | up    | 06:38:55 | Established |
| 192.168.83.52 | node specific | up    | 06:38:55 | Established |
+---------------+---------------+-------+----------+-------------+
 
IPv6 BGP status
No IPv6 peers found.
```
7、测试，使用其他网段，如192.168.82.0/24的虚拟机ping 某一个pod ip，能正常通信即代表成功
```bash
[dev][root@spring-boot-demo1-192.168.82.85 ~]# ping -c 3 172.15.190.2
PING 172.15.190.2 (172.15.190.2) 56(84) bytes of data.
64 bytes from 172.15.190.2: icmp_seq=1 ttl=62 time=0.677 ms
64 bytes from 172.15.190.2: icmp_seq=2 ttl=62 time=0.543 ms
64 bytes from 172.15.190.2: icmp_seq=3 ttl=62 time=0.549 ms
 
--- 172.15.190.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2000ms
rtt min/avg/max/mdev = 0.543/0.589/0.677/0.067 ms
[dev][root@spring-boot-demo1-192.168.82.85 ~]#
```
## 5、使用Calico打通Svc网络
* 现状
  一般情况下，Kuberntes集群暴露服务的方式有Ingress、NodePort、HostNetwork，这几种方式用在生产环境下是没有问题的，安全性和稳定性有保障。但是在内部开发环境下，使用起来就有诸多不便，开发希望可以直接访问自己的服务，但是Pod IP又是随机变化的，这个时候我们就可以使用SVC IP 或者SVC Name进行访问
* 目标
  打通SVC网络，使开发本地可以通过SVC IP 或 SVC Name访问集群服务
  官方文档：[https://docs.projectcalico.org/archive/v3.8/networking/service-advertisement](https://docs.projectcalico.org/archive/v3.8/networking/service-advertisement)
  注意：前提是已经用BGP打通了Pod网络或已经建立了BGP对等才可以继续进行
  1、 [Kubernetes Master]确定SVC网络信息
```bash
[root@master1 node]# kubectl cluster-info dump|grep -i  "service-cluster-ip-range"
                            "--service-cluster-ip-range=172.16.0.0/16",
                            "--service-cluster-ip-range=172.16.0.0/16",
                           
```
2、 [Kubernetes Master]启用SVC网络广播
```bash
[root@master1 ~]# kubectl patch ds -n kube-system calico-node --patch    '{"spec": {"template": {"spec": {"containers": [{"name": "calico-node", "env": [{"name": "CALICO_ADVERTISE_CLUSTER_IPS", "value": "172.16.0.0/16"}]}]}}}}'
daemonset.apps/calico-node patched
```
3、测试
正常情况下启用BGP广播后，3分钟内核心交换即可接收到路由信息
```bash
# 找到集群DNS服务进行测试
kubectl get svc kube-dns -n kube-system
NAME       TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                  AGE
kube-dns   ClusterIP   172.16.0.10   <none>        53/UDP,53/TCP,9153/TCP   3d21h
 
 
# 找一个Pod IP在集群外进行解析测试，如果可以解析到结果说明SVC网络已经打通
[dev][root@spring-boot-demo1-192.168.82.85 ~]# dig -x 172.15.190.2 @172.16.0.10   
 
; <<>> DiG 9.9.4-RedHat-9.9.4-61.el7_5.1 <<>> -x 172.15.190.2 @172.16.0.10
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 23212
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available
 
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;2.190.15.172.in-addr.arpa.     IN      PTR
 
;; ANSWER SECTION:
2.190.15.172.in-addr.arpa. 30   IN      PTR     172-15-190-2.ingress-nginx.ingress-nginx.svc.k8s-test.fjf. # 可以正常解析到主机记录
 
;; Query time: 3 msec
;; SERVER: 172.16.0.10#53(172.16.0.10)
;; WHEN: Fri Jul 09 15:26:55 CST 2021
;; MSG SIZE  rcvd: 150
```
