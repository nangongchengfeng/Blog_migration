---
author: 南宫乘风
categories:
- Python学习
date: 2022-12-19 10:44:22
description: 简介：使用阿里云的数据库，开启的数据库治理服务。会产生大量的审计日志。我们有的审计日志数据，保留天，每小时收费空间：元小时计算下来：元解决：打算数据量存储天，以前的审计日志，可以使用阿里云的调用，下载。。。。。。。
image: http://image.ownit.top/4kdongman/36.jpg
tags:
- 数据库
- 大数据
title: Python本地下载-实例的SQL审计日志
---

<!--more-->

简介：使用阿里云的RDS数据库，开启DAS的数据库治理服务。会产生大量的审计日志。

我们有2T的审计日志数据，保留180天，每小时收费空间：0.008元/GB/小时

计算下来：2x1024x 24x 30 x 0.008 =11796 元

![](http://image.ownit.top/csdn/9193e553411f48338b950fa990047f2e.png)

 解决：打算数据量存储30天，以前的审计日志，可以使用阿里云的API 调用，下载，归档报错。如果出现问题，可以及时定位。保留周期更长。费用更少。

阿里云API接口：[查询实例的SQL审计日志 \(aliyun.com\)](https://help.aliyun.com/document_detail/26294.htm?spm=a2c4g.11186623.0.0.44a05d7amIPH4t#t8148.html "查询实例的SQL审计日志 (aliyun.com)")

![](http://image.ownit.top/csdn/cbb1db8a9c824c658ec83a13e4a77564.png)

 目前使用这个API接口拉取，基本相关信息已经存在。

高级一点可以采用 一下API拉取日志

[按照访问来源统计全量请求数据的API接口\_数据库自治服务-阿里云帮助中心](https://help.aliyun.com/document_detail/443053.html "按照访问来源统计全量请求数据的API接口_数据库自治服务-阿里云帮助中心")

[GetFullRequestStatResultByInstanceId \- 按照SQL ID异步统计全量请求数据 \(aliyun.com\)](https://help.aliyun.com/document_detail/443054.html "GetFullRequestStatResultByInstanceId \- 按照SQL ID异步统计全量请求数据 (aliyun.com)")

# 环境准备

1、Python 3.8 的环境

2、安装阿里云的sdk

        SDK 包名称alibabacloud\_rds20140815

        SDK 版本2.1.2

        SDK 包管理平台pypi

SDK 安装命令

```
pip install alibabacloud_rds20140815==2.1.2
```

提示仓库同步可能会有延迟，如果遇到版本不存在的情况，请稍后再试或使用上一个版本

[阿里云 OpenAPI 开发者门户 \(aliyun.com\)](https://next.api.aliyun.com/api/Rds/2014-08-15/DescribeSQLLogRecords?lang=PYTHON "阿里云 OpenAPI 开发者门户 (aliyun.com)")

# 基础代码

此代码是阿里云自动生成的

![](http://image.ownit.top/csdn/645558bb06614fe68861efd55b777377.png)

一个执行，一个异步执行。选择其中一个即可。 

```bash
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_rds20140815 import models as rds_20140815_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Rds20140815Client:
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
        config.endpoint = f'rds.aliyuncs.com'
        return Rds20140815Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        describe_sqllog_records_request = rds_20140815_models.DescribeSQLLogRecordsRequest(
            dbinstance_id='xxxxxx',
            start_time='2022-11-18T00:00:00Z',
            end_time='2022-11-19T00:00:00Z',
            page_size=100,
            page_number=1
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.describe_sqllog_records_with_options(describe_sqllog_records_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        describe_sqllog_records_request = rds_20140815_models.DescribeSQLLogRecordsRequest(
            dbinstance_id='xxxxxx',
            start_time='2022-11-18T00:00:00Z',
            end_time='2022-11-19T00:00:00Z',
            page_size=100,
            page_number=1
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.describe_sqllog_records_with_options_async(describe_sqllog_records_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
```

 

# 2、根据小时拉去代码

因为数据量很大，我们准备根据  **小时 ** 拉去日志。

![](http://image.ownit.top/csdn/b5842cfe585a4eb883d5ed58cceae6e9.png)

 代码介绍：

根据每小时拉去文件，进行按时间保存，拉去一天的量完成后 会钉钉通知

```bash
import datetime
import json
import os
import sys
from time import sleep

import requests
from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_rds20140815 import models as rds_20140815_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

import copy


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Rds20140815Client:
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
        config.endpoint = f'rds.aliyuncs.com'
        return Rds20140815Client(config)

    @staticmethod
    def main(page_number=1, startTime=None, endTime=None):
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('xxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxx')
        describe_sqllog_records_request = rds_20140815_models.DescribeSQLLogRecordsRequest(
            #数据库实例ID
            dbinstance_id='rm-xxxxxxxxxxxxxxxxx',
            end_time=endTime,
            start_time=startTime,
            page_size=100,
            page_number=page_number
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            data = client.describe_sqllog_records_with_options(describe_sqllog_records_request, runtime)
            return data
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


def msg(text):
    json_text = {
        "msgtype": "text",
        "at": {
            "atMobiles": [
                "11111"
            ],
            "isAtAll": False
        },
        "text": {
            "content": text
        }
    }
    print(requests.post(api_url, json.dumps(json_text), headers=headers).content)


if __name__ == '__main__':
    startTime = '2022-11-19T00:00:00Z'
    for i in range(24):
        endTime = (datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(
            hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        rds_time = datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%SZ")
        rds_time_file_log = rds_time.strftime("%Y-%m-%d_%H")  # print(rds_time_file)
        rds_file = rds_time.strftime("%Y-%m-%d")  # print(rds_time_file)
        folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), rds_file)
        print(folder)
        log_path = os.path.exists(folder)
        if not log_path:
            os.makedirs(folder)

        print(startTime, endTime)
        rds = Sample.main(startTime=startTime, endTime=endTime)
        # 总条数
        rds_num = rds.body.total_record_count

        # 页数
        rds_page = rds.body.page_number

        # page的num数量
        pag_num_max = 100
        # 每页返回的数值
        page_record_count = rds.body.page_record_count

        # 总页数
        page_num_sum = int(rds_num / pag_num_max) + 1

        rds_log = rds.body.items.to_map()
        for i in range(page_num_sum + 1):
            print(i + 1)
            num = i + 1
            rds_one = Sample.main(page_number=num, startTime=startTime, endTime=endTime)
            page_record_count_one = rds_one.body.page_record_count
            if page_record_count_one != 0:
                rds_log_one = rds_one.body.items.to_map()
                # 获取rds 的真实日志数据
                for v in rds_log_one['SQLRecord']:
                    with open(folder + '/' + 'rds_' + rds_time_file_log + '.log', 'a', encoding="utf-8") as f:
                        f.write(f"{str(v)} \n")
            if (i + 1) % 2000 == 0:
                sleep(10)
        f.close()

        startTime = endTime  # 参数days=1（天+1） 可以换成 minutes=1（分钟+1）、seconds=1（秒+1）

    token = "xxxxxxxxxxxxxxxxxxxxxxxx"
    text = "python拉去数据"

    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % token
    msg('RDS数据拉去-完成告警')
```