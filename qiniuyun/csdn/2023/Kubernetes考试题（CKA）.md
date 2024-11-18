---
author: 南宫乘风
categories:
- Kubernetes应用
date: 2023-01-31 18:10:28
description: 题目每次还原初始化快照后，开机后等分钟，登录检查一下所有的，确保都为，再开始练习。、权限控制问题设置配置环境：为部署流水线创建一个新的并将其绑定到范围为特定的的特定。创建一个名为且仅允许创建以下资源类。。。。。。。
image: ../../title_pic/63.jpg
slug: '202301311810'
tags:
- kubernetes
- 容器
- 云原生
title: Kubernetes考试题（CKA）
---

<!--more-->

# CKA题目

每次还原初始化快照后，开机后等5分钟，ssh登录node01（11.0.1.112）检查一下所有的pod，确保都为Running，再开始练习。

```bash
kubectl get pod -A
```

# 1、权限控制RBAC

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Context 
为部署流水线创建一个新的ClusterRole并将其绑定到范围为特定的  namespace 的特定ServiceAccount。 
 
Task 
创建一个名为deployment-clusterrole且仅允许创建以下资源类型的新ClusterRole： 
Deployment 
StatefulSet 
DaemonSet 
在现有的  namespace app-team1中创建一个名为cicd-token的新  ServiceAccount。 
限于  namespace app-team1中，将新的ClusterRole deployment-clusterrole绑定到新的  ServiceAccount cicd-token。
```

考点：RBAC授权模型的理解。

没必要参考网址，使用-h帮助更方便。  
kubectl create clusterrole \-h  
kubectl create rolebinding \-h

### 解答

```bash
kubectl create clusterrole deployment-clusterrole --verb=create --resource=deployments,statefulsets,daemonsets 
 
kubectl -n app-team1 create serviceaccount cicd-token 
#  题目中写了“限于namespace app-team1中”，则创建rolebinding。没有写的话，则创建clusterrolebinding。 
kubectl -n app-team1 create rolebinding cicd-token-rolebinding --clusterrole=deployment-clusterrole --serviceaccount=app-team1:cicd-token 
# rolebinding后面的名字cicd-token-rolebinding随便起的，因为题目中没有要求，如果题目中有要求，就不能随便起了。
检查（考试时，可以不检查的） 
kubectl -n app-team1 describe rolebinding cicd-token-rolebinding 
```

‍

# 2、查看pod的CPU

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
通过  pod label name=cpu-loader，找到运行时占用大量  CPU 的  pod，   
并将占用  CPU 最高的  pod 名称写入文件  /opt/KUTR000401/KUTR00401.txt（已存在）。 
```

考点：kubectl top \--l 命令的使用

没必要参考网址，使用-h帮助更方便。  
kubectl top pod \-h

‍

### 解答

```bash
考试时务必执行，切换集群。模拟环境中不需要执行。 
# kubectl config use-context k8s 
 
开始操作 
 
# 查看pod名称  -A是所有namespace 
kubectl top pod -l name=cpu-loader --sort-by=cpu -A 
 
# 将cpu占用最多的pod的name写入/opt/test1.txt文件 
echo "查出来的Pod Name" > /opt/KUTR000401/KUTR00401.txt 
 
检查 
cat /opt/KUTR000401/KUTR00401.txt 
```

# 3、配置网络策略 NetworkPolicy

‍

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context hk8s 
 
Task 
在现有的namespace my-app中创建一个名为allow-port-from-namespace的新NetworkPolicy。 
确保新的NetworkPolicy允许namespace echo中的Pods连接到namespace my-app中的Pods的9000端口。 
 
进一步确保新的NetworkPolicy： 
不允许对没有在监听  端口9000的Pods的访问 
不允许非来自  namespace echo中的Pods的访问 
```

双重否定就是肯定，所以最后两句话的意思就是：  
仅允许端口为9000的pod方法。  
仅允许echo命名空间中的pod访问。

**考点：NetworkPolicy 的创建**

### 解答

参考官方文档，拷贝yaml文件内容，并修改。  
这里要注意，模拟题和真题截图里都有提到echo这个namespace，但是和真题的截图比较，你会发现，两个echo出现的位置不同，一个作为访问者，一个作为  
被访问者。  
所以不要搞混了。他们其实只是个名字而已，叫什么都无所谓，但要分清访问和被访问。

**podSelector**：每个 NetworkPolicy 都包括一个 `podSelector`​， 它对该策略所适用的一组 Pod 进行选择。示例中的策略选择带有 " role \(作用\) =db" 标签的 Pod。 空的 `podSelector`​ 选择名字空间下的所有 Pod。

```bash
开始操作 
 
