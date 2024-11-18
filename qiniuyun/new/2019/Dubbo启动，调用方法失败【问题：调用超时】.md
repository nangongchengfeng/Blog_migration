---
author: 南宫乘风
categories:
- Java
date: 2019-11-19 16:18:24
description: 今天，启动，开始写项目。在一个调用里面的一个方法时，程序一直调用，每次显示报红。很难搞。问题代码这么烦，已经搞崩心态了扔百度翻译去。，真智障靠，方法调用超时。解决办法：设置超时时间设置是否检查服务存在。。。。。。。
image: http://image.ownit.top/4kdongman/93.jpg
tags:
- 错误问题解决
title: Dubbo启动，调用方法失败【问题：调用超时】
---

<!--more-->

今天，启动dubbo，开始写项目。

在一个调用dubbo里面的一个方法时，程序一直调用，每次显示报红。

很难搞。

问题代码

```html
com.alibaba.dubbo.rpc.RpcException:
 Failed to invoke the method getAllSku in the service com.atguigu.gmall.service.
SkuService. Tried 3 times of the providers 
[192.168.116.1:53684] (1/1) from the registry 47.98.231.26:2181
 on the consumer 192.168.116.1 using the dubbo version 2.6.0. Last error is:
 Invoke remote method timeout. method: getAllSku,
 provider: dubbo://192.168.116.1:53684/com.atguigu.gmall.service
```

这么烦，已经搞崩心态了

扔百度翻译去。

【bug，真TM智障】

靠，方法调用超时。

![](http://image.ownit.top/csdn/20191119161554665.png)

 

 

解决办法：

```
# 设置超时时间
spring.dubbo.consumer.timeout=600000
# 设置是否检查服务存在
spring.dubbo.consumer.check=false
```

可以了，终于找出bug了。真是不容易

 

![](http://image.ownit.top/csdn/20191119161735417.png)