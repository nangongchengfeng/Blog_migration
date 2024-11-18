---
author: 南宫乘风
categories:
- Prometheus监控
date: 2023-11-28 15:17:01
description: 、简介在现代的环境中，对于服务器和网络设备的监控是至关重要的。群辉作为一种流行的网络存储解决方案，为用户提供了高性能和可靠的存储服务。然而，了解设备的运行状况和性能指标对于确保其正常运行和及时采取措施。。。。。。。
image: ../../title_pic/14.jpg
slug: '202311281517'
tags:
- prometheus
title: 使用Prometheus监控Synology（群辉）
---

<!--more-->

## 1、简介
在现代的IT环境中，对于服务器和网络设备的监控是至关重要的。Synology（群辉）作为一种流行的网络存储解决方案，为用户提供了高性能和可靠的存储服务。然而，了解Synology设备的运行状况和性能指标对于确保其正常运行和及时采取措施至关重要。

Prometheus是一个功能强大的开源监控系统，它提供了灵活的数据模型和丰富的查询语言，可用于收集、存储和可视化各种应用程序和设备的监控指标。通过将Prometheus与Synology（群辉）集成，您可以实时监控Synology（Snmp协议）设备的关键指标，如CPU使用率、内存使用率、磁盘空间、网络流量等，以便及时发现问题并采取适当的措施。
![在这里插入图片描述](../../image/5b51e8c475bc46c09588bbf3921911f2.png)

## 2、环境准备

> Synology（群辉）：7.2 .1 
> prometheus：2.48.0
>  Grafan ：10
>  Snmp_exporter: 0.22.0 (注意版本：新版本配置变更)
>  
Snmp版本问题：https://github.com/prometheus/snmp_exporter/blob/main/auth-split-migration.md
从snmp_exporter v0.23.0 版本开始，配置文件格式snmp_exporter已更改。v0.22.0 及之前版本的配置文件将不起作用
![在这里插入图片描述](../../image/05d89f5b95a54fb9ada55359c1c88d01.png)
## 3、Synology配置

### 1、开启SNMP协议
![在这里插入图片描述](../../image/742f1f07dd2446aa9cbca8f3b1540d85.png)
### 2、安装Docker
在套件中心，直接搜索 “docker” 进行安装
7.0 和 6.0 的版本不一样
7.0
![在这里插入图片描述](../../image/d962481c880942ad96e16c31ed7792dd.png)
### 3、Node-Exporter 安装
 Node-Exporter 是监控 Synology的底层系统，相当于Linux操作系统， 这个可以使用docker的镜像安装，不过这里 大佬已经封装好插件，直接使用。
 **添加源**
 ```bash
 https://spk7.imnks.com/
 http://spk.bobohome.store:8880
```
![在这里插入图片描述](../../image/b7f02afed97b419083dc0cf17a2b5d86.png)
![在这里插入图片描述](../../image/aa86ea06d35a4dbb9628b525d6bb78ce.png)
## 4、Docker安装组件
参考： https://github.com/ddiiwoong/synology-prometheus
Docker目录下，创建monitor目录，后续的配置存放里面
![在这里插入图片描述](../../image/7d1fcd84f17047ed90d65871d6636fd6.png)

### 1、Snmp_exporter 安装
我使用dockerfile 进行安装
snmp的文件：https://github.com/ddiiwoong/synology-prometheus/blob/master/snmp-synology/snmp.yml

```bash
version: "3.8"
services:
  snmp-exporter:
    image: ricardbejarano/snmp_exporter:0.22.0
    container_name: snmp_exporter
    volumes:
      - ./snmp-synology/snmp.yml:/etc/snmp_exporter/snmp.yml
    ports:
      - 9116:9116
    command:
      - "--config.file=/etc/snmp_exporter/snmp.yml"
```
启动成功
![在这里插入图片描述](../../image/c2d1ac6640ad42f4a61c2383e7e01dd4.png)
测试
![在这里插入图片描述](../../image/45585d0a0f5c487199d14ae6f5ceba88.png)

![在这里插入图片描述](../../image/66241a98926a45169f2c1b3982cc308d.png)
### 2、Prometheus安装
这次我才用ssh到nas系统，直接执行命令进行创建
**prometheus.yml 配置文件**
```bash
global:
  scrape_interval:     15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
  - static_configs:
    - targets: ['alertmanager:9093']

rule_files:
  - "/etc/prometheus/rules/*"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
        labels:
          group: 'prometheus'
  - job_name: node
    static_configs:
    - targets: ['192.168.123.200:9100']
  - job_name: 'snmp'
    metrics_path: /snmp
    static_configs:
      - targets:
        - 192.168.123.200
    params:
      module: [synology]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 192.168.123.200:9116
```
放到指定位置,然后创建prometheus
```bash
docker run -d  -p 9090:9090 -u root \
  -v /volume1/docker/monitor/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v /volume1/docker/monitor/prometheus/rules:/etc/prometheus/rules \
  -v /volume1/docker/monitor/prometheus/data:/etc/prometheus/data \
  --name prometheus \
  prom/prometheus:latest \
  --storage.tsdb.path=/etc/prometheus/data \
  --storage.tsdb.retention.time=90d \
  --config.file=/etc/prometheus/prometheus.yml
```
![在这里插入图片描述](../../image/f3c148925f1441afa585db5e569693c1.png)
### 3、Grafan安装
参考文档：https://blog.csdn.net/wayne_primes/article/details/112467639
```bash
docker run \
-d --name grafana  -p 3000:3000 \
grafana/grafana grafana

将配置文件拷贝至宿主机方便修改配置
docker exec -it grafana cat /etc/grafana/grafana.ini > /data/grafana/grafana.ini

mkdir -p /data/grafana/data
#修改目录权限否则启动后容器中用户无法创建数据文件夹和文件
chmod 777  /data/grafana/data

```
Grafan创建命令
```bash
docker run  -d -p 3000:3000 -u root \
--name grafana \
-e "GF_SECURITY_ADMIN_PASSWORD=admin" \
-v "/volume1/docker/monitor/grafana/grafana.ini:/etc/grafana/grafana.ini" \
-v "/volume1/docker/monitor/grafana/data/:/var/lib/grafana" \
$(cat /etc/hosts |grep -Ev "^$|[#;]" | awk -F ' ' '{if(NR>2){print "--add-host "$2":"$1}}')  \
grafana/grafana grafana
```
![在这里插入图片描述](../../image/51ea3845c15e4fcc8c91d77da0932e1e.png)

## 5、界面展示
### 1、添加数据源
![在这里插入图片描述](../../image/3efdf8d0c5d848ec8f48850ee73fe949.png)
### 2、导入大屏展示
ID：
Linux：8919
群辉：14284  14364

![在这里插入图片描述](../../image/7557166a8117400db73044fe8a157c56.png)

![在这里插入图片描述](../../image/c58313ddcd264e2490310abcd522d8f0.png)