查看所有ns的标签label 
kubectl get ns --show-labels 
如果访问者的namespace没有标签label，则需要手动打一个。如果有一个独特的标签label，则也可以直接使用。 
kubectl label ns echo project=echo

编写一个yaml文件 
vim networkpolicy.yaml 
#注意  :set paste，防止yaml文件空格错序。 

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
  namespace: my-app
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              project: echo
      ports:
        - protocol: TCP
          port: 9000
```

检查

```bash
kubectl describe networkpolicy -n my-app 
```

# 4、暴露服务 service

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
请重新配置现有的deployment  front-end  以及添加名为http的端口规范来公开现有容器  nginx 的端口80/tcp。
创建一个名为front-end-svc的新service，以公开容器端口http。 
配置此service，以通过各个Pod所在的节点上的  NodePort  来公开他们。 
```

‍

### 解答

```bash
# kubectl config use-context k8s 
 
开始操作 
 
检查deployment信息，并记录SELECTOR的Lable标签，这里是app=front-end 
kubectl get deployment front-end -o wide 

参考官方文档，按照需要edit deployment，添加端口信息 
kubectl edit deployment front-end 
#注意  :set paste，防止yaml文件空格错序。 
    spec: 
      containers: 
      - image: vicuu/nginx:hello 
        imagePullPolicy: IfNotPresent 
        name: nginx         #找到此位置。下文会简单说明一下yaml文件的格式，不懂yaml格式的，往下看。 
        ports:                  #添加这4行 
        - name: http 
          containerPort: 80 
          protocol: TCP 

暴露对应端口 
kubectl expose deployment front-end --type=NodePort --port=80 --target-port=80 --name=front-end-svc 

#注意考试中需要创建的是NodePort，还是ClusterIP。如果是ClusterIP，则应为--type=ClusterIP 
#--port是service的端口号，--target-port是deployment里pod的容器的端口号。 

暴露服务后，检查一下service的selector标签是否正确，这个要与deployment的selector标签一致的。 
kubectl get svc front-end-svc -o wide 
kubectl get deployment front-end -o wide 
```

# 5、创建 Ingress

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
如下创建一个新的nginx Ingress 资源： 
名称: ping 
Namespace: ing-internal 
使用服务端口  5678在路径  /hello  上公开服务  hello 
 
可以使用以下命令检查服务  hello的可用性，该命令应返回  hello： 
curl -kL <INTERNAL_IP>/hello 
```

### 解答

‍

```bash
vim ingress.yaml 
#注意  :set paste，防止yaml文件空格错序。 

apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    app.kubernetes.io/component: controller
  name: nginx-example
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"
spec:
  controller: k8s.io/ingress-nginx
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ping
  namespace: front-end
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx-example #这里调用上面新建的ingressClassName 为nginx-example 
  rules:
  - http:
      paths:
      - path: /hello
        pathType: Prefix
        backend:
          service:
            name: hello
            port:
              number: 80
```

‍

最后curl检查

通过get ingress 查看ingress 的内外IP，然后通过提供的 curl 测试 ingress 是否正确。

‍

另一种方法

```bash
kubectl create ingress ping --rule=/hello=hello:5678 --class=nginx --annotation=nginx.ingress.kubernetes.io/rewrite-target=/ -n ing-internal 
```

‍

# 6、扩容 deployment副本数量

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
将  deployment   presentation 扩展至  4个  pods 
```

kubectl scale deployment \-h

### 解答

```bash
先检查一下现有的pod数量（可不检查） 
kubectl get deployments presentation -o wide 
kubectl get pod -l app=presentation

扩展成4个 
kubectl scale deployment presentation --replicas=4 
```

# 7、调度 pod 到指定节点

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
按如下要求调度一个  pod： 
名称：nginx-kusc00401 
Image：nginx 
Node selector：disk=ssd 
```

考点：nodeSelect属性的使用

### 解答

```bash
开始操作 
先检查一个是否有这个pod，应该是没有创建的，所以需要创建 
kubectl get pod -A|grep nginx-kusc00401 

#  确保node有这个labels，考试时，检查一下就行，应该已经提前设置好了labels。
 
kubectl get nodes --show-labels|grep 'disk=ssd' 

node02 添加标签
kubectl label nodes node02 disk=ssd

cat pod_nginx_ssd.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: app
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disk: ssd

