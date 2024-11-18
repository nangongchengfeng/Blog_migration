---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-18 18:01:08
description: 白盒监控：监控一些内部的数据，的监控数据，的大小。内部暴露的指标被称为白盒监控。比较关注的是原因。黑盒监控：站在用户的角度看到的东西。网站不能打开，网站打开的比较慢。比较关注现象，表示正在发生的问题，。。。。。。。
image: http://image.ownit.top/4kdongman/16.jpg
tags:
- Prometheus监控
- ''
- Kubernetes应用
- kubernetes
- 监控类
- 黑盒测试
- docker
- centos
title: prometheus黑盒测试
---

<!--more-->

白盒监控：监控一些内部的数据，topic的监控数据，Redis key的大小。内部暴露的指标被称为白盒监控。比较关注的是原因。

 

黑盒监控：站在用户的角度看到的东西。网站不能打开，网站打开的比较慢。比较关注现象，表示正在发生的问题，正在发生的告警。

github文档：<https://github.com/prometheus/blackbox_exporter>

关于部署，已经做成yaml格式，一键部署上去就可以了

创建comfingmap   \---》 挂载到deployments  \--》暴露service服务使用

 

```bash
[root@k8s-master01 config]# cat exe.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: blackbox-exporter
  name: blackbox-exporter
  namespace: monitoring
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: blackbox-exporter
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: blackbox-exporter
    spec:
      containers:
      - args:
        - --config.file=/mnt/blackbox.yml
        env:
        - name: TZ
          value: Asia/Shanghai
        - name: LANG
          value: C.UTF-8
        image: prom/blackbox-exporter:master
        imagePullPolicy: IfNotPresent
        lifecycle: {}
        name: blackbox-exporter
        ports:
        - containerPort: 9115
          name: web
          protocol: TCP
        resources:
          limits:
            cpu: 324m
            memory: 443Mi
          requests:
            cpu: 10m
            memory: 10Mi
        securityContext:
          allowPrivilegeEscalation: false
          privileged: false
          readOnlyRootFilesystem: false
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
          name: config
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
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
          name: blackbox-conf
        name: config
---
apiVersion: v1
data:
  blackbox.yml: |-
    modules:
      http_2xx:
        prober: http
      http_post_2xx:
        prober: http
        http:
          method: POST
      tcp_connect:
        prober: tcp
      pop3s_banner:
        prober: tcp
        tcp:
          query_response:
          - expect: "^+OK"
          tls: true
          tls_config:
            insecure_skip_verify: false
      ssh_banner:
        prober: tcp
        tcp:
          query_response:
          - expect: "^SSH-2.0-"
      irc_banner:
        prober: tcp
        tcp:
          query_response:
          - send: "NICK prober"
          - send: "USER prober prober prober :prober"
          - expect: "PING :([^ ]+)"
            send: "PONG ${1}"
          - expect: "^:[^ ]+ 001"
      icmp:
        prober: icmp
kind: ConfigMap
metadata:
  name: blackbox-conf
  namespace: monitoring
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: blackbox-exporter
  name: blackbox-exporter
  namespace: monitoring
spec:
  ports:
  - name: container-1-web-1
    port: 9115
    protocol: TCP
    targetPort: 9115
  selector:
    app: blackbox-exporter
  sessionAffinity: None
  type: ClusterIP
```

测试验证

```bash
 curl http://10.96.203.216:9115/probe?target=www.baidu.com&module=http_2xx
```

```
[root@k8s-master01 config]# curl http://10.96.203.216:9115/probe?target=www.baidu.com&module=http_2xx 
[1] 4221
#获取baidu.com的相关信息
[root@k8s-master01 config]# # HELP probe_dns_lookup_time_seconds Returns the time taken for probe dns lookup in seconds
# TYPE probe_dns_lookup_time_seconds gauge
probe_dns_lookup_time_seconds 0.338946599
# HELP probe_duration_seconds Returns how long the probe took to complete in seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds 0.682111152
# HELP probe_failed_due_to_regex Indicates if probe failed due to regex
# TYPE probe_failed_due_to_regex gauge
probe_failed_due_to_regex 0
# HELP probe_http_content_length Length of http content response
# TYPE probe_http_content_length gauge
probe_http_content_length -1
# HELP probe_http_duration_seconds Duration of http request by phase, summed over all redirects
# TYPE probe_http_duration_seconds gauge
probe_http_duration_seconds{phase="connect"} 0.00913168
probe_http_duration_seconds{phase="processing"} 0.008949937
probe_http_duration_seconds{phase="resolve"} 0.338946599
probe_http_duration_seconds{phase="tls"} 0
probe_http_duration_seconds{phase="transfer"} 0.324605594
# HELP probe_http_redirects The number of redirects
# TYPE probe_http_redirects gauge
probe_http_redirects 0
# HELP probe_http_ssl Indicates if SSL was used for the final redirect
# TYPE probe_http_ssl gauge
probe_http_ssl 0
# HELP probe_http_status_code Response HTTP status code
# TYPE probe_http_status_code gauge
probe_http_status_code 200
# HELP probe_http_uncompressed_body_length Length of uncompressed response body
# TYPE probe_http_uncompressed_body_length gauge
probe_http_uncompressed_body_length 297140
# HELP probe_http_version Returns the version of HTTP of the probe response
# TYPE probe_http_version gauge
probe_http_version 1.1
# HELP probe_ip_addr_hash Specifies the hash of IP address. It's useful to detect if the IP address changes.
# TYPE probe_ip_addr_hash gauge
probe_ip_addr_hash 2.882632397e+09
# HELP probe_ip_protocol Specifies whether probe ip protocol is IP4 or IP6
# TYPE probe_ip_protocol gauge
probe_ip_protocol 4
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 1
```