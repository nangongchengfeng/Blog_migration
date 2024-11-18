---
author: 南宫乘风
categories:
- Python学习
- 项目实战
- Jenkins
date: 2023-06-17 18:26:30
description: 、背景日志是非常重要的信息资源。它们记录了应用程序的运行状态、错误和异常情况，帮助我们了解系统的健康状况以及发现潜在的问题。为了高效地管理和分析日志数据，许多组织采用了、和堆栈作为日志收集和分析的解决。。。。。。。
image: ../../title_pic/10.jpg
slug: '202306171826'
tags:
- python
- 钉钉
- 机器人
title: 提高错误日志处理效率！使用Python和钉钉机器人实现自动告警聚合
---

<!--more-->

## 1、背景
日志是非常重要的信息资源。它们记录了应用程序的运行状态、错误和异常情况，帮助我们了解系统的健康状况以及发现潜在的问题。为了高效地管理和分析日志数据，许多组织采用了Elasticsearch、Logstash和Kibana（ELK）堆栈作为日志收集和分析的解决方案。

开发一个实时监控和告警脚本，专门用于监控ELK平台中的错误日志，并及时发送告警通知给相关人员。该系统将通过扫描Elasticsearch中的日志数据，筛选出等级为ERROR的错误日志，并根据预设的告警规则进行处理。
## 2、目的
使用Python从Elasticsearch中查询特定级别为ERROR的错误日志，并通过钉钉机器人实现告警聚合和发送，以提高错误日志的处理效率和及时响应能力。

为什么开发这个脚本？
因为目前我们这边没有监控日志的信息，出现问题不能及时发现 和预知
**优势**
1、消息进行聚合，每个项目的多条告警信息，汇总一条发送。突破钉钉机器人每分钟只能发送20条的限制
2、告警信息you太多的重复，进行去重处理，添加告警次数发送。防止被钉钉限流
![在这里插入图片描述](../../image/11257bf3bf2a44a399601d3731b2842b.png)


## 3、原理
1. 使用Python的Elasticsearch库连接到Elasticsearch集群。
2. 构建Elasticsearch查询DSL（领域专用语言），过滤出级别为ERROR的日志记录。
3. 执行查询并获取结果。
4. 对查询结果进行聚合，统计每个项目的错误次数。
5. 根据聚合结果，生成告警消息的Markdown格式内容。
6. 使用钉钉机器人发送告警消息到指定的钉钉群。

## 4、流程
1. 导入必要的Python库，包括`elasticsearch`和`requests`。
2. 创建Elasticsearch连接，指定Elasticsearch集群的主机和端口。
3. 构建Elasticsearch查询DSL，设置查询条件为日志级别为ERROR。
4. 执行查询，获取查询结果。
5. 对查询结果进行处理，聚合每个项目的错误次数。
6. 根据聚合结果生成告警消息的Markdown内容。
7. 使用钉钉机器人API发送告警消息到指定的钉钉群。

## 5、实现代码
![在这里插入图片描述](../../image/49e71e0494aa4c47a10f525b2e547de4.png)


