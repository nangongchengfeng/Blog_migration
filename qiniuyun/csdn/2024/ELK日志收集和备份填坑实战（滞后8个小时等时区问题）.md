---
author: 南宫乘风
categories:
- 项目实战
date: 2024-04-15 11:39:49
description: 的备份：快照备份根据时间，每天零点在机器来调用接口实现快照备份，通过快照备份，可以定准恢复到某一天的日志。现象：坑：但是恢复某一天日志，发现会少小时的日志，基本是：时间段、引言：在大规模分布式系统中，。。。。。。。
image: ../../title_pic/30.jpg
slug: '202404151139'
tags:
- elk
- kibana
title: ELK日志收集和备份填坑实战 （滞后8个小时等时区问题）
---

<!--more-->

ES的备份：[ES快照备份](https://blog.csdn.net/heian_99/article/details/127828348?spm=1001.2014.3001.5501)    
根据时间，每天零点在Linux机器crontab来调用api接口实现快照备份，通过快照备份，可以定准恢复到某一天的日志。
现象：（坑：但是恢复某一天日志，发现会少8小时的日志，基本是：0:00 - 08:00 时间段）


## 1、引言： 
在大规模分布式系统中，ELK（Elasticsearch、Logstash、Kibana）栈已成为日志管理和分析的标准工具集。然而，实际部署与运维过程中，往往会遭遇各种挑战，其中时区问题导致的日志时间滞后尤为常见。本文将聚焦于解决ELK日志收集与备份过程中出现的滞后8小时等时区问题，分享实战经验与填坑策略。

## 2、问题现象与原因
### 1、剖析滞后8小时时区

现象描述：在Kibana上观察到的一个典型现象是，即使日志事件是在当地时间上午9点发生的，但在日志系统中显示的时间却是下午5点。这种时差问题会导致运维团队在实时监控和响应中遭遇不少困难，因为所有的日志数据都显示为8小时前的事件。

**问题根源**

这一问题通常由以下几个因素造成：

1. 日志源端时区设置错误：
日志生成时，很多系统默认使用格林尼治标准时间（GMT）来记录时间戳，而不是当地时间。如果日志源设备或服务的时区设置不正确，或未明确指定时区，就会在源头产生时间偏差。

2. 传输过程中的时区处理不当：
在日志数据的收集过程中，如使用Logstash或Filebeat等工具，若这些工具没有被正确配置为转换或识别正确的时区，它们在处理日志时会继续使用GMT时间戳，从而进一步传递错误的时间信息。

3. Elasticsearch存储与展示的时区配置不当：
Elasticsearch在存储时间数据时，默认使用UTC时间。如果在Elasticsearch或Kibana中没有设置正确的时区，即使原始日志的时间戳是正确的，展示时也会因为时区转换错误而导致时间显示不正确
 ### 2、时区问题拆解
**Elasticserch 默认时区是？能改吗？**
官方文档强调：在 Elasticsearch 内部，日期被转换为 UTC时区并存储为一个表示自1970-01-01 00:00:00  以来经过的毫秒数的值。

Internally, dates are converted to UTC (if the time-zone is specified) and stored as a long number representing milliseconds-since-the-epoch.

https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html

Elasticsearch date 类型默认时区：UTC。

正如官方工程师强调（如下截图所示）：Elasticsearch 默认时区不可以修改
![在这里插入图片描述](../../image/d56a34ce1bca46779c4c0da3709c7621.png)
https://discuss.elastic.co/t/index-creates-in-different-timezone-other-than-utc/148941但，我们可以“曲线救国”，通过：

ingest pipeline 预处理方式写入的时候修改时区；
logstash filter 环节做时区转换；
查询时指定时区；
聚合时指定时区。

 **Kibana 默认时区是？能改吗？**
kibana 默认时区是浏览器时区。可以修改，修改方式如下：Stack Management -> Advanced Settings ->Timezone for data formatting.
![在这里插入图片描述](../../image/aeee464bca284f3e9d2bb4f0b24891a4.png)
 **Logstash 默认时区是？能改吗？**

默认：UTC。可以通过中间：filter 环节进行日期数据处理，包括：转时区操作。
![在这里插入图片描述](../../image/2073ee08d27d4858a65ab435994370e9.png)
- logstash 默认 UTC 时区。
- Elasticsearch 默认 UTC 时区。
- Kibana 默认浏览器时区，基本我们用就是：东八区。
- 如果基于Mysql 同步数据，Mysql 数据是：东八区。

## 3、填坑实战与解决方案
基于上面的分析，如何解决时区问题呢？。
实战项目中，时间问题就转嫁为：写入的时候转换成给定时区（如：东8区）就可以。
**1、查看机器的时区和日志**

```bash
/ # date
Mon Apr 15 11:21:29 CST 2024
```
![在这里插入图片描述](../../image/ce7561b4cf524faa9e8df8f0c8bdf27e.png)
**2、Filebeaet 收集配置**

```yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /app/logs/app/*.log
  multiline.pattern: ^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}[.,:]0{0,1}\d{3}
  multiline.negate: true
  multiline.match: after
  fields:
    logtype: ${LOGTYPE:app}

fields_under_root: true
fields:
  ip: ${POD_IP}

output.logstash:
  hosts: ["logstash-server.default.svc.cloudcs.fjf:5044"]
```
**3、logstash 中间 filter 环节处理**
数据源端：APP日志；
数据目的端：Elasticsearch；
同步方式：logstash，本质借助：logstash_input_jdbc 插件同步；
时区处理：logstash filter 环节 ruby 脚本处理。 


```json
{"@timestamp":"2024-04-15T10:48:34.518811962+08:00","severity":"INFO","service":"cat-outer-gateway","trace":"","span":"","parent":"","exportable":"","pid":"1","thread":"reactor-http-epoll-2","class":"c.fujfu.gateway.filter.CallBackUriFilter","rest":"path:/cat-payment-dock/api/minSheng/notify,method:POST\n"}
{"@timestamp":"2024-04-15T10:55:29.711692942+08:00","severity":"INFO","service":"cat-outer-gateway","trace":"","span":"","parent":"","exportable":"","pid":"1","thread":"reactor-http-epoll-4","class":"c.fujfu.gateway.filter.CallBackUriFilter","rest":"path:/cat-payment-dock/api/minSheng/notify,method:POST\n"}
```

```bash
2024-04-15 11:32:57.582  INFO [HzgDfyOvQqCH4DsY5Al7Jw] 1 --- [nio-8050-exec-9] c.f.f.s.impl.FpProductCfgServiceImpl     : capitalId:1724007481146916866-该用户渠道被限制，channelCodeList:[huawei, oppo, vivo, xiaomi, yingyongbao, yingyongbaotuiguang, Android_oppo, Android_yingyongbao, Android_huawei, Android_xiaomi, FYH-rongyao, FYH-vivo, FYH-xiaomi, FYH-huawei] ,userReqVO.getRegisterChannel():huawei
2024-04-15 11:32:57.695  INFO [TtPg4TgCQI+MFkLxSCZzMA] 1 --- [nio-8050-exec-2] c.f.f.s.f.request.JUZIFundProductCaller  : 【桔子数科】请求明文：https://api-gateway.jzhlkj.com/bus/standard/credit/queryQuota，参数：{"channelUid":"29443d29067c4182baec1115026cf8d5"}
```



下方的脚本就实现**收集上方两种日志格式** 和 **写入的时候转换成给定时区**这个功能。

date 的数据 就是 东八区 的时间。我直接把 东八区的时间 写入`@timestamp` 在传入到ES（东八区） 。然后在 Kibana中访问 也是东八区，形成一个闭环
```json
    input {
      beats {
        port => 5044
      }
    }

    filter {
      if [fields][json] == "true" {
        json {
          source => "message"
          remove_field => ["message","agent","tags","ecs"]
          add_field => {
            "loglevel" => "%{[severity]}"
          }
        }
      } else if [fields][logtype] == "powerjob" {
        grok {
          match => { "message" => "%{TIMESTAMP_ISO8601:date} \s{0,1}(?<severity>.*?) (?<pid>.*?) --- \[(?<thread>.*?)\] (?<class>.*?) \s*: (?<rest>.*+?)" }
          remove_field => ["message","agent","tags"]
          add_field => {
            "loglevel" => "%{[severity]}"
          }
        }
        mutate {
          update => { "[fields][logtype]" => "logstash" }
        }
      } else {
        grok {
          match => { "message" => [
                    "%{TIMESTAMP_ISO8601:date} (?<loglevel>.*?)\s{1,2}\| \[(?<threadname>.*?)\] (?<classname>.*?) \[(?<codeline>.*?)\] \| \[(?<traceid>.*?)\] \| (?<msg>.*+?)",
                    "%{TIMESTAMP_ISO8601:date} (?<loglevel>.*?)\s{1,2}\| \[(?<threadname>.*?)\] (?<classname>.*?) \[(?<codeline>.*?)\] \| (?<msg>.*+?)",
                    "\[%{TIMESTAMP_ISO8601:date}\] \[(?<loglevel>.*?)\s{0,2}\] \[(?<threadname>.*?)\] (?<classname>.*?) (?<codeline>.*?) - (?<msg>.*+?)",
                     "%{TIMESTAMP_ISO8601:date} \[(?<threadname>.*?)\] (?<loglevel>.*?)\s{0,2} (?<classname>.*?) (?<codeline>.*?) - (?<msg>.*+?)",
                     "\[%{TIMESTAMP_ISO8601:date}\] \[\s{0,2}(?<loglevel>.*?)\] \[(?<threadid>.*?)\] \[(?<threadname>.*?)\] \[(?<classname>.*?)\] : (?<msg>.*+?)"
                   ]}
          remove_field => ["message","agent","tags"]
        }
      }
      ruby {
        code =>'
        arr = event.get("host")["name"].split(".")[0]
        event.set("projectname",arr)
        '
      }
      date {
        match => ["date","ISO8601","yyyy-MM-dd HH:mm:ss.SSS"] #获取date的时间
        target => "@timestamp" # 复制给@timestamp 字段
        timezone => "Asia/Shanghai" # 设置 上海地区
      }

    }
    output {

      elasticsearch {
        hosts => ["elasticsearch-log.prod.server.fjf:9200"]
        user => "xxxxx"
        password => "xxxxx"
        manage_template => false
        index => "%{[fields][logtype]}-prod-%{+YYYY.MM.dd}"
      }
    }
```

**修改前**

![在这里插入图片描述](../../image/2253076e11d84bb8a25717d6f351d751.png)


**修改后**
![在这里插入图片描述](../../image/6e98e01bf97d4fb3968d29d3588afb49.png)

![在这里插入图片描述](../../image/d60e8645de934971b3004f50046931d5.png)





## 4、总结

数据写入时间不一致、数据滞后8小时等时区问题的本质是：各个处理端时区不一致，写入源的时区、Kibana默认是本地时区（如中国为：东8区时区），而 logstash、Elasticsearch 是UTC时区。





参考文档：[https://www.cnblogs.com/fat-girl-spring/p/15122906.html](https://www.cnblogs.com/fat-girl-spring/p/15122906.html)
