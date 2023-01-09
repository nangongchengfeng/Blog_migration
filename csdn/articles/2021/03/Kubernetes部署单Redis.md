+++
author = "南宫乘风"
title = "Kubernetes部署单Redis"
date = "2021-03-09 10:36:44"
tags=['docker', 'kubernetes', '中间件', 'redis']
categories=['Kubernetes', ' Kubernetes应用']
image = "post/4kdongman/29.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/114556056](https://blog.csdn.net/heian_99/article/details/114556056)

Kubernetes集群中，我们时常要部署中间件，nginx，redis等等

首先，这些中间件要容器化，才可以部署到Kubernetes集群中。

（1）一般我们到dockerhub官方，寻找镜像  [https://hub.docker.com/search?q=redis&amp;type=image](https://hub.docker.com/search?q=redis&amp;type=image)

（2）我们可以自己定制，，公司需要的docker 镜像

部署单个Redis

### （1）首先下载redis的镜像（版本：）

```
docker pull redis:5.0.4-alpine
```

### （2）编写configmap

因为需要指定命名空间 redis-node

```
kubectl create cm redis-node
```

```
apiVersion: v1
data:
  redis.conf: |-
    #heian
    bind 0.0.0.0
    protected-mode yes
    port 6379
    tcp-backlog 511
    timeout 0
    tcp-keepalive 300
    daemonize no
    supervised no
    pidfile /var/run/redis_6379.pid
    loglevel notice
    logfile /var/log/redis.log
    databases 16
    save 900 1
    save 300 10
    save 60 10000
    stop-writes-on-bgsave-error yes
    rdbcompression yes
    rdbchecksum yes
    dbfilename dump.rdb
    dir /data
    slave-serve-stale-data yes
    slave-read-only yes
    repl-diskless-sync no
    repl-diskless-sync-delay 5
    repl-disable-tcp-nodelay no
    slave-priority 100
    appendonly no
    appendfilename "appendonly.aof"
    appendfsync everysec
    no-appendfsync-on-rewrite no
    auto-aof-rewrite-percentage 100
    auto-aof-rewrite-min-size 64mb
    aof-load-truncated yes
    lua-time-limit 5000
    slowlog-log-slower-than 10000
    slowlog-max-len 128
    latency-monitor-threshold 0
    notify-keyspace-events ""
    hash-max-ziplist-entries 512
    hash-max-ziplist-value 64
    list-max-ziplist-size -2
    list-compress-depth 0
    set-max-intset-entries 512
    zset-max-ziplist-entries 128
    zset-max-ziplist-value 64
    hll-sparse-max-bytes 3000
    activerehashing yes
    client-output-buffer-limit normal 0 0 0
    client-output-buffer-limit slave 256mb 64mb 60
    client-output-buffer-limit pubsub 32mb 8mb 60
    hz 10
    aof-rewrite-incremental-fsync yes
kind: ConfigMap
metadata:
  name: redis-conf
  namespace: redis-node
```

### (3)编写单个redis的yaml文件

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: redis-single-node
  name: redis-single-node
  namespace: redis-node
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: redis-single-node
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: redis-single-node
    spec:
      containers:
      - command:
        - sh
        - -c
        - redis-server "/mnt/redis.conf"
        env:
        - name: TZ
          value: Asia/Shanghai
        - name: LANG
          value: C.UTF-8
        image: redis:5.0.4-alpine
        imagePullPolicy: IfNotPresent
        lifecycle: {}
        livenessProbe:
          failureThreshold: 2
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          tcpSocket:
            port: 6379
          timeoutSeconds: 2
        name: redis-single-node
        ports:
        - containerPort: 6379
          name: web
          protocol: TCP
        readinessProbe:
          failureThreshold: 2
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          tcpSocket:
            port: 6379
          timeoutSeconds: 2
        resources:
          limits:
            cpu: 100m
            memory: 339Mi
          requests:
            cpu: 10m
            memory: 10Mi
        securityContext:
          privileged: false
          runAsNonRoot: false
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /usr/share/zoneinfo/Asia/Shanghai
          name: tz-config
        - mountPath: /etc/localtime
          name: tz-config
        - mountPath: /etc/timezone
          name: timezone
        - mountPath: /mnt
          name: redis-conf
          readOnly: true
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 30
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 30
      volumes:
      - hostPath:
          path: /usr/share/zoneinfo/Asia/Shanghai
          type: ""
        name: tz-config
      - hostPath:
          path: /etc/timezone
          type: ""
        name: timezone
      - configMap:
          defaultMode: 420
          name: redis-conf
        name: redis-conf

```

因为修改configmap，不会自动更新，需要删除容器才会重新加载。我这边尝试挂载configmap为文件，指定启动配置文件

![2021030910361041.png](https://img-blog.csdnimg.cn/2021030910361041.png)

### (4)暴露端口，service

这边我做了service暴露。用的ClusterIP，接下来可以通过ingress包这个ip通过域名映射出去

```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: redis-single-node
spec:
  ports:
  - name: redis-port
    port: 6379
    protocol: TCP
    targetPort: 6379
  selector:
    app: redis-single-node
  sessionAffinity: None
  type: ClusterIP
```

![20210309105037391.png](https://img-blog.csdnimg.cn/20210309105037391.png)
