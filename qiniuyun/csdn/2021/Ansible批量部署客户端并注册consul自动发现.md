---
author: 南宫乘风
categories:
- Prometheus监控
date: 2021-08-23 19:25:59
description: 前文链接：需求：监控多台主机时，基于自动发现模块，主机安装采集器注册到那台，识别到。获取地址上的监控主机列表，实现多台主机自动发现。思路：机器安装采集器注册为系统服务使用注册到机器中监控到后，配置地址。。。。。。。
image: ../../title_pic/65.jpg
slug: '202108231925'
tags:
- Ansible
- prometheus
- ansible
title: Ansible批量部署客户端并注册consul自动发现
---

<!--more-->

前文链接：<https://blog.csdn.net/heian_99/article/details/119874180>

需求：prometheus监控多台主机时，基于自动发现consul模块，主机安装采集器注册到那台consul，consul识别到。promethues获取consul地址上的监控主机列表，实现多台主机自动发现。

思路：

1.  web机器安装node\_exporter采集器  
    2.注册node\_exporter为系统服务  
    3.使用curl -x PUT ... 注册到consul机器中  
    4.consul监控到后，prometheus配置consul地址。  
    1-3步都可用ansible批量完成。

node\_exoporter软件包 ，system服务配置文件，注册脚本，注册接口

如果有密码验证还需要一个config.yml

### consul-register.sh

注册脚本\(传参方式注册\)：

```bash
#!/bin/bash
service_name=$1
instance_id=$2
ip=$3
port=$4

curl -X PUT -d '{"id": "'"$instance_id"'","name": "'"$service_name"'","address": "'"$ip"'","port": '"$port"',"tags": ["'"$service_name"'"],"checks": [{"http": "http://'"$ip"':'"$port"'","interval": "5s"}]}' http://10.10.10.27:8500/v1/agent/service/register
```

### node\_exporter.service

node\_exporter系统服务配置文件

```bash
[heian@zabbix ~]$ cat node_exporter.service 


[Unit]
Description=node_exporter
After=network.target 

[Service]
ExecStart=/usr/local/node_exporter/node_exporter\
          --web.listen-address=:9100\
          --collector.systemd\
          --collector.systemd.unit-whitelist=(sshd|nginx).service\
          --collector.processes\
          --collector.tcpstat\
          --collector.supervisord
[Install]
WantedBy=multi-user.target



--collector.systemd --collector.systemd.unit-include=(docker|portal|sshd).service 配置的意思是只收集docker,portal,sshd服务的数据
--web.config=/usr/local/jiankong/node_exporter/config.yml 如果有密码验证接口需要指定这个config.yml，里面保存的用户名和密码。需要把这条配在启动execstart行的node_proter后。
```

### ansible-playbook

```
cat hosts

[blog]
10.10.10.15  name=nginx

```

```bash
cat playbook.yml

- hosts: blog
  remote_user: heian
  become: yes
  become_user: root
  become_method: sudo
  gather_facts: no
  tasks:
    - name: 推送采集器安装包
      unarchive: src=node_exporter-1.2.2.linux-amd64.tar.gz dest=/usr/local/
    - name: 重命名
      shell: |
        cd /usr/local/ 
        if [ ! -d node_exporter ];then 
           mv node_exporter-1.2.2.linux-amd64  node_exporter 
        fi
    - name: 推送system文件
      copy: src=node_exporter.service dest=/usr/lib/systemd/system
    - name: 启动服务
      systemd: name=node_exporter state=started enabled=yes
    - name: 推送注册脚本
      copy: src=consul-register.sh dest=/usr/local/node_exporter
    - name: 注册当前节点
      shell: /bin/sh /usr/local/node_exporter/consul-register.sh {{ group_names[0] }} {{ name }} {{ inventory_hostname }} 9100
```

\{<!-- -->{ group_names[0] }} --ansible内置变量 代表hosts中自定义组名，数组形式，[0]取第一个  
\{<!-- -->{ name }} -- hosts文件中定义主机的名字，如name=web1  
\{<!-- -->{ inventory_hostname }} 当前执行主机的ip  
执行：

![](../../image/20210823192310944.png)

看一下consul中，服务已经注册进来了 

![](../../image/20210823192329533.png)

### prometheus自动发现

![](../../image/20210823192429609.png)

 ![](../../image/20210823192453713.png)

 

![](../../image/20210823192508451.png)

 

参考文档地址：<https://www.jianshu.com/p/f243a3aec18e>