---
author: 南宫乘风
categories:
- Python学习
date: 2023-02-19 11:06:57
description: 背景：阿里云的服务器因为阿里云升级插件，导致安全防护程序重启，产生不同的端口。导致低自动发现注册的端口大量报警。解决：杀掉关于因为非业务变更的端口检测的触发器。相关文档：监控之主机端口监控自动发现监控。。。。。。。
image: http://image.ownit.top/4kdongman/16.jpg
tags:
- 阿里云
- 服务器
- 腾讯云
title: Python获取zabbix问题触发器
---

<!--more-->

背景：阿里云的ECS服务器因为阿里云升级插件，导致安全防护程序重启，产生不同的端口。导致低自动发现注册的端口 大量报警。

解决：杀掉关于因为非业务 变更的端口检测的触发器。

相关文档：

[Zabbix监控之主机端口监控自动发现](https://blog.csdn.net/pazzn/article/details/123405523 "Zabbix监控之主机端口监控自动发现")

# zabbix监控端口原理

一个个去添加listen监控tcp的话不现实啊，还是也搞自动发现吧

分割下来也是2步啊

第一步脚本丢[zabbix](https://so.csdn.net/so/search?q=zabbix&spm=1001.2101.3001.7020 "zabbix")\-agent下产生自定义键值

第二步不就是zabbix-server添加自动发现绑定这个键值咯

![](http://image.ownit.top/csdn/f66c00f538754f47bf0fed614a44d07c.png)

 

[什么是安骑士Agent插件？](https://help.aliyun.com/document_detail/31778.html "什么是安骑士Agent插件？")

[Agent 插件\_云安全中心（安骑士）-阿里云帮助中心](https://help.aliyun.com/document_detail/28456.html "Agent 插件_云安全中心（安骑士）-阿里云帮助中心")

# 解决思路

1、根据zabbix的api 获取的token

2、根据token获取到问题主机的触发器id

3、根据触发器id 删除相关的触发器，

4、消停大面积的告警

![](http://image.ownit.top/csdn/15634a75e62e40e286938f4106065706.png)

zabbix相关的API文档 可以查询官方文档或者博客

<https://www.cnblogs.com/rxysg/p/15700912.html> 

[Python调用Zabbix API接口批量修改（禁用/启用）触发器trigger\_啥是比亚的技术博客\_51CTO博客](https://blog.51cto.com/u_9499607/2481726 "Python调用Zabbix API接口批量修改（禁用/启用）触发器trigger_啥是比亚的技术博客_51CTO博客")

## 1、获取zabbix的token 

```python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 16:45
# @Author  : 南宫乘风
# @File    : zabbix_trigger.py
# @Software: PyCharm
import json
import os
import requests

url = "http://ip/zabbix/api_jsonrpc.php"  # 此处域名修改为相应的地址
headers = {
    'Content-Type': 'application/json-rpc'
}

tokens = '97553b7342457602a0a6452f0058c0ed'


def token_get():  # 根据账号密码获取token
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",  # zabbix管理员用户名
            "password": "密码"  # 账户密码
        },
        "auth": None,
        "id": 1
    }
    json_data = json.dumps(data)
    req = requests.post(url, data=json_data, headers=headers)
    js_req = req.json()
    print(js_req['result'])
    return js_req['result']
```

## 2、获取zabbix有问题主机触发器的id

```python

def hosts_get(token):  # 获取有问题主机的触发器id
    # data = {
    #     "jsonrpc": "2.0",
    #     "method": "host.get",
    #     "params": {
    #         "output": ["hostid", "name"],
    #         "filter": {
    #             # 筛选条件
    #             "value": 1,  # value值为1表示有问题
    #             "status": 0  # status为0表示已启用的trigger
    #         },
    #     },
    #
    #     "auth": token,
    #     "id": 1
    # }
    data = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            # output表示输出结果包含参数有哪些
            "output": [
                "triggerid",
                "description",
                "status",
                "value",
                "priority",
                "lastchange",
                "recovery_mode",
                "hosts",
                "state",
            ],
            "selectHosts": "hosts",  # 需包含主机ID信息，以便于根据主机ID查询主机信息
            "selectItems": "items",
            "filter": {
                # 筛选条件
                "value": 1,  # value值为1表示有问题
                "status": 0  # status为0表示已启用的trigger
            },
        },
        "auth": token,  # 这里的auth就是登录后获取的
        'id': '1'  # 这个id可以随意
    }
    json_data = json.dumps(data)
    req = requests.post(url, data=json_data, headers=headers)
    js_req = req.json()
    print(len(js_req['result']), js_req['result'])
    id_list = []
#判断 有问题的地自动发现的端口
    for item in js_req['result']:
        if 'PROCESS' in item['description']:
            id_list.append(item['triggerid'])
    print(len(id_list), id_list)
    return js_req['result']

```

## 3、删除触发器的ID

```python
def del_trigger(id):
    id_one = []
    ids = id_one.append(str(id))

    values = {

        "jsonrpc": "2.0",

        "method": "trigger.delete",

        "params": id_one,  # 触发器id

        "auth": tokens,

        "id": 1

    }
    json_data = json.dumps(values)
    req = requests.post(url, data=json_data, headers=headers)
    js_req = req.json()
    print(js_req)
    # return js_req['result']
```

完正代码

```python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 16:45
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : zabbix_trigger.py
# @Software: PyCharm
import json
import os
import requests

url = "http://ip/zabbix/api_jsonrpc.php"  # 此处域名修改为相应的地址
headers = {
    'Content-Type': 'application/json-rpc'
}

tokens = '97553b7342457602a0a6452f0058c0ed'


def token_get():  # 根据账号密码获取token
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",  # zabbix管理员用户名
            "password": "密码"  # 账户密码
        },
        "auth": None,
        "id": 1
    }
    json_data = json.dumps(data)
    req = requests.post(url, data=json_data, headers=headers)
    js_req = req.json()
    print(js_req['result'])
    return js_req['result']


def hosts_get(token):  # 获取所有主机信息
    # data = {
    #     "jsonrpc": "2.0",
    #     "method": "host.get",
    #     "params": {
    #         "output": ["hostid", "name"],
    #         "filter": {
    #             # 筛选条件
    #             "value": 1,  # value值为1表示有问题
    #             "status": 0  # status为0表示已启用的trigger
    #         },
    #     },
    #
    #     "auth": token,
    #     "id": 1
    # }
    data = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            # output表示输出结果包含参数有哪些
            "output": [
                "triggerid",
                "description",
                "status",
                "value",
                "priority",
                "lastchange",
                "recovery_mode",
                "hosts",
                "state",
            ],
            "selectHosts": "hosts",  # 需包含主机ID信息，以便于根据主机ID查询主机信息
            "selectItems": "items",
            "filter": {
                # 筛选条件
                "value": 1,  # value值为1表示有问题
                "status": 0  # status为0表示已启用的trigger
            },
        },
        "auth": token,  # 这里的auth就是登录后获取的
        'id': '1'  # 这个id可以随意
    }
    json_data = json.dumps(data)
    req = requests.post(url, data=json_data, headers=headers)
    js_req = req.json()
    print(len(js_req['result']), js_req['result'])
    id_list = []
    for item in js_req['result']:
        if 'PROCESS' in item['description']:
            id_list.append(item['triggerid'])
    print(len(id_list), id_list)
    return js_req['result']

#这边我做了个调试，如果想直接一次运行成功，建议自己改动 启动是的代码

id_lists = ['21284', '21244', '21249', '21275', '21264', '21278', '21262', '21263', '21266', '21270', '21272', '21276',
            '21277', '21279', '21267', '21269', '21254', '21282', '21287', '21268', '21273', '21274', '21285', '21289',
            '21283', '21286', '21290', '21251', '21250', '21243']


def del_trigger(id):
    id_one = []
    ids = id_one.append(str(id))

    values = {

        "jsonrpc": "2.0",

        "method": "trigger.delete",

        "params": id_one,  # 触发器id

        "auth": tokens,

        "id": 1

    }
    json_data = json.dumps(values)
    req = requests.post(url, data=json_data, headers=headers)
    js_req = req.json()
    print(js_req)
    # return js_req['result']


for i in id_lists:
    del_trigger(i)
```