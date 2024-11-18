---
author: 南宫乘风
categories:
- Prometheus监控
date: 2021-09-12 12:51:59
description: 以下是生产环境中告警规则用例默认的是格式的，无法知道主机名。方法一：获取参考链接：主机名在指标中，且的值恰巧为，所以我们可以在中通过提取，只需要在原有后添加这样，在告警的中，就可以通过获取主机名了特别。。。。。。。
image: ../../title_pic/04.jpg
slug: '202109121251'
tags:
- prometheus
- 警报
- 别名
title: Prometheus监控，生产可用告警规则（可获取主机名）
---

<!--more-->

以下是生产环境中prometheus.rules.yml告警规则用例

prometheus默认的instance是ip:port格式的，无法知道主机名。

# 方法一：node\_uname\_info获取

参考链接：<https://blog.csdn.net/CHEndorid/article/details/106820612>

主机名（nodename）在指标node\_uname\_info中，且node\_uname\_info的值恰巧为1，所以我们可以在PromQL中通过node\_uname\_info提取，只需要在原有PromQL后添加

```bash
* on(instance) group_left(nodename) (node_uname_info)
```

这样，在prometheus告警的labels中，就可以通过nodename获取主机名了

特别的，up==0的值是0，做乘法是不会得到结果的

##   
示例：

```bash
    - alert: cpu使用率过高告警
      expr: (100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance)* 100))* on(instance) group_left(nodename) (node_uname_info) > 85
      for: 5m
      labels:
        region: 成都
      annotations:
        summary: "{{$labels.instance}}（{{$labels.nodename}}）CPU使用率过高！"
        description: '服务器{{$labels.instance}}（{{$labels.nodename}}）CPU使用率超过85%(目前使用:{{printf "%.2f" $value}}%)'
```

# 方法二：relabel\_configs增加主机名标签

此方法，可以适应所有报警的规则

在 prometheus增加主机配置是，添加配置即可

```bash
  - job_name: 'hadoop-test-exporter'
    consul_sd_configs:
    - server: 'localhost:8500'
      services: [hadoop-test-exporter]
    relabel_configs: #把__meta_consul_service_id 映射主机名
    - source_labels: [__meta_consul_service_id]
      separator: ;
      regex: (.*)
      target_label: hostname
      replacement: $1
      action: replace
    - source_labels: [__meta_consul_service_address] #映射主机IP
      separator: ;
      regex: (.*)
      target_label: ip
      replacement: $1
      action: replace
    - source_labels: ['__meta_consul_tags'] #根据tag来匹配分组
      regex: '^.*,hadoop-test,.*$'
      action: keep
```

![](../../image/20210912125024499.png)

 ![](../../image/20210912125048533.png)