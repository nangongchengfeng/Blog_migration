---
author: 南宫乘风
categories:
- Prometheus监控
date: 2021-09-12 13:02:43
description: 报警规则，是由语句编写组合的，但是有时语句会很长，我们看还好，但是有时间业务组那边也会使用来看主机偏高的指标，这边只能设置别名，方便他们使用。别名设置：很简单，也是和报警规则一样，但是语法可能不一样示。。。。。。。
image: ../../title_pic/04.jpg
slug: '202109121302'
tags:
- prometheus
- 监控
- 别名
title: Prometheus报警规则别名设置
---

<!--more-->

prometheus报警规则，是由promsql语句编写组合的，但是有时语句会很长，我们看还好，但是有时间业务组那边也会使用promsql来看主机偏高的指标，这边只能设置别名，方便他们使用。

**别名设置：**

很简单，也是和报警规则一样，但是语法可能不一样

**示例**  
 

```bash
[root@hdpv3test08 rules]# cat prometheus_rules_name.yml 
groups:
- name: alive
  rules:
  - record: node:ping:total 
    expr: up 
- name: cpu
  rules:
  - record: node:cpu_usage:ratio #别的文件使用，直接使用这个
    expr: ((100 - (avg by(instance,ip,hostname) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100))) 
- name: mem
  rules:
  - record: node:memory_usage:ratio
    expr: (100 -(node_memory_MemTotal_bytes -node_memory_MemFree_bytes+node_memory_Buffers_bytes+node_memory_Cached_bytes ) / node_memory_MemTotal_bytes * 100 )
```

node:cpu\_usage:ratio 就是查看cpu使用率的指标

下面两张图就是区别

![](../../image/20210912125819832.png)

 ![](../../image/20210912125903402.png)

 我们正常使用，就是直接采用这个别名指标了

![](../../image/20210912130017467.png)

 **业务组使用**

prometheus支持promsql语法，我们可以通过相关语句，很快定位到集群，资源使用情况

如：高CPU 高内存，出入流量大， tcp连接数多等等一些列问题。

**主机重启**

delta\(node\_boot\_time\_seconds\[5m\]\) \!= 0

![](../../image/20210912130137384.png)

**文件只读异常**

node\_filesystem\_readonly == 1

**CPU****使用率**

\(\(100 \- \(avg by\(instance,ip,hostname\) \(irate\(node\_cpu\_seconds\_total\{mode="idle"\}\[5m\]\)\) \* 100\)\)\)

![](../../image/20210912130137433.png)

**内存使用率**

\(100 \-\(node\_memory\_MemTotal\_bytes \-node\_memory\_MemFree\_bytes+node\_memory\_Buffers\_bytes+node\_memory\_Cached\_bytes \) / node\_memory\_MemTotal\_bytes \* 100 \)

**IO****性能**

 100-\(avg\(irate\(node\_disk\_io\_time\_seconds\_total\[5m\]\)\) by\(instance,hostname\)\* 100\) \< 40

**磁盘使用率**

100-\(node\_filesystem\_free\_bytes\{fstype=\~"ext4|xfs"\}/node\_filesystem\_size\_bytes \{fstype=\~"ext4|xfs"\}\*100\) > 80

**主机网络IO速率**

**入速率\(MiB/s\)**

irate\(node\_network\_receive\_bytes\_total\{\}\[5m\]\) / 1024 / 1024

**出速率\(MiB/s\)**

irate\(node\_network\_transmit\_bytes\_total\{\}\[5m\]\) / 1024 / 1024

**主机磁盘IO**

**写速率\(MiB/s\)**

irate\(node\_disk\_written\_bytes\_total\{\}\[5m\]\) / 1024 / 1024

**读速率\(MiB/s\)**

irate\(node\_disk\_read\_bytes\_total\{\}\[5m\]\) / 1024 / 1024

**TCP****连接数**

node\_netstat\_Tcp\_CurrEstab