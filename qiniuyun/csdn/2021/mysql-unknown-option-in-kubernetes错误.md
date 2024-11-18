---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-04-07 15:28:32
description: 错误问题原因：把的用户密码配置成，然后挂载，会一直报错，无法完成初始解决问题问题是我使用该命令创建了我的机密，而命令自动插入了结尾的换行符。使用代替。因此我没有注意到日志输出中有换行符。希望这可以帮助。。。。。。。
image: ../../title_pic/49.jpg
slug: '202104071528'
tags:
- 错误问题解决
title: mysql-unknown-option-in-kubernetes错误
---

<!--more-->

## **错误问题**

**原因：把MySQL的用户密码配置成secrets，然后挂载mysql，mysql会一直报错，无法完成初始**

```bash
Version: '5.7.33'  socket: '/var/run/mysqld/mysqld.sock'  port: 0  MySQL Community Server (GPL)
2021-04-07 15:06:32+08:00 [Note] [Entrypoint]: Temporary server started.
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
2021-04-07T07:06:58.526144Z 0 [Note] InnoDB: page_cleaner: 1000ms intended loop took 24159ms. The settings might not be optimal. (flushed=200 and evicted=0, during the time.)
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
2021-04-07 15:06:58+08:00 [Note] [Entrypoint]: Creating database wordpress
mysql: [ERROR] unknown option '--"'
```

![](../../image/20210407151922867.png)

## 解决问题

问题是我使用该`echo 'secret' | base64`命令创建了我的机密，而echo命令自动插入了结尾的换行符。

使用`echo \-n 'secret' | base64`代替。✔️

因此我没有注意到日志输出中有换行符。希望这可以帮助一些也使用echo命令对base64进行编码的人。

![](../../image/20210407152321646.png)

![](../../image/20210407152651461.png)

 

参考文章： <https://stackoverflow.com/questions/62985541/mysql-unknown-option-in-kubernetes#>