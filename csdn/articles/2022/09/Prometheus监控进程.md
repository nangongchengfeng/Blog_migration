+++
author = "南宫乘风"
title = "Prometheus监控进程"
date = "2022-09-21 14:37:01"
tags=['prometheus', '服务器', 'java']
categories=['Prometheus监控']
image = "post/4kdongman/62.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/126972415](https://blog.csdn.net/heian_99/article/details/126972415)

# <a id="Prometheus_0"></a>Prometheus监控进程

process-export主要用来做进程监控，比如某个服务的进程数、消耗了多少CPU、内存等资源。

## <a id="processexporter_5"></a>一、process-exporter使用

‍

### <a id="11__processexporter_9"></a>1.1 下载 process-exporter

[process-exporter GibHUB地址](https://github.com/ncabatoff/process-exporter)<br> [process-exporter 下载地址](https://github.com/ncabatoff/process-exporter/releases/download/v0.7.5/process-exporter-0.7.5.linux-amd64.tar.gz)

process-exporter可以使用命令行参数也可以指定配置文件启动

### <a id="12__processexporter_16"></a>1.2 配置 process-exporter

```
vim /usr/local/process-exporter/process_name.yaml #存放脚本的地方

process_names:
#  - name: "{<!-- -->{.Comm}}"
#    cmdline:
#    - '.+'

  - name: "{<!-- -->{.Matches}}"
    cmdline:
    - 'nginx' #唯一标识

  - name: "{<!-- -->{.Matches}}"
    cmdline:
    - '/opt/atlassian/confluence/bin/tomcat-juli.jar'

  - name: "{<!-- -->{.Matches}}"
    cmdline:
    - 'vsftpd'

  - name: "{<!-- -->{.Matches}}"
    cmdline:
    - 'redis-server'

```

示例：

>  
 cmdline: 所选进程的唯一标识，ps -ef 可以查询到。如果改进程不存在，则不会有该进程的数据采集到。 
 例如：&gt; ps -ef | grep redis 
 redis 4287 4127 0 Oct31 ? 00:58:12 redis-server *:6379 
 <table><thead>|{<!-- -->{.Comm}}|groupname=”redis-server”|exe或者sh文件名称
</thead><tbody>|{<!-- -->{.ExeBase}}|groupname=”redis-server *:6379”|/
|{<!-- -->{.ExeFull}}|groupname=”/usr/bin/redis-server *:6379”|ps中的进程完成信息
|{<!-- -->{.Username}}|groupname=”redis”|使用进程所属的用户进行分组
|{<!-- -->{.Matches}}|groupname=”map[:redis]”|表示配置到关键字“redis”
</tbody></table>


### <a id="13__59"></a>1.3 编写启动脚本

```
vim /usr/lib/systemd/system/process_exporter.service
 
[Unit]
Description=Prometheus exporter for processors metrics, written in Go with pluggable metric collectors.
Documentation=https://github.com/ncabatoff/process-exporter
After=network.target
  
[Service]
Type=simple
User=root
WorkingDirectory=/usr/local/process-exporter
ExecStart=/usr/local/process-exporter/process-exporter -config.path=/usr/local/process-exporter/process-exporter.yaml
Restart=on-failure
  
[Install]
WantedBy=multi-user.target

```

### <a id="14__procexxexport_80"></a>1.4 启动 procexx-export

```
systemctl daemon-reload
systemctl start process_exporter
systemctl enable process_exporter

```

**验证监控数据**

```
curl http://localhost:9256/metrics

#相关测试的数据
# HELP http_response_size_bytes The HTTP response sizes in bytes.
# TYPE http_response_size_bytes summary
http_response_size_bytes{<!-- -->handler="prometheus",quantile="0.5"} 2988
http_response_size_bytes{<!-- -->handler="prometheus",quantile="0.9"} 2996
http_response_size_bytes{<!-- -->handler="prometheus",quantile="0.99"} 3006
http_response_size_bytes_sum{<!-- -->handler="prometheus"} 1.34205181e+08
http_response_size_bytes_count{<!-- -->handler="prometheus"} 45188
# HELP namedprocess_namegroup_context_switches_total Context switches
# TYPE namedprocess_namegroup_context_switches_total counter
namedprocess_namegroup_context_switches_total{<!-- -->ctxswitchtype="nonvoluntary",groupname="map[:bladebit]"} 7.7977455e+07
namedprocess_namegroup_context_switches_total{<!-- -->ctxswitchtype="nonvoluntary",groupname="map[:pw_python.py]"} 2.02666e+06
namedprocess_namegroup_context_switches_total{<!-- -->ctxswitchtype="voluntary",groupname="map[:bladebit]"} 3.335109e+06
namedprocess_namegroup_context_switches_total{<!-- -->ctxswitchtype="voluntary",groupname="map[:pw_python.py]"} 8.22652233e+08
# HELP namedprocess_namegroup_cpu_system_seconds_total Cpu system usage in seconds
# TYPE namedprocess_namegroup_cpu_system_seconds_total counter
namedprocess_namegroup_cpu_system_seconds_total{<!-- -->groupname="map[:bladebit]"} 94275.01000000017
namedprocess_namegroup_cpu_system_seconds_total{<!-- -->groupname="map[:pw_python.py]"} 64818.93000000004
# HELP namedprocess_namegroup_cpu_user_seconds_total Cpu user usage in seconds
# TYPE namedprocess_namegroup_cpu_user_seconds_total counter
namedprocess_namegroup_cpu_user_seconds_total{<!-- -->groupname="map[:bladebit]"} 2.42621264299998e+07
namedprocess_namegroup_cpu_user_seconds_total{<!-- -->groupname="map[:pw_python.py]"} 85.29000000000613
# HELP namedprocess_namegroup_major_page_faults_total Major page faults
# TYPE namedprocess_namegroup_major_page_faults_total counter
namedprocess_namegroup_major_page_faults_total{<!-- -->groupname="map[:bladebit]"} 18261
namedprocess_namegroup_major_page_faults_total{<!-- -->groupname="map[:pw_python.py]"} 1236
# HELP namedprocess_namegroup_memory_bytes number of bytes of memory in use
# TYPE namedprocess_namegroup_memory_bytes gauge
namedprocess_namegroup_memory_bytes{<!-- -->groupname="map[:bladebit]",memtype="resident"} 4.46810939392e+11
namedprocess_namegroup_memory_bytes{<!-- -->groupname="map[:bladebit]",memtype="swapped"} 0
namedprocess_namegroup_memory_bytes{<!-- -->groupname="map[:bladebit]",memtype="virtual"} 4.47847292928e+11
namedprocess_namegroup_memory_bytes{<!-- -->groupname="map[:pw_python.py]",memtype="resident"} 1.2959744e+07
namedprocess_namegroup_memory_bytes{<!-- -->groupname="map[:pw_python.py]",memtype="swapped"} 0
namedprocess_namegroup_memory_bytes{<!-- -->groupname="map[:pw_python.py]",memtype="virtual"} 2.4733696e+08

```

‍

## <a id="prometheus__131"></a>二、prometheus 配置

添加或修改配置

```
- job_name: 'dev_prometheus'
  scrape_interval: 10s
  honor_labels: true
  metrics_path: '/metrics'

  static_configs:
  - targets: ['127.0.0.1:9090','127.0.0.1:9100']
    labels: {<!-- -->cluster: 'dev',type: 'basic',env: 'dev',job: 'prometheus',export: 'prometheus'}
  - targets: ['127.0.0.1:9256']
    labels: {<!-- -->cluster: 'dev',type: 'process',env: 'dev',job: 'prometheus',export: 'process_exporter'}

```

重启prometheus服务

```
curl -X POST http://127.0.0.1:9090/-/reload


```

## <a id="grafana_155"></a>三、grafana出图

process-exporter对应的dashboard为：[https://grafana.com/grafana/dashboards/249](https://grafana.com/grafana/dashboards/249)

**效果如下**

![5fbfbd062f45480aaf08451fe1802dd4.png](https://img-blog.csdnimg.cn/5fbfbd062f45480aaf08451fe1802dd4.png)

## <a id="_164"></a>四、常用监控规则

### <a id="_166"></a>进程数

```
alert: 进程告警
expr: sum(namedprocess_namegroup_states) by (cluster,job,instance) &gt; 500
for: 20s
labels:
  severity: warning
annotations:
  value: 服务器当前已产生 {<!-- -->{<!-- --> $value }} 个进程，大于告警阈值

```

### <a id="_178"></a>僵尸进程数

```
alert: 进程告警
expr: sum by(cluster, job, instance, groupname) (namedprocess_namegroup_states{<!-- -->state="Zombie"}) &gt; 0
for: 1m
labels:
  severity: warning
annotations:
  value: 当前产生 {<!-- -->{<!-- --> $value }} 个僵尸进程

```

### <a id="_190"></a>进程重启

```
alert: 进程重启告警
expr: ceil(time() - max by(cluster, job, instance, groupname) (namedprocess_namegroup_oldest_start_time_seconds)) &lt; 60
for: 25s
labels:
  label: alert_once
  severity: warning
annotations:
  value: 进程 {<!-- -->{<!-- --> $labels.groupname }} 在 {<!-- -->{<!-- --> $value }} 秒前发生重启

```

### <a id="_203"></a>进程退出

```
alert: 进程退出告警
expr: up{<!-- -->export="process_exporter"} == 0 or max by(cluster, job, instance, groupname) (delta(namedprocess_namegroup_oldest_start_time_seconds{<!-- -->groupname=~"^map.*"}[10d])) &lt; 0
for: 55s
labels:
  severity: warning
annotations:
  value: 进程 {<!-- -->{<!-- --> $labels.export}} 已退出

```

## <a id="Ansible_215"></a>五、Ansible批量添加

![6a6c385e56e14cfc949b074337178c38.png](https://img-blog.csdnimg.cn/6a6c385e56e14cfc949b074337178c38.png)

这里采用Consul注册发现方式，相关类容可以查询网上

### <a id="51Consul_222"></a>5.1Consul注册脚本

```
#!/bin/bash
service_name=$1
instance_id=$2
ip=$3
port=$4
 
curl -X PUT -d '{"id": "'"$instance_id"'","name": "'"$service_name"'","address": "'"$ip"'","port": '"$port"',"tags": ["'"$service_name"'"],"checks": [{<!-- -->"http": "http://'"$ip"':'"$port"'","interval": "5s"}]}' http://10.1.8.202:8500/v1/agent/service/register



```

### <a id="Ansible_236"></a>Ansible剧本脚本

```
[root@openvpn process]# cat playbook.yml 
- hosts: Harvester
  remote_user: root
  gather_facts: no
  tasks:
    - name: 推送采集器安装包
      unarchive: src=process-exporter.tar.gz dest=/usr/local/
    - name: 重命名
      shell: |
        cd /usr/local/ 
        if [ ! -d process-exporter ];then 
           mv process-exporter-0.4.0.linux-amd64  process-exporter 
        fi
    - name: 查询主机名称
      shell: echo "h-`hostname`"
      register: name_host
    - name: 推送system文件
      copy: src=process_exporter.service dest=/usr/lib/systemd/system
    - name: 启动服务
      systemd: name=process_exporter state=started enabled=yes
    - name: 推送注册脚本
      copy: src=consul-register.sh dest=/usr/local/process-exporter
    - name: 注册当前节点
      shell: /bin/sh /usr/local/process-exporter/consul-register.sh {<!-- -->{<!-- --> group_names[0] }} {<!-- -->{<!-- --> name_host.stdout  }} {<!-- -->{<!-- --> inventory_hostname }} 9256


```

![13d7ee428028406b850e8642f5aeb555.png](https://img-blog.csdnimg.cn/13d7ee428028406b850e8642f5aeb555.png)

‍
