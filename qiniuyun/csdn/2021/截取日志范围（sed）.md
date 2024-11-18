---
author: 南宫乘风
categories:
- 错误问题解决
date: 2021-11-03 16:53:26
description: 后续补充截取某个时间段到某个时间段的日志截取某个时间段到现在的。。。。。。。
image: ../../title_pic/60.jpg
slug: '202111031653'
tags:
- apache
title: 截取日志范围（sed）
---

<!--more-->

 

后续补充

```bash
sed  -n  '/2021-02-13 21:00:00/,/2021-02-13 22:00:00/p'   /usr/local/apache-tomcat-6.0.45/logs/crm.log   > /opt/crm-`date +%Y-%m-%d-%H-%M`.log
截取某个时间段到某个时间段的日志    
sed  -n  '/2021-01-18 21:10:00/,$p'   /usr/local/apache-tomcat-6.0.45/logs/crm.log   > /opt/crm-`date +%Y-%m-%d-%H-%M`.log 
截取某个时间段到现在的
```