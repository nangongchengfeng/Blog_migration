+++
author = "南宫乘风"
title = "Python访问Apollo获取配置"
date = "2023-01-05 10:50:16"
tags=['python', '开发语言']
categories=['Python学习']
image = "post/4kdongman/55.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/128476370](https://blog.csdn.net/heian_99/article/details/128476370)

## 环境

操作系统 ： CentOS7.3.1611_x64

Python 版本 : 3.6.8

Apollo源码地址：

[GitHub - apolloconfig/apollo: Apollo is a reliable configuration management system suitable for microservice configuration management scenarios.](https://github.com/ctripcorp/apollo)

访问Apollo使用这个库：

[GitHub - filamoon/pyapollo: Python client for Ctrip's Apollo.](https://github.com/filamoon/pyapollo)

不要使用pypi提供的apollo库（是一个编辑器的库）。

其实真正需要的也就一个文件（pyapollo.py）：

[pyExamples/pyapollo.py at master · mike-zhang/pyExamples · GitHub](https://github.com/mike-zhang/pyExamples/blob/master/pyapolloRelate/pyapollo.py)



## 安装pyapollos

```
pip install pyapollos
```

注意注意注意：这个pyapollo库使用时会报链接超时，所以不要使用了 

这里是一个别人修改后的库, [github传送门](https://github.com/mike-zhang/pyExamples/blob/master/pyapolloRelate/pyapollo.py)，直接复制这个代码创建一个类使用就好了。

 参考文档：[https://blog.csdn.net/weixin_44809381/article/details/123072829](https://blog.csdn.net/weixin_44809381/article/details/123072829)

使用示例：

```
import time

import pyapollos

a = pyapollos.ApolloClient(app_id="movie-project", config_server_url="https://config-server-dev.ownit.top",
                           cluster='default', timeout=10)

#如果是关联空间的值，必须使用namespace ，指定空间名称
c = a.get_value("ops.appDomain", namespace="yunwei.common-public-config")
print(c)


#测试值
var code = "cb224f2d-8ec8-4d66-85cc-072fb64ea58d"

```

![8d15708abfcf4455ba819c3e089ed3dc.png](https://img-blog.csdnimg.cn/8d15708abfcf4455ba819c3e089ed3dc.png)



![8f2c696e05ec4d12a0b9a16d91604206.png](https://img-blog.csdnimg.cn/8f2c696e05ec4d12a0b9a16d91604206.png)



## 生产实战实例

配置环境变量：

```
import os

from pyapollo import ApolloClient

client = ApolloClient(app_id="spider-customer", cluster="default",
                      config_server_url='http://' + os.environ.get('APOLLO_CONFIG_URL'))

project_name = client.get_value('project.name')
# 服务
server_port = int(client.get_value('server.port'))
env = client.get_value('env')
# redis
redis_host = client.get_value('redis.host')
redis_port = int(client.get_value('redis.port'))
redis_db = int(client.get_value('redis.db'))
redis_password = client.get_value('redis.password')

# mysql
mysql_host = client.get_value('mysql.host')
mysql_port = int(client.get_value('mysql.port'))
mysql_user = client.get_value('mysql.user')
mysql_password = client.get_value('mysql.password')
mysql_database = client.get_value('mysql.database')

# 钉钉机器人
log_robot_token = client.get_value('log_robot_token')
log_robot_secret = client.get_value('log_robot_secret')

# oss
oss_endpoint = client.get_value('oss.ossEndpoint')
oss_accessKeyId = client.get_value('oss.ossAccessKeyId')
oss_accessKeySecret = client.get_value('oss.ossAccessKeySecret')
oss_bucketName = client.get_value('oss.bucketName')
```

## 二、调用API接口获取配置

### 1，通过带缓存的Http接口从Apollo读取配置

该接口会从缓存中获取配置，适合频率较高的配置拉取请求，如简单的每30秒轮询一次配置。

由于缓存最多会有一秒的延时，所以如果需要配合配置推送通知实现实时更新配置的话，请参考通过不带缓存的Http接口从Apollo读取配置
- Http接口说明
URL: {config_server_url}/configfiles/json/{appId}/{clusterName}/{namespaceName}?ip={clientIp}

Method: GET<br> 参数说明：

|参数名|是否必须|参数值|备注
|------
|config_server_url|是|Apollo配置服务的地址|
|appId|是|应用的appId|
|clusterName|是|集群名|一般情况下传入 default 即可。 如果希望配置按集群划分，可以参考[集群独立配置说明](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fctripcorp%2Fapollo%2Fwiki%2F%25E5%25BA%2594%25E7%2594%25A8%25E6%258E%25A5%25E5%2585%25A5%25E6%258C%2587%25E5%258D%2597%23%25E4%25B8%2589%25E9%259B%2586%25E7%25BE%25A4%25E7%258B%25AC%25E7%25AB%258B%25E9%2585%258D%25E7%25BD%25AE%25E8%25AF%25B4%25E6%2598%258E)做相关配置，然后在这里填入对应的集群名。
|namespaceName|是|Namespace的名字|如果没有新建过Namespace的话，传入application即可。 如果创建了Namespace，并且需要使用该Namespace的配置，则传入对应的Namespace名字。需要注意的是对于properties类型的namespace，只需要传入namespace的名字即可，如application。对于其它类型的namespace，需要传入namespace的名字加上后缀名，如datasources.json
|ip|否|应用部署的机器ip|这个参数是可选的，用来实现灰度发布。 如果不想传这个参数，请注意URL中从?号开始的query parameters整个都不要出现。

## 2，通过不带缓存的Http接口从Apollo读取配置

该接口会直接从数据库中获取配置，可以配合配置推送通知实现实时更新配置。
- Http接口说明
URL: {config_server_url}/configs/{appId}/{clusterName}/{namespaceName}?releaseKey={releaseKey}&amp;ip={clientIp}

Method: GET<br> 参数说明：

|参数名|是否必须|参数值|备注
|------
|config_server_url|是|Apollo配置服务的地址|
|appId|是|应用的appId|
|clusterName|是|集群名|一般情况下传入 default 即可。 如果希望配置按集群划分，可以参考[集群独立配置说明](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fctripcorp%2Fapollo%2Fwiki%2F%25E5%25BA%2594%25E7%2594%25A8%25E6%258E%25A5%25E5%2585%25A5%25E6%258C%2587%25E5%258D%2597%23%25E4%25B8%2589%25E9%259B%2586%25E7%25BE%25A4%25E7%258B%25AC%25E7%25AB%258B%25E9%2585%258D%25E7%25BD%25AE%25E8%25AF%25B4%25E6%2598%258E)做相关配置，然后在这里填入对应的集群名。
|namespaceName|是|Namespace的名字|如果没有新建过Namespace的话，传入application即可。 如果创建了Namespace，并且需要使用该Namespace的配置，则传入对应的Namespace名字。需要注意的是对于properties类型的namespace，只需要传入namespace的名字即可，如application。对于其它类型的namespace，需要传入namespace的名字加上后缀名，如datasources.json
|releaseKey|否|上一次的releaseKey|将上一次返回对象中的releaseKey传入即可，用来给服务端比较版本，如果版本比下来没有变化，则服务端直接返回304以节省流量和运算
|ip|否|应用部署的机器ip|这个参数是可选的，用来实现灰度发布。