kubectl get pod nginx -o wide
```

# 8、查看可用节点数量

### 问题

```bash
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
检查有多少  nodes 已准备就绪（不包括被打上  Taint：NoSchedule 的节点），   
并将数量写入  /opt/KUSC00402/kusc00402.txt
```

考点：检查节点角色标签，状态属性，污点属性的使用

kubectl \-h

### 解答

```bash
# grep的-i 是忽略大小写，grep -v是排除在外，grep -c是统计查出来的条数。 
kubectl describe nodes | grep -i Taints | grep -vc NoSchedule 
echo "查出来的数字" > /opt/KUSC00402/kusc00402.txt 


其实你直接使用如下命令，就能一眼看出来，几个没有的。 
kubectl describe nodes | grep -i Taints 
```

# 9、创建多容器的 pod

### 问题

```bash
设置配置环境： 
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
按如下要求调度一个Pod： 
名称：kucc8 
app containers: 2 
container  名称/images： 
⚫  nginx 
⚫  consul 
```

### 解答

```bash
# kubectl config use-context k8s 
 
可以参考上一题“调度pod到指定节点”的yaml配置文件。 
 
开始操作 
 
vim pod-kucc.yaml 
#注意  :set paste，防止yaml文件空格错序。 
 

apiVersion: v1
kind: Pod
metadata:
  name: nginx-consul
  labels:
    env: app
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  - name: consul
    image: consul
    imagePullPolicy: IfNotPresent


kubectl get pod nginx-consul
```

# 10、创建 PV

### 问题

```bash
Task 
创建名为  app-config  的  persistent volume，容量为  1Gi，访问模式为  ReadWriteMany。   
volume 类型为  hostPath，位于  /srv/app-config 
```

考点：hostPath类型的pv

### 解答

https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

```bash
直接从官方复制合适的案例，修改参数，然后设置  hostPath 为  /srv/app-config 即可。 
 
开始操作 
 
vim pv.yaml 
#注意  :set paste，防止yaml文件空格错序。 

[root@bt cka]# cat pv_config_app.yaml 
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
spec:
  capacity:
    storage: 1Gi 
  accessModes:
    - ReadWriteMany
  hostPath:
    path: "/srv/app-config"



kubectl get pv 
# RWX是ReadWriteMany，RWO是ReadWriteOnce。 
```

# 11、创建 PVC

### 问题

```bash
Task 
创建一个新的PersistentVolumeClaim： 
名称: pv-volume 
Class: csi-hostpath-sc 
容量: 10Mi 
 
创建一个新的Pod，来将PersistentVolumeClaim作为volume进行挂载： 
名称：web-server 
Image：nginx:1.16 
挂载路径：/usr/share/nginx/html 
 
配置新的Pod，以对volume具有ReadWriteOnce权限。 
 
最后，使用kubectl edit或kubectl patch将  PersistentVolumeClaim的容量扩展为70Mi，并记录此更改。 
```

考点：pvc的创建class属性的使用，–record记录变更

### 解答

```shell
根据官方文档复制一个PVC配置，修改参数，不确定的地方就是用  kubectl 的  explain 帮助。 
 
开始操作
vim pvc.yaml 
#注意  :set paste，防止yaml文件空格错序。

[root@bt cka]# cat pvc_storgae.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-volume
spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi

创建PVC 
kubectl apply -f pvc.yaml 
 
检查 
kubectl get pvc

vim pvc-pod.yaml 
#注意  :set paste，防止yaml文件空格错序

apiVersion: v1 
kind: Pod 
metadata: 
  name: web-server 
spec: 
  volumes: 
    - name: task-pv-storage   #绿色的两个name要一样。 
      persistentVolumeClaim: 
        claimName: pv-volume  #这个要使用上面创建的pvc名字 
  containers: 
    - name: nginx 
      image: nginx:1.16 
      volumeMounts: 
        - mountPath: "/usr/share/nginx/html" 
          name: task-pv-storage   #绿色的两个name要一样。 


创建 
kubectl apply -f pvc-pod.yaml 
 
检查 
kubectl get pod web-server 

改大小，并记录过程。 
#  将storage: 10Mi改为storage: 70Mi   （模拟环境里会报错，下面有解释。） 
#  注意是修改上面的spec:里面的storage: 
kubectl edit pvc pv-volume --record  
#模拟环境是nfs存储，操作时，会有报错忽略即可。考试时用的动态存储，不会报错的。
模拟环境使用的是nfs做后端存储，是不支持动态扩容pvc的（:wq保存退出时，会报错）。 
所以最后一步修改为70Mi，只是操作一下即可。换成ceph做后端存储，可以，但是集群资源太少，无法做ceph。
```

‍

# 12、查看 pod 日志

### 问题

```bash
[candidate@node-1] $ kubectl config use-context k8s 
 
