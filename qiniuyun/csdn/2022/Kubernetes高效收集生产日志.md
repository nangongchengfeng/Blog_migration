---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2022-03-12 19:40:43
description: 容器本身特性：采集目标多：容器本身的特性导致采集目标多，需要采集容器内日志、容器。对于容器内部的文件日志采集，现在并没有一个很好的工具能够去动态发现采集。针对每种数据源都有对应的采集软件，但缺乏一站式。。。。。。。
image: ../../title_pic/29.jpg
slug: '202203121940'
tags:
- kubernetes
- docker
- 容器
title: Kubernetes高效收集生产日志
---

<!--more-->

- 容器本身特性：
  - 采集目标多：容器本身的特性导致采集目标多，需要采集容器内日志、容器 stdout。对于容器内部的文件日志采集，现在并没有一个很好的工具能够去动态发现采集。针对每种数据源都有对应的采集软件，但缺乏一站式的工具。
  - 弹性伸缩难：kubernetes 是分布式的集群，服务、环境的弹性伸缩对于日志采集带来了很大的困难，无法像传统虚拟机环境下那样，事先配置好日志的采集路径等信息，采集的动态性以及数据完整性是非常大的挑战。
- 现有日志工具的一些缺陷：
  - 缺乏动态配置的能力。目前的采集工具都需要事先手动配置好日志采集方式和路径等信息，因为它无法能够自动感知到容器的生命周期变化或者动态漂移，所以它无法动态地去配置。
  - 日志采集重复或丢失的问题。因为现在的一些采集工具基本上是通过 tail 的方式来进行日志采集的，那么这里就可能存在两个方面的问题：一个是可能导致日志丢失，比如采集工具在重启的过程中，而应用依然在写日志，那么就有可能导致这个窗口期的日志丢失；而对于这种情况一般保守的做法就是，默认往前多采集 1M 日志或 2M 的日志，那么这就又会可能引起日志采集重复的问题。
  - 未明确标记日志源。因为一个应用可能有很多个容器，输出的应用日志也是一样的，那么当我们将所有应用日志收集到统一日志存储后端时，在搜索日志的时候，我们就无法明确这条日志具体是哪一个节点上的哪一个应用容器产生的。

本文档将介绍一种 Docker 日志收集工具 log-pilot，结合 Elasticsearch 和 kibana 等工具，形成一套适用于 kubernetes 环境下的一站式日志解决方案。

