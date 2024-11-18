---
author: 南宫乘风
categories:
- Python学习
- 项目实战
date: 2023-07-04 11:04:27
description: 引言在开发应用程序时，我们经常需要对某些功能或进行速率限制，以防止滥用和保护服务器资源。的库提供了一种简单且强大的方法来实现速率限制。本文将介绍如何使用库在应用程序中实现速率限制功能。什么是速率限制？。。。。。。。
image: ../../title_pic/66.jpg
slug: '202307041104'
tags:
- python
- 开发语言
title: 限制速度，释放潜力：Python中的ratelimit库解密
---

<!--more-->

## 引言
在开发Web应用程序时，我们经常需要对某些功能或API进行速率限制，以防止滥用和保护服务器资源。Python的ratelimit库提供了一种简单且强大的方法来实现速率限制。本文将介绍如何使用ratelimit库在Python应用程序中实现速率限制功能。
 ## 什么是速率限制？
 
 速率限制是一种限制某个操作或功能的调用频率的方法。它可以防止恶意用户或程序对系统造成过大的负载或滥用系统资源。速率限制通常通过设置每秒或每分钟允许的最大请求数来实现。
 
 ## ratelimit库简介
 ratelimit是一个Python库，它提供了速率限制的功能。它基于令牌桶算法，允许您以简洁而灵活的方式对函数或方法进行速率限制。
 
 ratelimit 提供的装饰器，可以控制被装饰的函数在某个周期内被调用的次数不超过一个阈值，尽管作者本意是限制那些访问web API 的函数的调用次数，但你可以推而广之，所有不能频繁调用的函数都可以用这个装饰器来修饰。

项目的github地址: [https://github.com/tomasbasham/ratelimit](https://github.com/tomasbasham/ratelimit)

## ratelimit库

> 实例
> @sleep_and_retry
@limits(calls=2, period=10)

@sleep_and_retry 是一个 Python 装饰器，用于在函数调用达到限制后自动进行重试，并在重试之前进行休眠。它通常与限流库（如 ratelimit）一起使用，以确保函数在限制条件下被正确执行。

@limits(calls=2, period=10) 是 ratelimit 库中的另一个装饰器，用于设置函数的限制条件。在这个例子中，它指定了函数在 10 秒内最多可以被调用 2 次。

当函数被装饰时，@sleep_and_retry 会在函数调用超过限制时自动进行休眠并重试。具体的行为如下：

当函数第一次被调用时，它会立即执行。
如果函数在 10 秒内已经被调用了 2 次，它将抛出一个异常，指示超过了限制。
如果函数调用达到了限制，@sleep_and_retry 会在下一次调用之前休眠一段时间，以确保函数在下一个计算周期开始之前被重试。
休眠时间的计算基于上一次函数调用的时间和当前时间之间的差值。

<br>
<br>

要开始使用ratelimit库，首先需要安装它。可以使用pip命令进行安装：
```python
pip install ratelimit
```
使用ratelimit库进行速率限制：


下面是一个示例，演示如何在Python函数上应用速率限制：
```python
from ratelimit import limits, sleep_and_retry

# 设置速率限制为每秒最多两次调用
@sleep_and_retry
@limits(calls=2, period=1)
def my_function():
    # 在此处添加您的功能代码
    pass
```
在上面的示例中，@limits(calls=2, period=1)装饰器定义了一个速率限制规则，允许每秒最多调用两次my_function函数。@sleep_and_retry装饰器可确保当超出速率限制时，函数将休眠并重试。

根据您的需求，您可以根据实际情况调整calls和period参数的值。

## 日常使用
### 函数限制
```python
from ratelimit import limits, sleep_and_retry
import time

# 设置每分钟最多调用次数为 3
@limits(calls=3, period=60)
@sleep_and_retry
def my_function():
    # 在这里编写你的函数逻辑
    print("函数被调用")

# 测试函数的调用
for _ in range(10):
    try:
        my_function()
    except Exception as e:
        print("调用次数超过限制，等待1分钟后继续")
        time.sleep(60)
        my_function()
```
![在这里插入图片描述](../../image/43b800f62e514f46b7a44e773b4f3f73.png)

```python
from ratelimit import limits, sleep_and_retry


@sleep_and_retry
@limits(calls=1, period=10)
def call_api():
    print('call api')


while True:
    call_api()

```

### 高并发线程池
```python
from ratelimit import limits, sleep_and_retry
from concurrent.futures import ThreadPoolExecutor


# 设置每分钟最多调用次数为 3
@sleep_and_retry
@limits(calls=3, period=10)
def my_function():
    # 在这里编写你的函数逻辑
    print("函数被调用")


# 创建 ThreadPoolExecutor 对象
executor = ThreadPoolExecutor(max_workers=5)

# 测试函数的调用
for _ in range(100):
    executor.submit(my_function)

```

参考文档：
[python开源项目解读—ratelimit，限制函数单位时间内被调用次数](https://zhuanlan.zhihu.com/p/483013717)
[Python Django 配置使用django-ratelimit限制网站接口访问频率](https://www.cjavapy.com/article/2606/)
