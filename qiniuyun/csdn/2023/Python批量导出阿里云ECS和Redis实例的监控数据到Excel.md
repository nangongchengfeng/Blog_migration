---
author: 南宫乘风
categories:
- Python学习
- 项目实战
date: 2023-04-12 10:53:54
description: 背景某公司使用阿里云的和服务作为其业务支撑，为了及时了解机器的使用情况，领导要求业务部门对所有阿里云机器的平均资源使用率进行统计，并汇总在一个表格中，以便领导查看和分析。需求为了满足领导的需求，我们需。。。。。。。
image: ../../title_pic/74.jpg
slug: '202304121053'
tags:
- python
- 阿里云
- redis
title: Python批量导出阿里云ECS和Redis实例的监控数据到Excel
---

<!--more-->

#  背景
某公司使用阿里云的 ECS 和 Redis 服务作为其业务支撑，为了及时了解机器的使用情况，领导要求业务部门对所有阿里云机器的平均资源使用率进行统计，并汇总在一个 Excel 表格中，以便领导查看和分析。
# 需求
为了满足领导的需求，我们需要实现以下基本需求：

1. 使用阿里云 Python SDK 获取所有 ECS 和 Redis 实例的 ID 和名称，以及机器的规格和资源使用情况等信息。

2. 使用阿里云监控服务 ECS、Redis API 获取实例的监控数据，并将其保存为 Python 字典类型。

3. 根据用户定义的时间范围，计算所有实例的平均资源使用率，并将其汇总到一个 Python 字典中。

4. 使用 Excel 处理库（例如 openpyxl），创建一个新的 Excel 文件，并在其中创建一个新的 sheet。

5. 将计算得到的数据写入到 Excel 文件中。在写入时，需要提取出每个实例的 ID、名称、规格、平均 CPU 使用率、平均内存使用率和平均网络带宽使用率等信息，并按照一定的格式写入到 Excel 文件的合适位置。

6. 最后，保存 Excel 文件并退出程序。用户应当能够方便地查看和使用导出的 Excel 表格，并根据需要进行数据分析和处理。

通过实现上述需求，业务部门可以较为方便和及时地了解到各个机器的使用情况，快速发现并解决资源使用过度或者资源浪费的问题，提高云计算资源的利用率和企业运营效率。同时，我们也能够充分发挥 Python 和阿里云 API 的强大能力，实现一个业务部门的全新 Python 项目，提升自己的编程能力和阿里云 API 使用经验。

# 环境
> Python 3.8 
> pip install alibabacloud_cms20190101==2.0.5
> 
> pip install alibabacloud_r_kvstore20150101==2.20.7

获取所有ECS和Redis 机器的资源使用率

**使用到的api接口**

