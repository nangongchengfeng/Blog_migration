---
author: 南宫乘风
categories:
- Python学习
date: 2023-09-05 11:44:32
description: 引言是一款强大的堡垒机系统，可以有效管理和控制企业内部服务器的访问权限，提高网络安全性。本文将介绍如何使用编程语言，结合提供的接口，实现对跳板机的管理和操作。、什么是？是一种堡垒机系统，它提供了一种安。。。。。。。
image: ../../title_pic/55.jpg
slug: '202309051144'
tags:
- python
- 开发语言
title: Python调用Jumpserver的Api接口增删改查
---

<!--more-->

## 引言
Jumpserver是一款强大的堡垒机系统，可以有效管理和控制企业内部服务器的访问权限，提高网络安全性。本文将介绍如何使用Python编程语言，结合Jumpserver提供的API接口，实现对跳板机的管理和操作。
## 1、什么是Jumpserver？
Jumpserver是一种堡垒机系统，它提供了一种安全且集中的方式来管理和控制用户对服务器的访问权限。Jumpserver可以帮助企业实现统一认证、审计日志记录、权限管理等功能，从而提高网络安全性。
## 2、Jumpserver提供的API接口
Jumpserver提供了一组强大的API接口，可以实现对跳板机的管理和操作。这些API包括获取服务器列表、认证访问权限、执行命令和文件传输等功能，可以通过HTTP请求进行调用。

**目前使用的版本：v3.6.2**
不同步的版本，API 接口有变化