```bash

# -*- coding: utf-8 -*-
# @Time    : 2023/6/17 18:11
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : all_es.py
# @Software: PyCharm
from collections import Counter
from datetime import datetime, timedelta

import requests
from elasticsearch import Elasticsearch

from monitor.es_ding import send_pretty_message

# Elasticsearch客户端实例
es = Elasticsearch(hosts=['http://172.18.xxx.xxxx:9200'], http_auth=('elastic', 'xxxxx'),
                   sniff_on_start=True,  # 连接前测试
                   sniff_on_connection_fail=True,  # 节点无响应时刷新节点
                   sniff_timeout=300,  # 设置超时时间
                   headers={'Content-Type': 'application/json'})


def format_timestamp(timestamp):
    """格式化时间为Elasticsearch接受的字符串格式"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def search_errors():
    """执行查询，获取错误日志数据"""
    current_time = datetime.now()
    one_minute_ago = current_time - timedelta(minutes=10)
    current_time_str = format_timestamp(current_time)
    one_minute_ago_str = format_timestamp(one_minute_ago)

    index = 'app-prod-*'  # 替换为实际的索引名称

    query = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": one_minute_ago_str,
                                "lt": current_time_str,
                                "format": "yyyy-MM-dd HH:mm:ss",
                                "time_zone": "+08:00"
                            }
                        }
                    },
                    {
                        "match": {
                            "loglevel": "ERROR" #匹配项目错误等级
                        }
                    },
                    {
                        "bool": {
                            "must_not": [
                                {
                                    "match": {
                                        "projectname": "fox-data-spiderman" # 需要屏蔽的项目
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "_source": [  ## 输出的字段
            "date",
            "projectname",
            "threadname",
            "msg"
        ],
        "from": 0,
        "size": 10000, # 返回查询的条数
    }

    result = es.search(index=index, body=query)
    total_documents = result["hits"]["total"]["value"]
    print(f"总共匹配到 {total_documents} 条文档")

    result = result['hits']['hits']
    all_result = []

    for i in result:
        all_result.append(i['_source'])

    msg_counter = Counter(d['msg'] for d in all_result if 'msg' in d)
    results = []

    for d in all_result:
        if 'msg' in d and d['msg'] in msg_counter:
            count = msg_counter[d['msg']]
            del msg_counter[d['msg']]
            d['count'] = count
            d['msg'] = d['msg'][:100] + ('...' if len(d['msg']) > 100 else '')
            results.append(d)

    return results


def aggregate_errors(results):
    """按项目名称聚合错误日志"""
    aggregated_data = {}
    for d in results:
        projectname = d.get('projectname')
        if projectname:
            if projectname not in aggregated_data:
                aggregated_data[projectname] = []
            aggregated_data[projectname].append({'date': d.get('date'), 'msg': d.get('msg'), 'count': d.get('count')})
    return aggregated_data


def generate_summary(projectname, messages):
    """生成Markdown格式的消息摘要"""
    markdown_text = f'### {projectname} \n\n'
    for message in messages:
        markdown_text += f"**时间：** {message['date']}\n\n"
        markdown_text += f"**告警次数：** <font color='red'><b>{message['count']}</b></font>\n\n"
        markdown_text += f"{message['msg']}\n\n---\n\n"
    return markdown_text


def send_message_summary(projectname, messages):
    """发送摘要消息给钉钉机器人"""
    summary = generate_summary(projectname, messages)
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': f'{projectname}消息告警',
            'text': summary
        }
    }
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxx'  # 替换为实际的Webhook URL
    response = requests.post(webhook_url, json=data)
    if response.status_code == 200:
        print('消息发送成功')
    else:
        print('消息发送失败')


if __name__ == '__main__':
    errors = search_errors()
    aggregated_errors = aggregate_errors(errors)

    for projectname, messages in aggregated_errors.items():
        print(f"{projectname}:")
        print(messages)

```
![在这里插入图片描述](../../image/684241db386e487ca34773314919cb22.png)
## 6、Crontab添加定时任务
也可以用采用：Jenkins与GitLab的定时任务工作流程
https://blog.csdn.net/heian_99/article/details/131164591?spm=1001.2014.3001.5501

```bash
#日志
*/2 * * * * cd /python_app/elasticsearch; /opt/anaconda3/envs/py38/bin/python -u  es_monitor.py >> es_error_info.log 2>&1

```
该定时任务的含义是每隔2分钟执行一次指定目录下的 es_monitor.py 脚本，并将输出信息追加到 es_error_info.log 文件中。这样可以定期监控 Elasticsearch 的错误日志，并记录相关信息以便后续查看和分析。
## 7、总结
本博客，为我们构建了一个完整的应用日志监控和告警系统，通过ELK技术栈和钉钉机器人的结合，使得我们能够及时发现和处理应用中的错误，提高了团队的工作效率和系统的稳定性。

