---
author: 南宫乘风
categories:
- Java
date: 2019-11-19 16:36:56
description: 好吧，这个问题比较，但是记录一下，以免后期遗忘。说白了，这个问题就是端口被占用了。问题：看翻译：端口被占用解决办法：解决端口被占用的问题、、等等查看占用程序的通过，停止程序看截图：。。。。。。。
image: http://image.ownit.top/4kdongman/54.jpg
tags:
- 错误问题解决
title: qos-server can not bind localhost22222, dubbo version 2.6.0, current host 127.0.0.1【问题解决】
---

<!--more-->

好吧，这个问题比较low，但是记录一下，以免后期遗忘。

说白了，这个问题就是端口被占用了。

问题：

```
qos-server can not bind localhost:22222, dubbo version: 2.6.0, current host: 127.0.0.1
java.net.BindException: Address already in use: bind
```

看翻译：【22222端口被占用】

![](http://image.ownit.top/csdn/20191119163341972.png)

解决办法：

[解决端口被占用的问题（80、222222、3306）等等](https://blog.csdn.net/heian_99/article/details/103089408)

查看占用程序的pid

```
netstat -ano | findstr 22222
```

通过pid，停止程序

```
taskkill /f /pid 20720
```

看截图：

![](http://image.ownit.top/csdn/2019111916364082.png)