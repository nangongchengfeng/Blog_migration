+++
author = "南宫乘风"
title = "Python编写告警信息，整合Alertmanager告警"
date = "2022-07-06 11:07:38"
tags=['python', 'flask', '开发语言']
categories=['Python学习']
image = "post/4kdongman/89.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/125618555](https://blog.csdn.net/heian_99/article/details/125618555)



![813725adf5d84c97ab5eeedb87375685.png](https://img-blog.csdnimg.cn/813725adf5d84c97ab5eeedb87375685.png)

#  Alertmanager告警 系统整合

## 流程

（1）监控端，可以使用Python 或者 shell 进行监控，把 相关的json数据推送到Alertmanager

（2）Alertmanager端 进行 汇总，发送，后续可以静默，抑制等功能

（3）把告警的数据发送到prometheusalert，进行钉钉的发送

## 环境

软件

[prometheusalert 告警系统](https://github.com/feiyu563/PrometheusAlert) ：主要是数据的各个渠道发送

[Alertmanager 告警处理](https://github.com/prometheus/alertmanager)：主要汇总数据，抑制，静默

## 思路

编写告警测试数据时，我们可以不用生成时间，仅生成相关的告警指标，时间程序会帮忙生成（待测试）



# 步骤

## 获取Alertmanager数据格式

方法，通过flask 编写接口，Alertmanager配置，告警时回把数据发送到此接口 ，进行展示查看



```
from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/send/", methods=["POST"])
def send():
    try:
        data = json.loads(request.data)
        print(data)
        alerts = data['alerts']
        for i in alerts:
            print('SEND SMS: ' + str(i))
    except Exception as e:
        print(e)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)

```

在Alertmanager配置

```
[root@prometheus-server alertmanager-0.24.0.linux-amd64]# cat alertmanager.yml
global:
  resolve_timeout: 5m
route:
  group_by: ['instance']
  group_wait: 30s
  group_interval: 10s
  repeat_interval: 10m
  receiver: 'web.hook.prometheusalert'
receivers:
- name: 'web.hook.prometheusalert'
  webhook_configs:
   - url: http://192.168.96.19:8082/send/

```

产生prometheus的测试数据

关闭客户端，产生告警 

![8631635087364da6af41e3d05958e483.png](https://img-blog.csdnimg.cn/8631635087364da6af41e3d05958e483.png)

**告警数据**

```
{
	'receiver': 'web\\.hook\\.prometheusalert',
	'status': 'firing',
	'alerts': [{
		'status': 'firing',
		'labels': {
			'alertname': '主机存活状态警告！',
			'cloud': '乘风-Dev环境',
			'instance': '192.168.82.105:9100',
			'job': 'node_exporter',
			'severity': '非常严重',
			'team': 'ops'
		},
		'annotations': {
			'description': '192.168.82.105:9100:服务器延时超过5分钟',
			'summary': '192.168.82.105:9100:服务器宕机'
		},
		'startsAt': '2022-07-05T05:54:37.452Z',
		'endsAt': '0001-01-01T00:00:00Z',
		'generatorURL': 'http://prometheus-server.0101101300.fjf:9090/graph?g0.expr=up+%3D%3D+0&amp;g0.tab=1',
		'fingerprint': '4a890f7c225c3bef'
	}],
	'groupLabels': {
		'instance': '192.168.82.105:9100'
	},
	'commonLabels': {
		'alertname': '主机存活状态警告！',
		'cloud': '乘风-Dev环境',
		'instance': '192.168.82.105:9100',
		'job': 'node_exporter',
		'severity': '非常严重',
		'team': 'ops'
	},
	'commonAnnotations': {
		'description': '192.168.82.105:9100:服务器延时超过5分钟',
		'summary': '192.168.82.105:9100:服务器宕机'
	},
	'externalURL': 'http://prometheus-server.0101101300.fjf:9093',
	'version': '4',
	'groupKey': '{}:{instance="192.168.82.105:9100"}',
	'truncatedAlerts': 0
}
```

**有用的告警数据**

```
{
		'status': 'firing',
		'labels': {
			'alertname': '主机存活状态警告！',
			'cloud': '乘风-Dev环境',
			'instance': '192.168.82.105:9100',
			'job': 'node_exporter',
			'severity': '非常严重',
			'team': 'ops'
		},
		'annotations': {
			'description': '192.168.82.105:9100:服务器延时超过5分钟',
			'summary': '192.168.82.105:9100:服务器宕机'
		},
		'startsAt': '2022-07-05T05:54:37.452Z',
		'endsAt': '0001-01-01T00:00:00Z',
		'generatorURL': 'http://prometheus-server.0101101300.fjf:9090/graph?g0.expr=up+%3D%3D+0&amp;g0.tab=1',
		'fingerprint': '4a890f7c225c3bef'
	}
```

**恢复数据**

```
{
	'receiver': 'web\\.hook\\.prometheusalert',
	'status': 'resolved',
	'alerts': [{
		'status': 'resolved',
		'labels': {
			'alertname': '主机存活状态警告！',
			'cloud': '乘风-Dev环境',
			'instance': '192.168.82.105:9100',
			'job': 'node_exporter',
			'severity': '非常严重',
			'team': 'ops'
		},
		'annotations': {
			'description': '192.168.82.105:9100:服务器延时超过5分钟',
			'summary': '192.168.82.105:9100:服务器宕机'
		},
		'startsAt': '2022-07-05T05:54:37.452Z',
		'endsAt': '2022-07-05T05:56:52.452Z',
		'generatorURL': 'http://prometheus-server.0101101300.fjf:9090/graph?g0.expr=up+%3D%3D+0&amp;g0.tab=1',
		'fingerprint': '4a890f7c225c3bef'
	}],
	'groupLabels': {
		'instance': '192.168.82.105:9100'
	},
	'commonLabels': {
		'alertname': '主机存活状态警告！',
		'cloud': '乘风-Dev环境',
		'instance': '192.168.82.105:9100',
		'job': 'node_exporter',
		'severity': '非常严重',
		'team': 'ops'
	},
	'commonAnnotations': {
		'description': '192.168.82.105:9100:服务器延时超过5分钟',
		'summary': '192.168.82.105:9100:服务器宕机'
	},
	'externalURL': 'http://prometheus-server.0101101300.fjf:9093',
	'version': '4',
	'groupKey': '{}:{instance="192.168.82.105:9100"}',
	'truncatedAlerts': 0
}
```

**有用的恢复数据**

```
{
		'status': 'resolved',
		'labels': {
			'alertname': '主机存活状态警告！',
			'cloud': '乘风-Dev环境',
			'instance': '192.168.82.105:9100',
			'job': 'node_exporter',
			'severity': '非常严重',
			'team': 'ops'
		},
		'annotations': {
			'description': '192.168.82.105:9100:服务器延时超过5分钟',
			'summary': '192.168.82.105:9100:服务器宕机'
		},
		'startsAt': '2022-07-05T05:54:37.452Z',
		'endsAt': '2022-07-05T05:56:52.452Z',
		'generatorURL': 'http://prometheus-server.0101101300.fjf:9090/graph?g0.expr=up+%3D%3D+0&amp;g0.tab=1',
		'fingerprint': '4a890f7c225c3bef'
	}
```

## Python发送告警数据

## 发送告警信息

```
import json
import requests

new_packinf = [{
		'status': 'firing',
		'labels': {
			'alertname': '主机存活状态警告！',
			'cloud': '乘风小贷-Dev环境',
			'instance': '192.168.82.105:9100',
			'job': 'node_exporter',
			'severity': '非常严重',
			'team': 'ops'
		},
		'annotations': {
			'description': '192.168.82.105:9100:服务器延时超过5分钟',
			'summary': '192.168.82.105:9100:服务器宕机'
		},
		'startsAt': '2022-07-05T05:54:37.452Z',
		'endsAt': '0001-01-01T00:00:00Z',
		'generatorURL': 'http://prometheus-server.0101101300.fjf:9090/graph?g0.expr=up+%3D%3D+0&amp;g0.tab=1',
		'fingerprint': '4a890f7c225c3bef'
	}]
jsons = json.dumps(new_packinf)
url = "http://192.168.82.105:9093/api/v2/alerts"
headers = {'Content-Type': 'application/json'}
responses = requests.post(url=url, headers=headers, data=jsons)
print(responses.status_code, responses.url)
# print(responses.json())

```

![3d025ff87b69479da1d6e5d8998449b2.png](https://img-blog.csdnimg.cn/3d025ff87b69479da1d6e5d8998449b2.png)

 ![9f5ad9c41e8a41b9b373bd27fc479306.png](https://img-blog.csdnimg.cn/9f5ad9c41e8a41b9b373bd27fc479306.png)

##  发送恢复告警信息

```
import json
import requests

new_packinf = [{
		'status': 'resolved',
		'labels': {
			'alertname': '主机存活状态警告！',
			'cloud': '乘风-Dev环境',
			'instance': '192.168.82.105:9100',
			'job': 'node_exporter',
			'severity': '非常严重',
			'team': 'ops'
		},
		'annotations': {
			'description': '192.168.82.105:9100:服务器延时超过5分钟',
			'summary': '192.168.82.105:9100:服务器宕机'
		},
		'startsAt': '2022-07-05T05:54:37.452Z',
		'endsAt': '2022-07-05T05:56:52.452Z',
		'generatorURL': 'http://prometheus-server.0101101300.fjf:9090/graph?g0.expr=up+%3D%3D+0&amp;g0.tab=1',
		'fingerprint': '4a890f7c225c3bef'
	}]
jsons = json.dumps(new_packinf)
url = "http://192.168.82.105:9093/api/v2/alerts"
headers = {'Content-Type': 'application/json'}
responses = requests.post(url=url, headers=headers, data=jsons)
print(responses.status_code, responses.url)
# print(responses.json())

```

![16a0b2ba1dc04d90b0325d634200fbb3.png](https://img-blog.csdnimg.cn/16a0b2ba1dc04d90b0325d634200fbb3.png)

 ![3198e394e11b408fa08d25390b373a75.png](https://img-blog.csdnimg.cn/3198e394e11b408fa08d25390b373a75.png)

```
import json
import requests
import time

year_time = time.strftime('%Y-%m-%d', time.localtime())
now_time = time.strftime('%H:%M:%S', time.localtime())
start_time = year_time + "T" + now_time + ".000+08:00"
is_end_time = False
if is_end_time:
    print("告警未解决")
    end_time = '0001-01-01T00:00:00Z'
else:
    print("告警已经解决")
    end_time = start_time
new_packinf = [{
    'labels': {
        'alertname': '主机存活状态警告！',
        'cloud': '小贷-Dev环境',
        'instance': '192.168.82.105:9100',
        'job': 'node_exporter',
        'severity': '非常严重',
        'team': 'ops'
    },
    'annotations': {
        'description': '192.168.82.105:9100:服务器延时超过5分钟',
        'summary': '192.168.82.105:9100:服务器宕机'
    },
    'endsAt': end_time,
}]
jsons = json.dumps(new_packinf)
url = "http://192.168.82.105:9093/api/v2/alerts"
headers = {'Content-Type': 'application/json'}
responses = requests.post(url=url, headers=headers, data=jsons)
print(responses.status_code, responses.url)
# print(responses.json())

```





# 钉钉告警模板

```
{<!-- -->{ $var := .externalURL}}{<!-- -->{ range $k,$v:=.alerts }}
{<!-- -->{if eq $v.status "resolved"}}
#### [Prometheus恢复信息]({<!-- -->{$v.generatorURL}})

##### &lt;font color="#02b340"&gt;告警名称&lt;/font&gt;：[{<!-- -->{$v.labels.alertname}}]({<!-- -->{$var}})
##### &lt;font color="#02b340"&gt;告警级别&lt;/font&gt;：{<!-- -->{$v.labels.severity}}
##### &lt;font color="#02b340"&gt;开始时间&lt;/font&gt;：{<!-- -->{TimeFormat $v.startsAt "2006-01-02 15:04:05"}}
##### &lt;font color="#02b340"&gt;结束时间&lt;/font&gt;：{<!-- -->{TimeFormat $v.endsAt "2006-01-02 15:04:05"}} 
##### &lt;font color="#02b340"&gt;实例地址&lt;/font&gt;：{<!-- -->{$v.labels.instance}}
##### &lt;font color="#02b340"&gt;主机名称&lt;/font&gt;：{<!-- -->{$v.labels.hostname}}

**{<!-- -->{$v.annotations.description}}**
{<!-- -->{else}}
#### [Prometheus告警信息]({<!-- -->{$v.generatorURL}})

##### &lt;font color="#FF0000"&gt;告警名称&lt;/font&gt;：[{<!-- -->{$v.labels.alertname}}]({<!-- -->{$var}})
##### &lt;font color="#FF0000"&gt;告警级别&lt;/font&gt;：{<!-- -->{$v.labels.severity}}
##### &lt;font color="#FF0000"&gt;开始时间&lt;/font&gt;：{<!-- -->{ TimeFormat $v.startsAt "2006-01-02 15:04:05"}}
##### &lt;font color="#FF0000"&gt;结束时间&lt;/font&gt;：{<!-- -->{TimeFormat $v.endsAt "2006-01-02 15:04:05"}} 
##### &lt;font color="#FF0000"&gt;实例地址&lt;/font&gt;：{<!-- -->{$v.labels.instance}}
##### &lt;font color="#FF0000"&gt;主机名称&lt;/font&gt;：{<!-- -->{$v.labels.hostname}}

**{<!-- -->{$v.annotations.description}}**
{<!-- -->{end}}
{<!-- -->{ end }}
{<!-- -->{ $urimsg:=""}}{<!-- -->{ range $key,$value:=.commonLabels }}{<!-- -->{$urimsg =  print $urimsg $key "%3D%22" $value "%22%2C" }}{<!-- -->{end}}[*** 点我屏蔽该告警]({<!-- -->{$var}}/#/silences/new?filter=%7B{<!-- -->{SplitString $urimsg 0 -3}}%7D)
```


