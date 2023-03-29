# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 14:55
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : test.py
# @Software: PyCharm
import frontmatter

metadata_str = """
---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-09-15 10:56:40
description: 错误今天不知道怎么回事，一台机器的报错，也就是无法初始化正常解决办法移除这台主机多余的网卡和然后从重新删除这个错误的，就会恢复正常。。。。。。。
image: http://image.ownit.top/4kdongman/46.jpg
tags:
- 错误问题解决
- golang
- docker
- python
title: calico-node 报错calico/node is not ready BIRD is not ready BGP not established
  with
---
"""
metadata = frontmatter.loads(metadata_str)

print(metadata['title'])  # 输出：SpringBoot集成Apollo和自动注册Consul
print(metadata['date'])   # 输出：2023-03-27 10:18:30
print(metadata['tags'])   # 输出：2023-03-27 10:18:30
print(metadata['categories'])   # 输出：2023-03-27 10:18:30