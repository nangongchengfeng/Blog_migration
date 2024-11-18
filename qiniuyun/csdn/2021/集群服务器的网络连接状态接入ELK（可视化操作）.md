---
author: 南宫乘风
categories:
- 项目实战
date: 2021-11-22 15:36:12
description: 同步集群服务器的网络连接状态上篇文件，主要是把集群服务器状态同步到一台机器上，然后通过，什么的比较方便。但是考虑到更简单，方便的操作，那就是接入日志管理平台来来，大致思路很简单有个完成的集群使用收集汇。。。。。。。
image: ../../title_pic/46.jpg
slug: '202111221536'
tags:
- Linux实战操作
- zookeeper
- java
- Kubernetes
title: 集群服务器的网络连接状态接入ELK（可视化操作）
---

<!--more-->

![](../../image/f0d382ca74a74af2b711e7e8e8a4a5cb.png)

# [Rsyslog同步集群服务器的网络连接状态](https://blog.csdn.net/heian_99/article/details/121432620)

上篇文件，主要是把集群服务器状态同步到一台机器上，然后通过grep，awk 什么的比较方便。但是考虑到更简单，方便的操作，那就是接入elk日志管理平台

来来，大致思路很简单

（1）有个完成的elk集群

（2）使用filebeat收集汇总的tcp.log（只要一个filebeat就可以）

（3）把filebeat数据发送到logstash中，进行日志切割转换（靠，正则很难受）

（4）把logstash的数据存储到es

（5）kibana展示es中的数据日志

# （1）filebeat收集tcp.log

来来，看配置，很简单

## 配置文件

```bash
[root@logserver01 filebeat]# cat tcp_listen.yml 
#=========================== Filebeat inputs =============================
filebeat.inputs:
- type: log
  enabled: true
  tail_files: true
  paths:
    - /var/log/history/tcp.log
#=========================== Filebeat outppp_id: messuts =============================
output.logstash:
  hosts: ["127.0.0.1:5516"]

```

## 启动命令

```bash
nohup /usr/local/filebeat/filebeat -e -c  /usr/local/filebeat/tcp_listen.yml -path.data=/usr/local/filebeat/tcp_listen &
```

# （2）logstash收集清洗日志

清洗日志，比较麻烦，需要grok正则来实现

grok正则

<http://grokdebug.herokuapp.com/>

```bash
2021-11-22T10:51:41+08:00 172.17.42.101 storm-42-101  [storm] info: 172.21.5.22 ESTABLISHED 1
```

## grok的正则

```bash
^(?<atime>\d+-\d+-\d+)(?:[^\d]+)(?<hhmmss>\d+:\d+:\d+)(?:[^\d]+\d+:\d+)(?:\s+)(?<hostip>\d+\.\d+\.\d+\.\d+)(?:\s)(?<hostname>[^ ]+)(?:\s+)(?<hostuser>[^ ]+)(?:\s+)(?<names>[^ ]+)(?:\s)%{HOSTNAME:connect_IP}(?:\s)(?<connect_state>[^ ]+)(?:\s)%{HOSTNAME:connect_num}
```

![](../../image/c088ea0d45314ae6a0ce377cd9e5e697.png)

##  配置文件

```bash
[root@logserver01 config]# cat tcp_listen.conf 
input {
   beats {
    port => 5516
    type => syslog
  }
}

filter {
    grok {
        match => { 
		"message" => "^(?<atime>\d+-\d+-\d+)(?:[^\d]+)(?<hhmmss>\d+:\d+:\d+)(?:[^\d]+\d+:\d+)(?:\s+)(?<hostip>\d+\.\d+\.\d+\.\d+)(?:\s)(?<hostname>[^ ]+)(?:\s+)(?<hostuser>[^ ]+)(?:\s+)(?<names>[^ ]+)(?:\s)%{HOSTNAME:connect_IP}(?:\s)(?<connect_state>[^ ]+)(?:\s)%{HOSTNAME:connect_num}"
		}
		overwrite => ["message"]
		
    }
	mutate {  
	split => ["type",","]     
	}

    mutate{remove_field => [ "tags","agent","host","log","ecs","type" ]}
	
	ruby { 
    code => "event.set('index_date', event.get('@timestamp').time.localtime + 8*60*60)" 
} 
	mutate { 
    convert => ["index_date", "string"] 
    gsub => ["index_date", "-\d{2}T([\S\s]*?)Z", ""] 
    gsub => ["index_date", "-", "."] 
}  
	date {
        match => ["time", "yyyy-MM-dd HH:mm:ss,SSS", "UNIX"]
        target => "@timestamp"
        locale => "cn"
    }
}

output {
  stdout {
#    codec=> rubydebug
  }
  elasticsearch {
    hosts => ["http://127.0.0.1:9200"]
    index => "tcp_listen_%{index_date}"
  }
}

```

## 启动命令

```bash
nohup /usr/local/logstash/bin/logstash -f /usr/local/logstash/config/tcp_listen.conf --path.data=/usr/local/logstash/data/tcp_listen &
```

![](../../image/ea84829a4e714484a236960efe963572.png)

#  （3）kibana展示数据

## 创建索引

![](../../image/08e1fd28fc304fae98021a42818ac2e2.png)

##  查看数据

脚本为15分钟拉去一次数据的。所有在kibana展示也是和脚本时间同步的 

![](../../image/0df915317d564e6b9202788e3bd7d783.png)

![](../../image/f0d382ca74a74af2b711e7e8e8a4a5cb.png)

![](../../image/07d4b6c2a5684582a567930301edfb08.png)