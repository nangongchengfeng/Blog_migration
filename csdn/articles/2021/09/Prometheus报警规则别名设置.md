+++
author = "南宫乘风"
title = "Prometheus报警规则别名设置"
date = "2021-09-12 13:02:43"
tags=['prometheus', '监控', '别名']
categories=['Prometheus监控']
image = "post/4kdongman/79.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/120249465](https://blog.csdn.net/heian_99/article/details/120249465)



prometheus报警规则，是由promsql语句编写组合的，但是有时语句会很长，我们看还好，但是有时间业务组那边也会使用promsql来看主机偏高的指标，这边只能设置别名，方便他们使用。

**别名设置：**

很简单，也是和报警规则一样，但是语法可能不一样

**示例**<br>  

```
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

node:cpu_usage:ratio 就是查看cpu使用率的指标

下面两张图就是区别

![20210912125819832.png](https://img-blog.csdnimg.cn/20210912125819832.png)

 ![20210912125903402.png](https://img-blog.csdnimg.cn/20210912125903402.png)

 我们正常使用，就是直接采用这个别名指标了

![20210912130017467.png](https://img-blog.csdnimg.cn/20210912130017467.png)

 **业务组使用**

prometheus支持promsql语法，我们可以通过相关语句，很快定位到集群，资源使用情况

如：高CPU 高内存，出入流量大， tcp连接数多等等一些列问题。

**主机重启**

delta(node_boot_time_seconds[5m]) != 0

![20210912130137384.png](https://img-blog.csdnimg.cn/20210912130137384.png)

**文件只读异常**

node_filesystem_readonly == 1

**CPU****使用率**

((100 - (avg by(instance,ip,hostname) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)))

![20210912130137433.png](https://img-blog.csdnimg.cn/20210912130137433.png)



**内存使用率**

(100 -(node_memory_MemTotal_bytes -node_memory_MemFree_bytes+node_memory_Buffers_bytes+node_memory_Cached_bytes ) / node_memory_MemTotal_bytes * 100 ) 

**IO****性能**

 100-(avg(irate(node_disk_io_time_seconds_total[5m])) by(instance,hostname)* 100) &lt; 40

**磁盘使用率**

100-(node_filesystem_free_bytes{fstype=~"ext4|xfs"}/node_filesystem_size_bytes {fstype=~"ext4|xfs"}*100) &gt; 80

**主机网络IO速率**

**入速率(MiB/s)**

irate(node_network_receive_bytes_total{}[5m]) / 1024 / 1024 

**出速率(MiB/s)**

irate(node_network_transmit_bytes_total{}[5m]) / 1024 / 1024

**主机磁盘IO**

**写速率(MiB/s)**

irate(node_disk_written_bytes_total{}[5m]) / 1024 / 1024 

**读速率(MiB/s)**

irate(node_disk_read_bytes_total{}[5m]) / 1024 / 1024

**TCP****连接数**

node_netstat_Tcp_CurrEstab