[https://docs.jumpserver.org/zh/v3/dev/rest_api/](https://docs.jumpserver.org/zh/v3/dev/rest_api/)
![在这里插入图片描述](../../image/28a7f8b5ba2444c4bf5cd0ece4225424.png)

![在这里插入图片描述](../../image/47ef7844228a447daa896934a18deacf.png)
## 3、Python中的HTTP请求库
在Python中，我们可以使用第三方的HTTP请求库，如requests库或http.client库，来发送HTTP请求并获取响应。这些库提供了简洁的接口，方便我们与Jumpserver的API进行交互。

requests库：
requests是一个功能强大、简单易用的第三方HTTP请求库，广泛应用于Python开发中。它提供了简洁的API，使得发送HTTP请求变得非常简单。使用requests库，我们可以发送各种类型的HTTP请求（GET、POST、PUT等），设置请求头、请求参数、请求体等，并能够获得服务器响应的状态码、内容等信息。

示例代码：
```python
import requests

# 发送GET请求并获取响应
response = requests.get('https://api.example.com/users')

# 获取响应内容
content = response.text

# 获取响应状态码
status_code = response.status_code
```
## 4、使用Python调用Jumpserver API进行认证
在使用Jumpserver的API之前，我们需要先进行认证。通常，Jumpserver会提供一个登录接口，我们可以使用用户名和密码进行登录，并获取到访问令牌（Access Token）。在后续的API请求中，我们需要将该访问令牌作为认证凭证。
[https://docs.jumpserver.org/zh/v3/dev/rest_api/#12](https://docs.jumpserver.org/zh/v3/dev/rest_api/#12)
![在这里插入图片描述](../../image/c1008d3ddd6c4967b15c691a6ebdba7e.png)
**推荐使用：Access Key方式 或者 Private Token**
![在这里插入图片描述](../../image/ab030453c9b945f7ac18252c5fb0da18.png)
![在这里插入图片描述](../../image/816375ce79d24d698d8c9f08ea051fd3.png)
```bash
docker exec -it jms_core /bin/bash
cd /opt/jumpserver/apps
python manage.py shell
from users.models import User
u = User.objects.get(username='admin')
u.create_private_token()
已经存在 private_token，可以直接获取即可
u.private_token
```

此处我才用双层验证方式
```python

KeyID = '77e76d19-141c-xxx-8d2b-xxxx'
SecretID = 'a04817bc-0bb1-439f-baa2-xxxx'
gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
ptivate_token = 'xxxxxxxxxx'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    # 'X-CSRFToken': 'eoLo2AVcQK5X1JQ392JHCzjZ8wPCWZJFJao5O9ObH8zQwtiPhGBzaOnNKjaENShf',
    "Authorization": 'Token ' + ptivate_token,
    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
    'Date': datetime.datetime.utcnow().strftime(gmt_form)
}


# 认证
def get_auth(KeyID, SecretID):
    """
    认证
    :param KeyID:  The key ID
    :param SecretID:    The secret ID
    :return:
    """
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
    return auth


auth = get_auth(KeyID, SecretID)

```
## 5、Jumpserver接口自动调用
 **获取所有用户**
 ```python
# 获取所有用户
def get_user_all():
    """
    获取所有用户
    :return:
    """
    url = jms_url + '/api/v1/users/users/'
    response = requests.get(url, auth=auth, headers=headers)
    user_list = json.loads(response.text)
    count = 0
    for i in user_list:
        count += 1
        print(i)
    print(count)

```
![在这里插入图片描述](../../image/4878517ec7d6434da545568bdc9fe292.png)
**获取监控指标**

```python
# 获取监控指标
def get_prometheus_metric():
    """
    获取监控指标
    :return:
    """
    url = jms_url + "/api/v1/prometheus/metrics/"
    response = requests.get(url, headers=headers, auth=auth)
    print(response.text)
    return response.text
   ```

**获取所有资产节点**
```python
# 获取所有资产节点
def get_node_all():
    """
    获取所有资产节点
    :return:
    """
    url = jms_url + "/api/v1/assets/nodes/"
    response = requests.get(url, headers=headers, auth=auth)
    node_list = json.loads(response.text)
    count = 0
    for i in node_list:
        count += 1
        print(i)
    print(count)
    return response.json()

```
**查看当前token（即admin）的所有资产**
```python
def get_asset_all():
    """
    查看当前token（即admin）的所有资产
    :return:
    """
    url = jms_url + "/api/v1/assets/assets/"
    response = requests.get(url, headers=headers, auth=auth)
    node_list = json.loads(response.text)
    count = 0
    for i in node_list:
        count += 1
        print(i)
    print(count)
    return response.json()
```
**创建资产节点**
```python
def assets_nodes_create(node_name):
    """
    创建资产节点
    :param node_name:
    :return:
    """
    node_data = {
        "value": node_name
    }
    url = jms_url + "/api/v1/assets/nodes/"
    node_info = get_node_info(node_name)
    if node_info:  # 根据node_name去查询，如果查到了说明已经有了。
        print("{name}已存在, id: {id}".format(name=node_name, id=node_info[0]["id"]))
    else:
        data = json.dumps(node_data)
        resp = requests.post(url, headers=headers, data=data)
        return resp.json()

```
**根据ip获取资产信息**
```python
def get_assets_list_by_ip(ip):
    """
    根据ip获取资产信息
    :param ip:
    :return:
    """
    url = jms_url + "/api/v1/assets/assets/"
    response = requests.get(url, headers=headers, params={
        "ip": ip
    })
    print(response.json())
    return response.json()
```

**查看资产节点信息**


```python
def get_node_info(node_name):
    """
    查看资产节点信息
    :param node_name:   节点名称
    :return:
    """
    url = jms_url + "/api/v1/assets/nodes/"
    response = requests.get(url, auth=auth, headers=headers, params={
        "value": node_name
    })
    print(response.text)
    return response.json()
```


**创建资产机器**
```python

# 创建资产机器
def asset_create(ip, hostname, node_id, comment):
    """
    创建资产机器
    :param ip:  ip地址
    :param hostname:   主机名
    :param node_id:   节点id
    :return:    返回创建的资产信息
    """
    asset_Data = {
        "name": hostname,
        "address": ip,
        "platform": "1",
        "protocols": [{

            "name": "ssh",
            "port": 22
        }],
        "is_active": True,
        "nodes": [node_id],
        "comment": comment,
        "accounts": [{
            # 账号模板id
            "template": "60b11033-a6e1-467d-8388-68a0e64134ff",
        }]
    }
    url = jms_url + "/api/v1/assets/hosts/"
    print(url)
    data = json.dumps(asset_Data)
    print(data)
    response = requests.post(url, auth=auth, headers=headers, data=data)
    print(response.text)

```
**运行创建服务器资产**
```python

# 运行创建服务器资产
def run_create_assets(node_name, project_name, ip, comment):
    """
    运行创建服务器资产
    :param node_name:  节点名称
    :param project_name:  机器名称
    :param ip:  ip地址
    :param comment:  备注
    :return:
    """
    # 节点id，无节点时创建节点
    node_info = get_node_info(node_name)

    # 如果len(node_info) == 0 说明没有节点，需要创建节点
    if len(node_info) == 0:
        # 创建节点
        node_id = assets_nodes_create(node_name)
        print(node_id)
    else:
        # 获取节点id
        node_id = node_info[0]["id"]
        print(node_id)
    # 管理用户 id
    hostname = "{ip}_{project_name}".format(ip=ip, project_name=project_name)
    # 查IP,创建资产
    ip_info = get_assets_list_by_ip(ip)
    if ip_info:
        print("%s 已存在，nodes: %s" % (ip_info[0]["address"], ip_info[0]["nodes"]))
    else:
        asset_create(ip, hostname, node_id, comment)

```
**获取组织信息**
```python

def get_org_info():
    """
    获取组织信息
    :return:
    """
    url = jms_url + "/api/v1/orgs/orgs/"
    response = requests.get(url, headers=headers)
    org_list = response.text
    print(org_list)
    for i in org_list.split("id"):
        print(i)

    return response.json()
```

## 6、完整代码
```python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/29 14:21
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : jms_add.py
# @Software: PyCharm


import requests, datetime, json
from httpsig.requests_auth import HTTPSignatureAuth

KeyID = '77e76d19-141c-4545--xxx'
SecretID = 'a04817bc-0bb1-439f-baa2-xxxx'
gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
ptivate_token = 'xxxxx'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    # 'X-CSRFToken': 'eoLo2AVcQK5X1JQ392JHCzjZ8wPCWZJFJao5O9ObH8zQwtiPhGBzaOnNKjaENShf',
    "Authorization": 'Token ' + ptivate_token,
    'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
    'Date': datetime.datetime.utcnow().strftime(gmt_form)
}


# 认证
def get_auth(KeyID, SecretID):
    """
    认证
    :param KeyID:  The key ID
    :param SecretID:    The secret ID
    :return:
    """
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=KeyID, secret=SecretID, algorithm='hmac-sha256', headers=signature_headers)
    return auth


auth = get_auth(KeyID, SecretID)


# 获取所有用户
def get_user_all():
    """
    获取所有用户
    :return:
    """
    url = jms_url + '/api/v1/users/users/'
    response = requests.get(url, auth=auth, headers=headers)
    user_list = json.loads(response.text)
    count = 0
    for i in user_list:
        count += 1
        print(i)
    print(count)


# 获取监控指标
def get_prometheus_metric():
    """
    获取监控指标
    :return:
    """
    url = jms_url + "/api/v1/prometheus/metrics/"
    response = requests.get(url, headers=headers, auth=auth)
    print(response.text)
    return response.text


# 获取所有资产节点
def get_node_all():
    """
    获取所有资产节点
    :return:
    """
    url = jms_url + "/api/v1/assets/nodes/"
    response = requests.get(url, headers=headers, auth=auth)
    node_list = json.loads(response.text)
    count = 0
    for i in node_list:
        count += 1
        print(i)
    print(count)
    return response.json()


# 查看当前token（即admin）的所有资产
def get_asset_all():
    """
    查看当前token（即admin）的所有资产
    :return:
    """
    url = jms_url + "/api/v1/assets/assets/"
    response = requests.get(url, headers=headers, auth=auth)
    node_list = json.loads(response.text)
    count = 0
    for i in node_list:
        count += 1
        print(i)
    print(count)
    return response.json()


###################################################################################################
# 创建资产节点
def assets_nodes_create(node_name):
    """
    创建资产节点
    :param node_name:
    :return:
    """
    node_data = {
        "value": node_name
    }
    url = jms_url + "/api/v1/assets/nodes/"
    node_info = get_node_info(node_name)
    if node_info:  # 根据node_name去查询，如果查到了说明已经有了。
        print("{name}已存在, id: {id}".format(name=node_name, id=node_info[0]["id"]))
    else:
        data = json.dumps(node_data)
        resp = requests.post(url, headers=headers, data=data)
        return resp.json()


#
def get_assets_list_by_ip(ip):
    """
    根据ip获取资产信息
    :param ip:
    :return:
    """
    url = jms_url + "/api/v1/assets/assets/"
    response = requests.get(url, headers=headers, params={
        "ip": ip
    })
    print(response.json())
    return response.json()


# 查看资产节点信息
def get_node_info(node_name):
    """
    查看资产节点信息
    :param node_name:   节点名称
    :return:
    """
    url = jms_url + "/api/v1/assets/nodes/"
    response = requests.get(url, auth=auth, headers=headers, params={
        "value": node_name
    })
    print(response.text)
    return response.json()


# 创建资产机器
def asset_create(ip, hostname, node_id, comment):
    """
    创建资产机器
    :param ip:  ip地址
    :param hostname:   主机名
    :param node_id:   节点id
    :return:    返回创建的资产信息
    """
    asset_Data = {
        "name": hostname,
        "address": ip,
        "platform": "1",
        "protocols": [{

            "name": "ssh",
            "port": 22
        }],
        "is_active": True,
        "nodes": [node_id],
        "comment": comment,
        "accounts": [{
            # 账号模板id
            "template": "60b11033-a6e1-467d-8388-68a0e64134ff",
        }]
    }
    url = jms_url + "/api/v1/assets/hosts/"
    print(url)
    data = json.dumps(asset_Data)
    print(data)
    response = requests.post(url, auth=auth, headers=headers, data=data)
    print(response.text)


# 运行创建服务器资产
def run_create_assets(node_name, project_name, ip, comment):
    """
    运行创建服务器资产
    :param node_name:  节点名称
    :param project_name:  机器名称
    :param ip:  ip地址
    :param comment:  备注
    :return:
    """
    # 节点id，无节点时创建节点
    node_info = get_node_info(node_name)

    # 如果len(node_info) == 0 说明没有节点，需要创建节点
    if len(node_info) == 0:
        # 创建节点
        node_id = assets_nodes_create(node_name)
        print(node_id)
    else:
        # 获取节点id
        node_id = node_info[0]["id"]
        print(node_id)
    # 管理用户 id
    hostname = "{ip}_{project_name}".format(ip=ip, project_name=project_name)
    # 查IP,创建资产
    ip_info = get_assets_list_by_ip(ip)
    if ip_info:
        print("%s 已存在，nodes: %s" % (ip_info[0]["address"], ip_info[0]["nodes"]))
    else:
        asset_create(ip, hostname, node_id, comment)


def get_org_info():
    """
    获取组织信息
    :return:
    """
    url = jms_url + "/api/v1/orgs/orgs/"
    response = requests.get(url, headers=headers)
    org_list = response.text
    print(org_list)
    for i in org_list.split("id"):
        print(i)

    return response.json()


if __name__ == '__main__':
    jms_url = 'https://jms.xxx.top'
    username = 'admin'
    password = 'xxxxxx'

    # 获取token
    # token = get_token(jms_url, username, password)

    # 创建资产节点
    # assets_nodes_create("k8s")

    # 根据ip获取资产信息
    # get_assets_list_by_ip("192.168.11.10")

    # 查看资产节点信息
    # get_node_info("k8s")

    # 创建资产调用
    # node_id = ["e8641c37-93e3-450e-aaf8-64d5baa69753"]
    # get_node_info("k8s")
    # asset_create(ip, hostname, node_id)

    # 运行创建服务器资产
    # run_create_assets("test", "风控", "192.168.11.10", "测试")

    # 获取组织信息
    # get_org_info()

    # 获取所有用户
    get_user_all()

```
![在这里插入图片描述](../../image/e5ed8b4b374946e6832159b584b39279.png)

