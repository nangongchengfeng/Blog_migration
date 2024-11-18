---
author: 南宫乘风
categories:
- Prometheus监控
date: 2021-03-18 22:21:16
description: 黑盒测试这次使用基于黑盒测试上面。用来收集监控的数据、创建官网地址：这里我们监控百度网站测试、修改的、测试验证。。。。。。。
image: ../../title_pic/43.jpg
slug: '202103182221'
tags:
- Kubernetes
- ''
- Kubernetes应用
- kubernetes
- 百度
- docker
- centos
title: Prometheus_additional传统配置
---

<!--more-->

# [prometheus黑盒测试](https://blog.csdn.net/heian_99/article/details/114984598)

这次使用基于黑盒测试上面。用来收集监控blackbox的数据

<https://github.com/prometheus/blackbox_exporter>

<https://github.com/prometheus/blackbox_exporter/blob/master/blackbox.yml>

<https://grafana.com/grafana/dashboards/5345>

### 1、创建secrets

官网地址：<https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/additional-scrape-config.md>

```bash
cat prometheus-additional.yaml

- job_name: 'blackbox'
  metrics_path: /probe
  params:
    module: [http_2xx]  # Look for a HTTP 200 response.
  static_configs:
    - targets:
      - http://www.baidu.com	  # 这里我们监控百度网站测试
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: blackbox-exporter:9115  # The blackbox exporter's real hostname:port.
```

```bash
kubectl create secret generic additional-scrape-configs --from-file=prometheus-additional.yaml --dry-run -oyaml > additional-scrape-configs.yaml

kubectl apply -f additional-scrape-configs.yaml -n monitoring 

```

![](../../image/20210318213322402.png)

### 2、修改Prometheus的CRD

 

```
[root@k8s-master01 manifests]# vim prometheus-prometheus.yaml 

apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  labels:
    prometheus: k8s
spec:
  alerting:
    alertmanagers:
    - name: alertmanager-main
      namespace: monitoring
      port: web
  image: quay.io/prometheus/prometheus:v2.15.2
  nodeSelector:
    kubernetes.io/os: linux
  podMonitorNamespaceSelector: {}
  podMonitorSelector: {}
  replicas: 1
  resources:
    requests:
      memory: 700Mi
  ruleSelector:
    matchLabels:
      prometheus: k8s
      role: alert-rules
  securityContext:
    fsGroup: 2000
    runAsNonRoot: true
    runAsUser: 1000
  serviceAccountName: prometheus-k8s
  serviceMonitorNamespaceSelector: {}
  serviceMonitorSelector: {}
  version: v2.15.2
  additionalScrapeConfigs:
    name: additional-scrape-configs
    key: prometheus-additional.yaml

[root@k8s-master01 manifests]# kubectl replace -f prometheus-prometheus.yaml 
prometheus.monitoring.coreos.com/k8s replaced



```

### 3、Prometheus测试验证

![](../../image/20210318220434421.png)

![](../../image/20210318220344134.png)

![](../../image/20210318220937701.png)