Task 
监控  pod foo 的日志并： 
提取与错误  RLIMIT_NOFILE相对应的日志行 
将这些日志行写入  /opt/KUTR00101/foo 
```

考点：kubectl logs命令

### 解答

```bash
kubectl logs foo | grep "RLIMIT_NOFILE" > /opt/KUTR00101/foo

检查 
cat /opt/KUTR00101/foo 
```

# 13、使用 sidecar 代理容器日志

### 问题

```bash
[candidate@node-1] $ kubectl config use-context k8s 
 
Context 
将一个现有的  Pod 集成到  Kubernetes 的内置日志记录体系结构中（例如  kubectl logs）。 
添加  streaming sidecar 容器是实现此要求的一种好方法。 
 
Task 
使用busybox Image来将名为sidecar的sidecar容器添加到现有的Pod 11-factor-app中。 
新的sidecar容器必须运行以下命令： 
/bin/sh -c tail -n+1 -f /var/log/11-factor-app.log 
使用挂载在/var/log的Volume，使日志文件11-factor-app.log 可用于sidecar 容器。 
除了添加所需要的volume mount以外，请勿更改现有容器的规格。 
```

考题翻译成白话，就是：  
添加一个名为sidecar 的边车容器\(使用busybox 镜像\)，加到已有的 pod 11-factor-app 中。  
确保 sidecar 容器能够输出 /var/log/11-factor-app.log 的信息。  
使用 volume 挂载 /var/log 目录，确保 sidecar 能访问 11-factor-app.log 文件

**考点：pod两个容器共享存储卷**

https://kubernetes.io/zh-cn/docs/concepts/cluster-administration/logging/

### 解答

```bash
通过  kubectl get pod -o yaml 的方法备份原始  pod 信息，删除旧的pod 11-factor-app 
copy 一份新  yaml 文件，添加  一个名称为  sidecar 的容器 
新建  emptyDir 的卷，确保两个容器都挂载了  /var/log 目录 
新建含有  sidecar 的  pod，并通过  kubectl logs 验证 


apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: leagcy-app
    image: busybox
    args:
    - /bin/sh
    - -c
    - >
      i=0;
      while true;
      do
        echo "$i: $(date)" >> /var/log/legacy-app.log;
        i=$((i+1));
        sleep 1;
      done    
    volumeMounts:
    - name: varlog
      mountPath: /var/log

  - name: sidecar
    image: busybox
    args: [/bin/sh, -c, 'tail -n+1 -F /var/log/legacy-app.log']
    volumeMounts:
    - name: varlog
      mountPath: /var/log

  volumes:
  - name: varlog
    emptyDir: {}

验证：
kubectl exec counter-log -c sidecar  -- tail -f /var/log/legacy-app.log
```

# 14、升级集群

### 问题

```bash
Task 
现有的Kubernetes 集群正在运行版本1.25.1。仅将master节点上的所有  Kubernetes控制平面和节点组件升级到版本1.25.2。 
 
确保在升级之前  drain master节点，并在升级后  uncordon master节点。   
 
可以使用以下命令，通过ssh连接到master节点： 
ssh master01 
可以使用以下命令，在该master节点上获取更高权限： 
sudo -i 
 
另外，在主节点上升级kubelet和kubectl。 
请不要升级工作节点，etcd，container 管理器，CNI插件，  DNS服务或任何其他插件。 
```

（注意，考试敲命令时，注意要升级的版本，根据题目要求输入具体的升级版本！！！）

考点：如何离线主机，并升级控制面板和升级节点

### 解答

‍

```bash
1、切换环境
kubectl config use-context mk8s

2、配置
#升级kueadm

kubectl cordon master01 
kubectl drain mk8s-master-0 --ignore=daemonsets

连接master机器 提权
ssh mk8s-master-0
sudo -i 


升级kubeadm

apt-get update 
apt-cache show kubeadm|grep 1.25.2 

apt install kubeadm=1.25.2   -y
kubeadm upgrade plan
#这里可以先查下的：apt-cache show|grep kubeadm
#kubeadm upgrade install v1.20.1 #。。。淦，这个写错了。。。。。。。是apply，并且要加上--ectd-ugrade=false。。。。。。题目要求不升级 etcd； 注意下这2个版本号写法的区别。。。。
kubeadm upgrade apply v1.20.1 --etcd-upgrade=false


