---
author: 南宫乘风
categories:
- Prometheus监控
date: 2024-03-04 11:44:38
description: 推荐多集群监控使用，其主要原因是基于的分层联邦。通过部署到每个集群中的实例作为初始收集器，然后将数据聚合到网格层次的实例上。网格层次的既可以部署在网格之外外部，也可以部署在网格内的集群中。使用以及进行。。。。。。。
image: ../../title_pic/51.jpg
slug: '202403041144'
tags:
- prometheus
- istio
- 云原生
title: Kube-Prometheus 监控Istio
---

<!--more-->

推荐 Istio 多集群监控使用 Prometheus，其主要原因是基于 Prometheus 的[分层联邦](https://prometheus.io/docs/prometheus/latest/federation/#hierarchical-federation)（Hierarchical Federation）。

通过 Istio 部署到每个集群中的 Prometheus 实例作为初始收集器，然后将数据聚合到网格层次的 Prometheus 实例上。 网格层次的 Prometheus 既可以部署在网格之外（外部），也可以部署在网格内的集群中。


使用 Istio 以及 Prometheus 进行生产规模的监控时推荐的方式是使用[分层联邦](https://prometheus.io/docs/prometheus/latest/federation/#hierarchical-federation)并且结合一组[记录规则](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)。

尽管安装 Istio 不会默认部署 [Prometheus](http://prometheus.io/)，[入门](https://istio.io/latest/zh/docs/setup/getting-started/)指导中 `Option 1: Quick Start` 的部署按照 [Prometheus 集成指导](https://istio.io/latest/zh/docs/ops/integrations/prometheus/)安装了 Prometheus。 此 Prometheus 部署刻意地配置了很短的保留窗口（6 小时）。此快速入门 Prometheus 部署同时也配置为从网格上运行的每一个 Envoy 代理上收集指标，同时通过一组有关它们的源的标签（`instance`、`pod` 和 `namespace`）来扩充指标
![在这里插入图片描述](../../image/4cf8db620d254e22a9cbcd3a01d057e8.png)
### 使用负载级别的聚合指标进行联邦
为了建立 Prometheus 联邦，请修改您的 Prometheus 生产部署配置来抓取 Istio Prometheus 联邦终端的指标数据。

将以下的 Job 添加到配置中：

```bash
- job_name: 'istio-prometheus'
  honor_labels: true
  metrics_path: '/federate'
  kubernetes_sd_configs:
  - role: pod
    namespaces:
      names: ['istio-system']
  metric_relabel_configs:
  - source_labels: [__name__]
    regex: 'workload:(.*)'
    target_label: __name__
    action: replace
  params:
    'match[]':
    - '{__name__=~"workload:(.*)"}'
    - '{__name__=~"pilot(.*)"}'

```

如果您使用的是 [Prometheus Operator](https://github.com/coreos/prometheus-operator)，请使用以下的配置：


**我这边就是使用 这种方式**

```bash
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-federation
  labels:
    app.kubernetes.io/name: istio-prometheus
spec:
  namespaceSelector:
    matchNames:
    - istio-system
  selector:
    matchLabels:
      app: prometheus
  endpoints:
  - interval: 30s
    scrapeTimeout: 30s
    params:
      'match[]':
      - '{__name__=~"workload:(.*)"}'
      - '{__name__=~"pilot(.*)"}'
    path: /federate
    targetPort: 9090
    honorLabels: true
    metricRelabelings:
    - sourceLabels: ["__name__"]
      regex: 'workload:(.*)'
      targetLabel: "__name__"
      action: replace

```

```bash
kubectl apply -f istio-federation.yaml -n monitoring


[root@bt ~]# kubectl get servicemonitors.monitoring.coreos.com -n monitoring  istio-federation 
NAME               AGE
istio-federation   44d


```

联邦配置的关键是首先匹配通过 Istio 部署的 Prometheus 中收集 [Istio 标准指标](https://istio.io/latest/zh/docs/reference/config/metrics/)的 Job。并且将收集到的指标重命名，方法为去除负载等级记录规则命名前缀 (`workload:`)。 这使得现有的仪表盘以及引用能够无缝地针对生产用 Prometheus 继续工作（并且不在指向 Istio 实例）。

您可以在设置联邦时包含额外的指标（例如 envoy、go 等）。

控制面指标也被生产用 Prometheus 收集并联邦。


### 配置文件监控kubernetes-istio-pods

 Prometheus 的抓取作业配置文件，怎么实现 Prometheus 如何抓取和处理与 Kubernetes Istio pods 相关的指标数据？

> 1、首先Istio内部集成安装Prometheus
>
> 2、我们可以去istio查看 人家的配置怎么写
>
> 3、根据人家的配置 ，修改一下，集成到Prometheus上

```yaml
global:
  evaluation_interval: 1m
  scrape_interval: 15s
  scrape_timeout: 10s
rule_files:
- /etc/config/recording_rules.yml
- /etc/config/alerting_rules.yml
- /etc/config/rules
- /etc/config/alerts
scrape_configs:
- job_name: prometheus
  static_configs:
  - targets:
    - localhost:9090
- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  job_name: kubernetes-apiservers
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - action: keep
    regex: default;kubernetes;https
    source_labels:
    - __meta_kubernetes_namespace
    - __meta_kubernetes_service_name
    - __meta_kubernetes_endpoint_port_name
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  job_name: kubernetes-nodes
  kubernetes_sd_configs:
  - role: node
  relabel_configs:
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - replacement: kubernetes.default.svc:443
    target_label: __address__
  - regex: (.+)
    replacement: /api/v1/nodes/$1/proxy/metrics
    source_labels:
    - __meta_kubernetes_node_name
    target_label: __metrics_path__
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  job_name: kubernetes-nodes-cadvisor
  kubernetes_sd_configs:
  - role: node
  relabel_configs:
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - replacement: kubernetes.default.svc:443
    target_label: __address__
  - regex: (.+)
    replacement: /api/v1/nodes/$1/proxy/metrics/cadvisor
    source_labels:
    - __meta_kubernetes_node_name
    target_label: __metrics_path__
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
- honor_labels: true
  job_name: kubernetes-service-endpoints
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scrape
  - action: drop
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scrape_slow
  - action: replace
    regex: (https?)
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scheme
    target_label: __scheme__
  - action: replace
    regex: (.+)
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_path
    target_label: __metrics_path__
  - action: replace
    regex: (.+?)(?::\d+)?;(\d+)
    replacement: $1:$2
    source_labels:
    - __address__
    - __meta_kubernetes_service_annotation_prometheus_io_port
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_service_annotation_prometheus_io_param_(.+)
    replacement: __param_$1
  - action: labelmap
    regex: __meta_kubernetes_service_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_service_name
    target_label: service
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_node_name
    target_label: node
- honor_labels: true
  job_name: kubernetes-service-endpoints-slow
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scrape_slow
  - action: replace
    regex: (https?)
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scheme
    target_label: __scheme__
  - action: replace
    regex: (.+)
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_path
    target_label: __metrics_path__
  - action: replace
    regex: (.+?)(?::\d+)?;(\d+)
    replacement: $1:$2
    source_labels:
    - __address__
    - __meta_kubernetes_service_annotation_prometheus_io_port
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_service_annotation_prometheus_io_param_(.+)
    replacement: __param_$1
  - action: labelmap
    regex: __meta_kubernetes_service_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_service_name
    target_label: service
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_node_name
    target_label: node
  scrape_interval: 5m
  scrape_timeout: 30s
- honor_labels: true
  job_name: prometheus-pushgateway
  kubernetes_sd_configs:
  - role: service
  relabel_configs:
  - action: keep
    regex: pushgateway
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_probe
- honor_labels: true
  job_name: kubernetes-services
  kubernetes_sd_configs:
  - role: service
  metrics_path: /probe
  params:
    module:
    - http_2xx
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_probe
  - source_labels:
    - __address__
    target_label: __param_target
  - replacement: blackbox
    target_label: __address__
  - source_labels:
    - __param_target
    target_label: instance
  - action: labelmap
    regex: __meta_kubernetes_service_label_(.+)
  - source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - source_labels:
    - __meta_kubernetes_service_name
    target_label: service
- honor_labels: true
  job_name: kubernetes-pods
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scrape
  - action: drop
    regex: true
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scrape_slow
  - action: replace
    regex: (https?)
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scheme
    target_label: __scheme__
  - action: replace
    regex: (.+)
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_path
    target_label: __metrics_path__
  - action: replace
    regex: (\d+);(([A-Fa-f0-9]{1,4}::?){1,7}[A-Fa-f0-9]{1,4})
    replacement: '[$2]:$1'
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_port
    - __meta_kubernetes_pod_ip
    target_label: __address__
  - action: replace
    regex: (\d+);((([0-9]+?)(\.|$)){4})
    replacement: $2:$1
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_port
    - __meta_kubernetes_pod_ip
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)
    replacement: __param_$1
  - action: labelmap
    regex: __meta_kubernetes_pod_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  - action: drop
    regex: Pending|Succeeded|Failed|Completed
    source_labels:
    - __meta_kubernetes_pod_phase
- honor_labels: true
  job_name: kubernetes-pods-slow
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scrape_slow
  - action: replace
    regex: (https?)
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scheme
    target_label: __scheme__
  - action: replace
    regex: (.+)
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_path
    target_label: __metrics_path__
  - action: replace
    regex: (\d+);(([A-Fa-f0-9]{1,4}::?){1,7}[A-Fa-f0-9]{1,4})
    replacement: '[$2]:$1'
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_port
    - __meta_kubernetes_pod_ip
    target_label: __address__
  - action: replace
    regex: (\d+);((([0-9]+?)(\.|$)){4})
    replacement: $2:$1
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_port
    - __meta_kubernetes_pod_ip
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)
    replacement: __param_$1
  - action: labelmap
    regex: __meta_kubernetes_pod_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  - action: drop
    regex: Pending|Succeeded|Failed|Completed
    source_labels:
    - __meta_kubernetes_pod_phase
  scrape_interval: 5m
  scrape_timeout: 30s

```

![在这里插入图片描述](../../image/1c4899a176854b5981aee33c6bd97633.png)



上面是人家的写的配置，修改配置为下方

在`prometheus-prometheus.yaml`的配置文件中，官方内置了一个字段`additionalScrapeConfigs`用于添加自定义的抓取目标

[https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/api.md#PrometheusSpec](https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/api.md#PrometheusSpec)

所以只需要按照官方的要求写入配置即可。新建额外抓取的信息`prometheus-additional.yaml`：

`prometheus-additional.yaml`

```bash
- job_name: kubernetes-istio-pods
  honor_labels: true
  honor_timestamps: true
  scrape_interval: 15s
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  follow_redirects: true
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    separator: ;
    regex: "true"
    replacement: $1
    action: keep
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape_slow]
    separator: ;
    regex: "true"
    replacement: $1
    action: drop
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scheme]
    separator: ;
    regex: (https?)
    target_label: __scheme__
    replacement: $1
    action: replace
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    separator: ;
    regex: (.+)
    target_label: __metrics_path__
    replacement: $1
    action: replace
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port, __meta_kubernetes_pod_ip]
    separator: ;
    regex: (\d+);(([A-Fa-f0-9]{1,4}::?){1,7}[A-Fa-f0-9]{1,4})
    target_label: __address__
    replacement: '[$2]:$1'
    action: replace
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port, __meta_kubernetes_pod_ip]
    separator: ;
    regex: (\d+);((([0-9]+?)(\.|$)){4})
    target_label: __address__
    replacement: $2:$1
    action: replace
  - separator: ;
    regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)
    replacement: __param_$1
    action: labelmap
  - separator: ;
    regex: __meta_kubernetes_pod_label_(.+)
    replacement: $1
    action: labelmap
  - source_labels: [__meta_kubernetes_namespace]
    separator: ;
    regex: (.*)
    target_label: namespace
    replacement: $1
    action: replace
  - source_labels: [__meta_kubernetes_pod_name]
    separator: ;
    regex: (.*)
    target_label: pod
    replacement: $1
    action: replace
  - source_labels: [__meta_kubernetes_pod_phase]
    separator: ;
    regex: Pending|Succeeded|Failed|Completed
    replacement: $1
    action: drop
  kubernetes_sd_configs:
  - role: pod
    kubeconfig_file: ""
    follow_redirects: true

```

抓取的目标制定为targets列表，创建secret对象`istio-additional-configs`引用该配置

```bash
kubectl create secret generic `istio-additional-configs` --from-file=./prometheus-additional.yaml -n monitoring
```

```bash
kubectl edit prometheus -n monitoring

spec:
  additionalScrapeConfigs:
    key: prometheus-additional.yaml
    name: istio-additional-configs

```
![在这里插入图片描述](../../image/1ffeb004ffb84b58ad78eb7e703ae2e2.png)
或者

在`promethes-prometheus.yaml`中添加`additionalScrapeConfigs`引用创建的secret

```bash
serviceAccountName: prometheus-k8s
   serviceMonitorNamespaceSelector: {}
   serviceMonitorSelector: {}
   version: v2.11.0
   additionalScrapeConfigs:
     name: ingress-nginx-additional-configs
     key: prometheus-additional.yaml
```

重建promethes配置:

```bash
$ kubectl delete -f ./prometheus-prometheus.yaml && kubectl apply -f ./prometheus-prometheus.yaml
```
![在这里插入图片描述](../../image/5e4d4ce274b14864a6a3a61f6d5ebd78.png)
### Grafan监控

关于Grafan的监控面板，可以去官方进行寻找

https://grafana.com/grafana/dashboards/

Istio也提供了自身平台的监控大盘，如下：
![在这里插入图片描述](../../image/3f2c4a11ba584b1f98b73d749961299c.png)
可以看出Istio的默认监控大盘非常全面，该监控的都监控起来了
![在这里插入图片描述](../../image/23de3cf54b9c462f8de2830aa2d341e3.png)
参考文档：[https://www.cnblogs.com/justmine/p/12269587.html](https://www.cnblogs.com/justmine/p/12269587.html)
