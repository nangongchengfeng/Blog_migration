---
author: 南宫乘风
categories:
- Linux实战操作
date: 2020-03-14 21:26:47
description: 占内存的程序命令占的程序命令。。。。。。。
image: http://image.ownit.top/4kdongman/27.jpg
tags:
- Linux
- 内存
- CPU
- 查询
title: Linux查看占用CPU和内存的 的程序
---

<!--more-->

占内存的程序命令

```bash
 ps aux | head -1;ps aux|sort -k4nr|head -5
```

![](http://image.ownit.top/csdn/20200314212600566.png)

占CPU的程序命令

```bash
ps aux | head -1;ps aux|sort -k3nr|head -5
```

![](http://image.ownit.top/csdn/20200314212429239.png)