---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-09-15 10:56:40
description: 错误今天不知道怎么回事，一台机器的报错，也就是无法初始化正常解决办法移除这台主机多余的网卡和然后从重新删除这个错误的，就会恢复正常。。。。。。。
image: http://image.ownit.top/4kdongman/06.jpg
tags:
- 错误问题解决
- golang
- docker
- python
title: calico-node 报错calico/node is not ready BIRD is not ready BGP not established
  with
---

<!--more-->

### **错误**

今天不知道怎么回事，一台机器的calico-node报错，也就是无法初始化正常

![](http://image.ownit.top/csdn/20210915105413198.png)

 

```bash
Events:
  Type     Reason     Age   From               Message
  ----     ------     ----  ----               -------
  Normal   Scheduled  45s   default-scheduler  Successfully assigned kube-system/calico-node-pkbkv to k8s-node2
  Normal   Started    45s   kubelet            Started container install-cni
  Normal   Pulled     45s   kubelet            Container image "docker.io/calico/cni:v3.20.0" already present on machine
  Normal   Started    45s   kubelet            Started container upgrade-ipam
  Normal   Pulled     45s   kubelet            Container image "docker.io/calico/cni:v3.20.0" already present on machine
  Normal   Created    45s   kubelet            Created container install-cni
  Normal   Created    45s   kubelet            Created container upgrade-ipam
  Normal   Started    44s   kubelet            Started container flexvol-driver
  Normal   Pulled     44s   kubelet            Container image "docker.io/calico/pod2daemon-flexvol:v3.20.0" already present on machine
  Normal   Created    44s   kubelet            Created container flexvol-driver
  Normal   Pulled     43s   kubelet            Container image "docker.io/calico/node:v3.20.0" already present on machine
  Normal   Created    43s   kubelet            Created container calico-node
  Normal   Started    43s   kubelet            Started container calico-node
  Warning  Unhealthy  40s   kubelet            Readiness probe failed: calico/node is not ready: BIRD is not ready: Error querying BIRD: unable to connect to BIRDv4 socket: dial unix /var/run/calico/bird.ctl: connect: connection refused
  Warning  Unhealthy  30s   kubelet            Readiness probe failed: 2021-09-15 02:36:49.282 [INFO][417] confd/health.go 180: Number of node(s) with BGP peering established = 0
calico/node is not ready: BIRD is not ready: BGP not established with 172.17.6.120,172.17.6.121,172.17.6.122
  Warning  Unhealthy  20s  kubelet  Readiness probe failed: 2021-09-15 02:36:59.282 [INFO][497] confd/health.go 180: Number of node(s) with BGP peering established = 0
calico/node is not ready: BIRD is not ready: BGP not established with 172.17.6.120,172.17.6.121,172.17.6.122
  Warning  Unhealthy  10s  kubelet  Readiness probe failed: 2021-09-15 02:37:09.280 [INFO][567] confd/health.go 180: Number of node(s) with BGP peering established = 0
calico/node is not ready: BIRD is not ready: BGP not established with 172.17.6.120,172.17.6.121,172.17.6.122
```

### 解决办法

```bash
Remove interfaces related to docker and flannel:
ip link
For each interface for docker or flannel, do the following
ifconfig <name of interface from ip link> down
ip link delete <name of interface from ip link>
```

移除这台主机多余的docker网卡和calico

然后从重新删除这个错误pod的，就会恢复正常

![](http://image.ownit.top/csdn/20210915105625479.png)