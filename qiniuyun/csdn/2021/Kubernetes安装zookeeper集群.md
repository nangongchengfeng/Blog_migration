---
author: 南宫乘风
categories:
- Kubernetes应用
date: 2021-10-14 18:07:59
description: 业务要求，近期集群要使用集群，准备在实现。方法一：使用和来挂载这个同时创建和方法二。。。。。。。
image: ../../title_pic/65.jpg
slug: '202110141807'
tags:
- zookeeper
- java
- Kubernetes
title: Kubernetes安装zookeeper集群
---

<!--more-->

业务要求，近期集群要使用zookeeper集群，准备在Kubernetes实现。

## 方法一：

使用pv和pvc 来挂载

这个同时创建pv和pvc

```bash
[root@k8s-master k8s-yaml]# cat zookeeper-pv.yaml 
apiVersion: v1
kind: PersistentVolume
metadata: 
  name: zk-01
  labels:
    name: zk-cluster
    type: nfs
spec:
  nfs:
    path: /home/installapp/nfs/data/zk-01
    server: 192.168.1.210
  accessModes: 
  - "ReadWriteOnce"
  capacity:
    storage: 1Gi
  persistentVolumeReclaimPolicy: Recycle
---
apiVersion: v1
kind: PersistentVolume
metadata: 
  name: zk-02
  labels:
    name: zk-cluster
    type: nfs
spec:
  nfs:
    path: /home/installapp/nfs/data/zk-02
    server: 192.168.1.210
  accessModes: 
  - "ReadWriteOnce"
  capacity:
    storage: 1Gi
  persistentVolumeReclaimPolicy: Recycle
---
apiVersion: v1
kind: PersistentVolume
metadata: 
  name: zk-03
  labels:
    name: zk-cluster
    type: nfs
spec:
  nfs:
    path: /home/installapp/nfs/data/zk-03
    server: 192.168.1.210
  accessModes: 
  - "ReadWriteOnce"
  capacity:
    storage: 1Gi
  persistentVolumeReclaimPolicy: Recycle
```

```bash
[root@k8s-master k8s-yaml]# cat statefulset-zk.yaml 
apiVersion: v1
kind: Service
metadata:
  name: zk-hs
  labels:
    app: zk
spec:
  ports:
  - port: 2888
    name: server
  - port: 3888
    name: leader-election
  clusterIP: None
  selector:
    app: zk
---
apiVersion: v1
kind: Service
metadata:
  name: zk-cs
  labels:
    app: zk
spec:
  ports:
  - port: 2181
    name: client
  selector:
    app: zk
---
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  name: zk-pdb
spec:
  selector:
    matchLabels:
      app: zk
  maxUnavailable: 1
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: zk
spec:
  selector:
    matchLabels:
      app: zk
  serviceName: zk-hs
  replicas: 3
  updateStrategy:
    type: RollingUpdate
  podManagementPolicy: OrderedReady
  template:
    metadata:
      labels:
        app: zk
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: "app"
                    operator: In
                    values:
                    - zk
              topologyKey: "kubernetes.io/hostname"
      containers:
      - name: kubernetes-zookeeper
        imagePullPolicy: IfNotPresent
        image: k8s.gcr.io/kubernetes-zookeeper:1.0-3.4.10
        resources:
          requests:
            memory: "1Gi"
            cpu: "0.5"
        ports:
        - containerPort: 2181
          name: client
        - containerPort: 2888
          name: server
        - containerPort: 3888
          name: leader-election
        command:
        - sh
        - -c
        - "start-zookeeper \
          --servers=3 \
          --data_dir=/var/lib/zookeeper/data \
          --data_log_dir=/var/lib/zookeeper/data/log \
          --conf_dir=/opt/zookeeper/conf \
          --client_port=2181 \
          --election_port=3888 \
          --server_port=2888 \
          --tick_time=2000 \
          --init_limit=10 \
          --sync_limit=5 \
          --heap=512M \
          --max_client_cnxns=60 \
          --snap_retain_count=3 \
          --purge_interval=12 \
          --max_session_timeout=40000 \
          --min_session_timeout=4000 \
          --log_level=INFO"
        readinessProbe:
          exec:
            command:
            - sh
            - -c
            - "zookeeper-ready 2181"
          initialDelaySeconds: 10
          timeoutSeconds: 5
        livenessProbe:
          exec:
            command:
            - sh
            - -c
            - "zookeeper-ready 2181"
          initialDelaySeconds: 10
          timeoutSeconds: 5
        volumeMounts:
        - name: datadir
          mountPath: /var/lib/zookeeper
      securityContext:
        # runAsUser: 1000
        fsGroup: 1000
  volumeClaimTemplates:
  - metadata:
      name: datadir
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

## 方法二

```bash
apiVersion: v1
kind: Service
metadata:
  name: zk-hs
  namespace: uat
  labels:
    app: zk
spec:
  ports:
  - port: 2888
    name: server
  - port: 3888
    name: leader-election
  clusterIP: None
  selector:
    app: zk
---
apiVersion: v1
kind: Service
metadata:
  name: zk-cs
  namespace: uat
  labels:
    app: zk
spec:
  ports:
  - port: 2181
    name: client
  selector:
    app: zk
---
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  name: zk-pdb
  namespace: uat
spec:
  selector:
    matchLabels:
      app: zk
  maxUnavailable: 1
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: zk
  namespace: uat
spec:
  selector:
    matchLabels:
      app: zk
  serviceName: zk-hs
  replicas: 3
  updateStrategy:
    type: RollingUpdate
  podManagementPolicy: OrderedReady
  template:
    metadata:
      labels:
        app: zk
    spec:
      nodeSelector:
        env: uat
      containers:
      - name: kubernetes-zookeeper
        imagePullPolicy: IfNotPresent
        image: k8s.gcr.io/kubernetes-zookeeper:1.0-3.4.10
        resources:
          requests:
            memory: "1Gi"
            cpu: "0.5"
        ports:
        - containerPort: 2181
          name: client
        - containerPort: 2888
          name: server
        - containerPort: 3888
          name: leader-election
        command:
        - sh
        - -c
        - "start-zookeeper \
          --servers=3 \
          --data_dir=/var/lib/zookeeper/data/${HOSTNAME} \
          --data_log_dir=/var/lib/zookeeper/data/${HOSTNAME}/log \
          --conf_dir=/opt/zookeeper/conf \
          --client_port=2181 \
          --election_port=3888 \
          --server_port=2888 \
          --tick_time=2000 \
          --init_limit=10 \
          --sync_limit=5 \
          --heap=512M \
          --max_client_cnxns=60 \
          --snap_retain_count=3 \
          --purge_interval=12 \
          --max_session_timeout=40000 \
          --min_session_timeout=4000 \
          --log_level=INFO"
        readinessProbe:
          exec:
            command:
            - sh
            - -c
            - "zookeeper-ready 2181"
          initialDelaySeconds: 10
          timeoutSeconds: 5
        livenessProbe:
          exec:
            command:
            - sh
            - -c
            - "zookeeper-ready 2181"
          initialDelaySeconds: 10
          timeoutSeconds: 5
        volumeMounts:
          - name: datadir
            mountPath: /var/lib/zookeeper
          - name: host-time
            mountPath: /etc/localtime
#      securityContext:
#        runAsUser: 0
#        fsGroup: 0
      volumes:
      - name: datadir
        hostPath:
          path: /store/logs/uat/zk
          type: DirectoryOrCreate
      - name: host-time
        hostPath:
          path: /etc/localtime
```