[GitHub \- AliyunContainerService/log-pilot: Collect logs for docker containersCollect logs for docker containers. Contribute to AliyunContainerService/log-pilot development by creating an account on GitHub.![](../../image/fluidicon.png)https://github.com/AliyunContainerService/log-pilot](https://github.com/AliyunContainerService/log-pilot "GitHub \- AliyunContainerService/log-pilot: Collect logs for docker containers")[容器日志采集利器Log-Pilot-阿里云开发者社区容器时代越来越多的传统应用将会逐渐容器化，而日志又是应用的一个关键环节，那么在应用容器化过程中，如何方便快捷高效地来自动发现和采集应用的日志，如何与日志存储系统协同来高效存储和搜索应用日志，本文将主要跟大家分享下如何通过Log-Pilot来采集容器的标准输出日志和容器内文件日志。![icon-default.png?t=M276](../../image/icon-default.png)https://developer.aliyun.com/article/674327](https://developer.aliyun.com/article/674327 "容器日志采集利器Log-Pilot-阿里云开发者社区")

Log-Pilot 支持容器事件管理，它能够动态地监听容器的事件变化，然后依据容器的标签来进行解析，生成日志采集配置文件，然后交由采集插件来进行日志采集。

相关特点和优势，可以点击上方的链接学习。

# 方案

从日志的采集方式上，在我看来方案大致主要分为两种：

\*\*（1）POD 里面安装logging agent\*\*

每个pod里面都要安装一个agent，无论是以放在本container还是以sidecar的方式部署，很明显会占用很多资源，基本不推荐

\*\*（2）在节点上安装logging agent（推荐）\*\*

其实容器stdout,stderr的日志最终也是落在[宿主机](https://cloud.tencent.com/product/cdh?from=10680 "宿主机")上，而容器内的路径可以通过配置volumeMount 在宿主机上配置映射即可，所以这种方式还是最可行的

> 当然应用还可以自己通过代码直接上报给日志服务，但是这种方式不够通用，还增加了业务代码的复杂性

**log-Pilot**是一个智能容器日志采集工具，它不仅能够高效便捷地将容器日志采集输出到多种存储日志后端，同时还能够动态地发现和采集容器内部的日志文件，更多咨询可以移步[这里](https://yq.aliyun.com/articles/674327 "这里")。

log-Pilot目前支持两种工具对日志进行收集，[Fluentd Plugin](https://github.com/AliyunContainerService/log-pilot/blob/master/docs/fluentd/docs.md "Fluentd Plugin") 和 [Filebeat Plugin](https://github.com/AliyunContainerService/log-pilot/blob/master/docs/filebeat/docs.md "Filebeat Plugin")。  
  
  
Log-Pilot支持容器事件管理，它能够动态地监听容器的事件变化，然后依据容器的标签来进行解析，生成日志采集配置文件，然后交由采集插件来进行日志采集

以下的的安装配置，是基于上一篇的EFK的配置，只是修改收集端（有必要，可以了解上一篇的文章）

[Kubernetes安装EFK日志收集\_南宫乘风-Linux运维-虚拟化容器-Python编程 ownit.top-CSDN博客](https://blog.csdn.net/heian_99/article/details/123405383?spm=1001.2014.3001.5501 "Kubernetes安装EFK日志收集_南宫乘风-Linux运维-虚拟化容器-Python编程     ownit.top-CSDN博客")

# 准备

参考官方[部署文档](https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/fluentd-elasticsearch "部署文档")的基础上使用本项目`manifests/efk/`部署，以下为几点主要的修改：

- **增加** **log-Pilot 部署代码（解决 不支持 es7.0 版本以上的痛点）**
- 修改官方docker镜像，方便国内下载加速
- 修改 es-statefulset.yaml 支持日志存储持久化等
- 增加自动清理日志

# 创建 Elasticsearch 集群

```bash
apiVersion: v1
kind: Namespace
metadata:
  name: logging
```

## 1、 es-service.yaml

```bash
kind: Service
apiVersion: v1
metadata:
  name: elasticsearch
  namespace: logging
  labels:
    app: elasticsearch
spec:
  selector:
    app: elasticsearch
  clusterIP: None
  ports:
    - port: 9200
      name: rest
    - port: 9300
      name: inter-node
```

定义了一个名为 elasticsearch 的 Service，指定标签 `app=elasticsearch`，当我们将 Elasticsearch StatefulSet 与此服务关联时，服务将返回带有标签 `app=elasticsearch`的 Elasticsearch Pods 的 DNS A 记录，然后设置 `clusterIP=None`，将该服务设置成无头服务。最后，我们分别定义端口9200、9300，分别用于与 REST API 交互，以及用于节点间通信。 

```bash
[root@master01 efk]# kubectl apply -f es-service.yaml
service/elasticsearch-logging created
[root@master01 efk]# kubectl get svc -n kube-system 
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
elasticsearch-logging   ClusterIP   None            <none>        9200/TCP                     15s
```

## es-statefulset.yaml

```bash
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: es
  namespace: logging
spec:
  serviceName: elasticsearch
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels: 
        app: elasticsearch
    spec:
      nodeSelector:  #记得给节点把标签，不然会找到不符合的节点
        es: log
      initContainers:
      - name: increase-vm-max-map
        image: busybox
        command: ["sysctl", "-w", "vm.max_map_count=262144"]
        securityContext:
          privileged: true
      - name: increase-fd-ulimit
        image: busybox
        command: ["sh", "-c", "ulimit -n 65536"]
        securityContext:
          privileged: true
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:7.6.2
        ports:
        - name: rest
          containerPort: 9200
        - name: inter
          containerPort: 9300
        resources:
          limits:
            cpu: 1000m
          requests:
            cpu: 1000m
        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data
        env:
        - name: cluster.name
          value: k8s-logs
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: cluster.initial_master_nodes
          value: "es-0,es-1,es-2"
        - name: discovery.zen.minimum_master_nodes
          value: "2"
        - name: discovery.seed_hosts
          value: "elasticsearch"
        - name: ES_JAVA_OPTS
          value: "-Xms512m -Xmx512m"
        - name: network.host
          value: "0.0.0.0"
  volumeClaimTemplates:
  - metadata:
      name: data
      labels:
        app: elasticsearch
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: nfsdata
      resources:
        requests:
          storage: 5Gi 
```

![](../../image/ea6bebb226ff4569a5b5793743149eaa.png)

 Pods 部署完成后，我们可以通过请求一个 REST API 来检查 Elasticsearch 集群是否正常运行。使用下面的命令将本地端口9200 转发到 Elasticsearch 节点（如es-0）对应的端口：

```bash
[root@master01 new]# kubectl port-forward es-0 9200:9200 --namespace=logging
Forwarding from 127.0.0.1:9200 -> 9200
Forwarding from [::1]:9200 -> 9200
```

```
curl http://localhost:9200/_cluster/state?pretty
```

![](../../image/be8ab8d757834cdda7cd3dc3ed0e3a38.png)

 看到上面的信息就表明我们名为 k8s-logs 的 Elasticsearch 集群成功创建了3个节点：es-0，es-1，和es-2，当前主节点是 es-0

# 创建 Kibana 服务

Elasticsearch 集群启动成功了，接下来我们可以来部署 Kibana 服务，新建一个名为 kibana.yaml 的文件，对应的文件内容如下：

## kibana.yaml 

```bash
apiVersion: v1
kind: Service
metadata:
  name: kibana
  namespace: logging
  labels:
    app: kibana
spec:
  ports:
  - port: 5601
  type: NodePort
  selector:
    app: kibana
 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: logging
  labels:
    app: kibana
spec:
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      nodeSelector:
        es: log
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:7.6.2
        resources:
          limits:
            cpu: 1000m
          requests:
            cpu: 1000m
        env:
        - name: ELASTICSEARCH_HOSTS
          value: http://elasticsearch:9200
        ports:
        - containerPort: 5601
```

上面我们定义了两个资源对象，一个 Service 和 Deployment，为了测试方便，我们将 Service 设置为了 NodePort 类型，Kibana Pod 中配置都比较简单，唯一需要注意的是我们使用 `ELASTICSEARCH_HOSTS` 这个环境变量来设置Elasticsearch 集群的端点和端口，直接使用 Kubernetes DNS 即可，此端点对应服务名称为 elasticsearch，由于是一个 headless service，所以该域将解析为3个 Elasticsearch Pod 的 IP 地址列表。 配置完成后，直接使用 kubectl 工具创建：

```bash
kubectl create -f kibana.yaml
service/kibana created
deployment.apps/kibana created
```

创建完成后，可以查看 Kibana Pod 的运行状态

```bash
[root@master01 new]#  kubectl get pods --namespace=logging
NAME                      READY   STATUS    RESTARTS   AGE
es-0                      1/1     Running   0          13m
es-1                      1/1     Running   0          9m48s
es-2                      1/1     Running   0          7m46s
kibana-8476dc9bbf-6mm6k   1/1     Running   0          3m2s
```

如果 Pod 已经是 Running 状态了，证明应用已经部署成功了，然后可以通过 NodePort 来访问 Kibana 这个服务，在浏览器中打开`http://<任意节点IP>:31838`即可，

出现 这个代表成功

![](../../image/9631236c38634351822510057c521ba3.png)

# 部署 **log-Pilot**

Log-pilot是一个智能容器日志采集工具，它不仅能够高效便捷地将容器日志采集输出到多种存储日志后端，同时还能够动态地发现和采集容器内部的日志文件。

针对前面提出的日志采集难题，Log-pilot通过声明式配置实现强大的容器事件管理，可同时获取容器标准输出和内部文件日志，解决了动态伸缩问题，此外，Log-pilot具有自动发现机制、CheckPoint及句柄保持的机制、自动日志数据打标、有效应对动态配置、日志重复和丢失以及日志源标记等问题。

本质

通过变量和模版文件生产日志收集配置文件，对日志进行采集。  
容器内文件日志路径需要配置emptyDir

## log-pilot.yaml

```bash
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-pilot
  labels:
    app: log-pilot
  # 设置期望部署的namespace。
  namespace: logging
spec:
  selector:
    matchLabels:
      app: log-pilot
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: log-pilot
      annotations:
        scheduler.alpha.kubernetes.io/critical-pod: ''
    spec:
      # 是否允许部署到Master节点上tolerations。
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: log-pilot
        # 版本请参考https://github.com/AliyunContainerService/log-pilot/releases。
        image: heleicool/log-pilot:7.x-filebeat
        resources:
          limits:
            memory: 500Mi
          requests:
            cpu: 200m
            memory: 200Mi
        env:
          - name: "NODE_NAME"
            valueFrom:
              fieldRef:
                fieldPath: spec.nodeName
          - name: "LOGGING_OUTPUT"
            value: "elasticsearch"
          # 请确保集群到ES网络可达。
          - name: "ELASTICSEARCH_HOSTS"
            value: "elasticsearch:9200"
          # 配置ES访问权限。
         # - name: "ELASTICSEARCH_USER"
        #    value: "{es_username}"
         # - name: "ELASTICSEARCH_PASSWORD"
         #   value: "{es_password}"
        volumeMounts:
        - name: sock
          mountPath: /var/run/docker.sock
        - name: root
          mountPath: /host
          readOnly: true
        - name: varlib
          mountPath: /var/lib/filebeat
        - name: varlog
          mountPath: /var/log/filebeat
        - name: localtime
          mountPath: /etc/localtime
          readOnly: true
        livenessProbe:
          failureThreshold: 3
          exec:
            command:
            - /pilot/healthz
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 2
        securityContext:
          capabilities:
            add:
            - SYS_ADMIN
      terminationGracePeriodSeconds: 30
      volumes:
      - name: sock
        hostPath:
          path: /var/run/docker.sock
      - name: root
        hostPath:
          path: /
      - name: varlib
        hostPath:
          path: /var/lib/filebeat
          type: DirectoryOrCreate
      - name: varlog
        hostPath:
          path: /var/log/filebeat
          type: DirectoryOrCreate
      - name: localtime
        hostPath:
          path: /etc/localtime
```

默认阿里云仓库只支持7.x以下版本es的数据写入，使用如下插件可以实现。  
git地址：https://[github](https://so.csdn.net/so/search?q=github&spm=1001.2101.3001.7020 "github").com/40kuai/log-pilot/tree/filebeat7.x  
dockerhub：heleicool/log-pilot:7.x-filebeat

![](../../image/edbed7a4e717446f90285410123ca994.png)

# 服务日志采集

创建一个标准的 Nginx 服务, 主要是 env 添加了两种,上面我们介绍过

一 是 基于 docker stdout 输出日志 \(aliyun\_logs\_catalina\)

二 是 基于 程序指定输出到指定的目录中 \(aliyun\_logs\_access\)

\( elasticsearch \)环境变量中的 name表示Index，这里name 表示 Index，这里 name表示Index，这里name 即是 catalina 和 access, 这里用于 Kibana 查询日志

##  nginx.yaml

```bash
apiVersion: apps/v1
kind: Deployment 
metadata: 
  name: nginx-dm
spec: 
  replicas: 3
  selector:
    matchLabels:
      name: nginx
  template: 
    metadata: 
      labels: 
        name: nginx 
    spec: 
      tolerations:
        - key: "node-role.kubernetes.io/master"
          effect: "NoSchedule"
      containers: 
        - name: nginx 
          image: nginx:alpine 
          imagePullPolicy: IfNotPresent
          env:
           - name: aliyun_logs_nginx-log
             value: "stdout"
           - name: aliyun_logs_access
             value: "/var/log/nginx/*.log"
          ports:
            - containerPort: 80
              name: http
---
apiVersion: v1 
kind: Service
metadata: 
  name: nginx-svc 
spec: 
  ports: 
    - port: 80
      name: http
      targetPort: 80
      protocol: TCP 
  selector: 
    name: nginx
```

 

![](../../image/5938c75a67e6431a80d2011f1a285334.png)

![](../../image/b844431d60b440909f12fb4c68000c4f.png)

 ![](../../image/c72e1f67ca834b2890d9b0225dfe2494.png)

 

### pod.yaml

```bash
[root@master01 new]# cat pod2.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: counter
  namespace: logging  #可以添加空间名称，也会收集到的
spec:
  containers:
  - name: count
    image: busybox
    args: [/bin/sh, -c,
            'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']
    env:
    # 1、stdout为约定关键字，表示采集标准输出日志。
    # 2、配置标准输出日志采集到ES的catalina索引下。
    - name: aliyun_logs_catalina
      value: "stdout"
    # 1、配置采集容器内文件日志，支持通配符。
    # 2、配置该日志采集到ES的access索引下。
```

### tomcat.yaml

```bash
apiVersion: v1
kind: Pod
metadata:
  name: tomcat
spec:
  containers:
  - name: tomcat
    image: "tomcat:7.0"
    env:
    # 1、stdout为约定关键字，表示采集标准输出日志。
    # 2、配置标准输出日志采集到ES的catalina索引下。
    - name: aliyun_logs_catalina
      value: "stdout"
    # 1、配置采集容器内文件日志，支持通配符。
    # 2、配置该日志采集到ES的access索引下。
    - name: aliyun_logs_access
      value: "/usr/local/tomcat/logs/catalina.*.log"
    # 容器内文件日志路径需要配置emptyDir。
    volumeMounts:
      - name: tomcat-log
        mountPath: /usr/local/tomcat/logs
  volumes:
    - name: tomcat-log
      emptyDir: {}
```

 [k8s 部署 log-pilot 收集容器标准输出日志和指定路径应用日志 \- lixinliang \- 博客园](https://www.cnblogs.com/lixinliang/p/14519118.html "k8s 部署 log-pilot 收集容器标准输出日志和指定路径应用日志 \- lixinliang \- 博客园")