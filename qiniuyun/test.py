# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 14:55
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : test.py
# @Software: PyCharm
import frontmatter

metadata_str = """
---
---
title: 集群服务器的网络连接状态接入ELK（可视化操作）
date: 2021-11-22 15:36:12
tags:  Linux实战操作 zookeeper java Kubernetes
categories: 项目实战
---
---
"""
metadata = frontmatter.loads(metadata_str)

print(metadata['title'])  # 输出：SpringBoot集成Apollo和自动注册Consul
print(metadata['date'])   # 输出：2023-03-27 10:18:30
print(metadata['tags'])   # 输出：2023-03-27 10:18:30
print(metadata['categories'])   # 输出：2023-03-27 10:18:30