**产品排列表** [https://cms.console.aliyun.com/metric-meta/acs_ecs_dashboard/ecs](https://cms.console.aliyun.com/metric-meta/acs_ecs_dashboard/ecs)
**获取所有机器** [https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMonitoringAgentHosts](https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMonitoringAgentHosts)
**获取所有redis**  [https://next.api.aliyun.com/api/R-kvstore/2015-01-01/DescribeInstancesOverview](https://next.api.aliyun.com/api/R-kvstore/2015-01-01/DescribeInstancesOverview)

**资源使用率获取** [https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMetricLast](https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMetricLast)
![在这里插入图片描述](../../image/14f84bd084ad4568887b8defa60d99dd.png)


# 实例数据获取（ECS和Redis）
可以参考下方的Api接口，我已经封装成函数 

**获取所有机器** [https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMonitoringAgentHosts](https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMonitoringAgentHosts)
**获取所有redsi**  [https://next.api.aliyun.com/api/R-kvstore/2015-01-01/DescribeInstancesOverview](https://next.api.aliyun.com/api/R-kvstore/2015-01-01/DescribeInstancesOverview)

**如果要使用下方函数，请添加自己的密钥对**
```python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 9:55
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ecs_all.py
# @Software: PyCharm
import json
from typing import List

from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_r_kvstore20150101.client import Client as R_kvstore20150101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_r_kvstore20150101 import models as r_kvstore_20150101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


def create_client_redis(
        access_key_id: str,
        access_key_secret: str,
) -> R_kvstore20150101Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'r-kvstore.aliyuncs.com'
    return R_kvstore20150101Client(config)


def create_client_ecs(
        access_key_id: str,
        access_key_secret: str,
) -> Cms20190101Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'metrics.ap-southeast-1.aliyuncs.com'
    return Cms20190101Client(config)


def get_ecs_instances():
    """
    获取阿里云 ECS 实例列表
    """
    client = create_client_ecs('xxxx', 'xxxx')
    describe_monitoring_agent_hosts_request = cms_20190101_models.DescribeMonitoringAgentHostsRequest()
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        data = client.describe_monitoring_agent_hosts_with_options(describe_monitoring_agent_hosts_request, runtime)
        return data
    except Exception as error:
        # 如有需要，请打印 error
        UtilClient.assert_as_string(error.message)


def get_redis_instances():
    # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
    client = create_client_redis('xxxx', 'xxxx')
    describe_instances_overview_request = r_kvstore_20150101_models.DescribeInstancesOverviewRequest(
        region_id='cn-shenzhen'
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        data = client.describe_instances_overview_with_options(describe_instances_overview_request, runtime)
        return data
    except Exception as error:
        # 如有需要，请打印 error
        UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    ecs_data = get_ecs_instances().to_map()
    redis_data = get_redis_instances().to_map()


    # 将 ECS 数据写入 JSON 文件中
    with open('ecs.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(ecs_data, indent=4,ensure_ascii=False))

    # 将 Redis 数据写入 JSON 文件中
    with open('redis.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(redis_data, indent=4,ensure_ascii=False))
    print("数据已经写入本地文件")

```
![在这里插入图片描述](../../image/1903b62297554dafbda334f1ce851245.png)
![在这里插入图片描述](../../image/b51eec5f74ab4b8a8796a81f2fe7d5e1.png)
# ECS实例资源
```python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 17:17
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ecs_monitor.py
# @Software: PyCharm
import json
import sys

from typing import List

from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from openpyxl import Workbook
from openpyxl.utils import get_column_letter


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Cms20190101Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'metrics.ap-southeast-1.aliyuncs.com'
        return Cms20190101Client(config)

    @staticmethod
    def main(parameter):
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('xxxx', 'xxxx')
        describe_metric_top_request = cms_20190101_models.DescribeMetricTopRequest(
            period='2592000',
            namespace='acs_ecs_dashboard',
            metric_name=parameter,
            orderby='Average',
            start_time='2023-03-12 00:00:00',
            end_time='2023-04-11 00:00:00',
            length='100',
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            data = client.describe_metric_top_with_options(describe_metric_top_request, runtime)
            return data
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


def get_host():
    global host_list
    # 打开 host.json 文件
    with open('ecs.json', 'r') as f:
        # 读取文件中的 JSON 数据
        data = json.load(f)
    # 输出读取到的数据

    host_list = data['body']["Hosts"]["Host"]
    host_list = [{k: v for k, v in d.items() if
                  k not in (
                      'isAliyunHost', 'NetworkType', 'InstanceTypeFamily', 'Region', 'AliUid', 'SerialNumber', 'EipId','EipAddress')}
                 for d in
                 host_list]
    print(host_list)
    return host_list


def ecs_dashboard(parameter):
    data_ecs = Sample.main(parameter)
    response_dict = data_ecs.body.to_map()
    data_Datapoints = json.loads(response_dict["Datapoints"])
    # for data in data_Datapoints:
    #     print(data)
    # print(type(data_Datapoints), data_Datapoints)
    return data_Datapoints


def set_workbook(ece_data_list):
    data = {
        'AgentVersion': '2.1.56',
        'HostName': 'xxx',
        'InstanceId': 'i-xxxxxxx',
        'IpGroup': 'xxxxxxxxxx',
        'OperatingSystem': 'Linux',
        'CPU_Average': 4.475,
        'Memory_Average': 20.499
    }

    # 新建一个 Workbook 对象
    wb = Workbook()

    # 获取第一个 sheet
    ws = wb.active

    # 获取最大行数
    max_row = ws.max_row
    # 设置表头
    headers = list(data.keys())
    for i, header in enumerate(headers, start=1):
        ws.cell(row=1, column=i).value = header

    # 写入数据
    for row_data in ece_data_list:
        # 写入数据
        max_row += 1
        for i, header in enumerate(row_data.keys(), start=1):
            column_letter = get_column_letter(i)
            cell_address = '{}{}'.format(column_letter, max_row)
            ws[cell_address] = row_data[header]

    # 保存文件
    wb.save('ECS_服务器资源.xlsx')


if __name__ == '__main__':
    host_list_data = get_host()

    es_monitor_list_cpu = ecs_dashboard("CPUUtilization")
    es_monitor_list_memory = ecs_dashboard("memory_usedutilization")

    # 匹配CPU
    # 遍历 list2，匹配 instanceId 并添加 Average 值到 list1 的对应字典中
    for d2 in es_monitor_list_cpu:
        for d1 in host_list_data:
            if d1['InstanceId'] == d2['instanceId']:
                d1['CPU_Average'] = d2['Average']
    # 匹配内存
    for d3 in es_monitor_list_memory:
        for d1 in host_list_data:
            if d1['InstanceId'] == d3['instanceId']:
                d1['Memory_Average'] = d3['Average']
    # 输出更新后的 list1
    # lst_sorted = sorted(host_list_data, key=lambda x: x['Memory_Average'], reverse=True)
    print(host_list_data)
    set_workbook(host_list_data)

```

![在这里插入图片描述](../../image/5805142c43d040cfbbe2d90a2a4d0064.png)

# Redis实例资源
```python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 17:17
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ecs_monitor.py
# @Software: PyCharm

# 产品排列表 https://cms.console.aliyun.com/metric-meta/acs_ecs_dashboard/ecs?spm=a2c4g.163515.0.0.27c776abvQGocz
# 获取所有机器 https://next.api.aliyun.com/api/Cms/2019-01-01/DescribeMonitoringAgentHosts?params={}&tab=DEBUG
# 获取所有redsi  https://next.api.aliyun.com/api/R-kvstore/2015-01-01/DescribeInstancesOverview?spm=a2c4g.473769.0.i0&lang=PYTHON&params={%22RegionId%22:%22cn-shenzhen%22}&tab=DEBUG
import json
import sys

from typing import List

from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from openpyxl import Workbook
from openpyxl.utils import get_column_letter


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Cms20190101Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'metrics.ap-southeast-1.aliyuncs.com'
        return Cms20190101Client(config)

    @staticmethod
    def main(parameter):
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('xxxx', 'xxx')
        describe_metric_top_request = cms_20190101_models.DescribeMetricTopRequest(
            period='2592000',
            namespace='acs_kvstore',
            metric_name=parameter,
            orderby='Average',
            start_time='2023-03-12 00:00:00',
            end_time='2023-04-11 00:00:00',
            length='100',
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            data = client.describe_metric_top_with_options(describe_metric_top_request, runtime)
            return data
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


def get_host():
    global host_list
    # 打开 host.json 文件
    with open('redis.json', 'r', encoding='utf-8') as f:
        # 读取文件中的 JSON 数据
        data = json.load(f)
    # 输出读取到的数据
    print(data)
    host_list = data['body']["Instances"]

    host_list = [{k: v for k, v in d.items() if
                  k not in ('ArchitectureType', 'EngineVersion', 'EndTime', 'ResourceGroupId', 'ZoneId', 'CreateTime',
                            'VSwitchId', 'InstanceClass', 'ConnectionDomain', 'VpcId', 'ChargeType', 'NetworkType',
                            'InstanceStatus', 'RegionId', 'InstanceType', 'SecondaryZoneId')}
                 for d in
                 host_list]
    return host_list


def ecs_dashboard(parameter):
    data_ecs = Sample.main(parameter)
    response_dict = data_ecs.body.to_map()
    data_Datapoints = json.loads(response_dict["Datapoints"])
    return data_Datapoints


def set_workbook(host_list_data):
    data = {
        'Capacity': 256,
        'InstanceId': 'r-xxxxx',
        'InstanceName': '大数据',
        'PrivateIp': 'xxxxxxxx',
        'Memory_Average': 15.719
    }

    # 新建一个 Workbook 对象
    wb = Workbook()

    # 获取第一个 sheet
    ws = wb.active

    # 获取最大行数
    max_row = ws.max_row

    # 设置表头
    headers = list(data.keys())
    for i, header in enumerate(headers, start=1):
        ws.cell(row=1, column=i).value = header

    # 写入数据
    for row_data in host_list_data:
        # 写入数据
        max_row += 1
        for i, header in enumerate(row_data.keys(), start=1):
            column_letter = get_column_letter(i)
            cell_address = '{}{}'.format(column_letter, max_row)
            ws[cell_address] = row_data[header]

    # 保存文件
    wb.save('Redis_服务器资源.xlsx')


if __name__ == '__main__':
    host_list_data = get_host()

    redis_monitor_list_Memory = ecs_dashboard("StandardMemoryUsage")

    # 匹配CPU
    # 遍历 list2，匹配 instanceId 并添加 Average 值到 list1 的对应字典中
    for d2 in redis_monitor_list_Memory:
        for d1 in host_list_data:
            if d1['InstanceId'] == d2['instanceId']:
                d1['Memory_Average'] = d2['Average']

    # # 输出更新后的 list1
    lst_sorted = sorted(host_list_data, key=lambda x: x['Memory_Average'], reverse=True)
    print(host_list_data)
    set_workbook(lst_sorted)

```


![在这里插入图片描述](../../image/2afc4c4ea0da4113a16e0cb56620bc92.png)