#升级kubelt 和 kubectl

apt install kubelet=1.20.1-00 kubectl=1.20.1-00 -y
systemctl restart kubelet #这里要重启下kubelt的，切记。。。

exit
exit

kubectl uncordon mk8s-master-0

3、验证
kubectl get node -owide
kubectl --version
kubelet --version
```

# 15、备份还原 etcd

### 问题

```bash
此项目无需更改配置环境。但是，在执行此项目之前，请确保您已返回初始节点。 
[candidate@master01] $ exit   #注意，这个之前是在master01上，所以要exit退到node01，如果已经是node01了，就不要再exit了。 
 
Task 
首先，为运行在https://11.0.1.111:2379 上的现有  etcd 实例创建快照并将快照保存到  /var/lib/backup/etcd-snapshot.db 
（注意，真实考试中，这里写的是https://127.0.0.1:2379） 
为给定实例创建快照预计能在几秒钟内完成。  如果该操作似乎挂起，则命令可能有问题。用  CTRL + C 来取消操作，然后重试。 
然后还原位于/data/backup/etcd-snapshot-previous.db的现有先前快照。 
提供了以下TLS证书和密钥，以通过etcdctl连接到服务器。 
 
CA 证书: /opt/KUIN00601/ca.crt 
客户端证书: /opt/KUIN00601/etcd-client.crt 
客户端密钥: /opt/KUIN00601/etcd-client.key 
```

**考点：etcd的备份和还原命令**

### 解答

```bash
# 备份
ETCDCTL_API=3 etcdctl snapshot save /data/backup/etcd-snapshot.db --endpoints=https://127.0.0.1:2379 --cacert=/opt/KUIN00601/ca.crt --cert=/opt/KUIN00601/etcd-client.crt --key=/opt/KUIN00601/etcd-client.key
# 恢复  
systemctl stop etcd 
systemctl cat etcd # 确认下数据目录（--data-dir值） 
mv /var/lib/etcd /var/lib/etcd.bak 
ETCDCTL_API=3 etcdctl snapshot restore /data/backup/etcd-snapshot-previous.db --data-dir=/var/lib/etcd 
chown -R etcd:etcd /var/lib/etcd 
systemctl start etcd

```

‍

‍

# 16、排查集群中故障节点

### 问题

```bash
名为node02的Kubernetes worker node处于NotReady状态。 
调查发生这种情况的原因，并采取相应的措施将node恢复为Ready状态，确保所做的任何更改永久生效。 
 
可以使用以下命令，通过ssh连接到node02节点： 
ssh node02 
可以使用以下命令，在该节点上获取更高权限： 
sudo -i
```

### 解答

```bash
过  get nodes 查看异常节点，登录节点查看  kubelet 等组件的  status 并判断原因。 
真实考试时，这个异常节点的kubelet服务没有启动导致的，就这么简单。 
 
执行初始化这道题的脚本a.sh，模拟node02异常。 
（考试时，不需要执行的！考试时切到这道题的集群后，那个node就是异常的。）


1、切换环境
kubectl config use-context wk8s #考试时切到这道题的集群后，那个 node 就是异常的。  真实考试时，这个异常节点的 kubelet 服务没有启动导致的，就这么简单。

2、配置
kubectl get node #查看Not Ready的node节点

ssh wk8s-node-0
sudo -i

systemctl status kubelet
systemctl start kubelet
systemctl enable kubelet

exit #退出root用户
exit #退出故障节点

3、验证
kubectl get node

#jounarlctl -u kubelet 查看kubelet日志
```

# 17、节点维护

### 问题

```bash
Task 
将名为  node02  的  node 设置为不可用，并重新调度该  node 上所有运行的  pods。 
```

考点：cordon和drain 命令的使用

### 解答

```bash
1、切换环境
kubectl config use-context ek8s

2、配置

kubectl cordon ek8s-node-1 #设置次节点为不可调度s
kubectl drain ek8s-node-1 --ignore-daemonsets #设置次节点为不可调度，并且排空次节点

#如果上面命令报错就加上一个 --delete-local-data --force
kubectl drain ek8s-node-1 --ignore-daemonsets --delete-local-data --force
kubectl drain ek8s-node-1 --ignore-daemonsets --delete-emptydir-data --force

3、验证
kubectl get node
```