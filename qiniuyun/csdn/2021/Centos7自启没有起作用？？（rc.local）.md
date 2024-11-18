---
author: 南宫乘风
categories:
- 错误问题解决
date: 2021-07-26 16:39:52
description: 今天机器重启，但是以前加的自启任务的脚本没有执行原因：在中文件的权限被降低了没有执行权限需要给它添加可执行权限。然后就可以在里面添加你要开机自启的命令了。。。。。。。
image: ../../title_pic/34.jpg
slug: '202107261639'
tags:
- Linux
- 自启
title: Centos7 自启没有起作用？？（rc.local）
---

<!--more-->

今天机器重启，但是以前加的自启任务的脚本没有执行

**原因：**

在centos7中,/etc/rc.d/rc.local文件的权限被降低了,没有执行权限,需要给它添加可执行权限。

```bash
chmod +x /etc/rc.d/rc.local
```

  
然后就可以在里面添加你要开机自启的命令了

```bash
vi /etc/rc.d/rc.local
```

![](../../image/20210726163905909.png)