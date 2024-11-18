---
author: 南宫乘风
categories:
- Python学习
date: 2023-07-12 09:27:00
description: 简介学习如何使用的库来处理在程序运行过程中可能出现的各种异常和错误。是一种简单、易于使用的重试机制，帮助我们处理由网络问题或其他暂时性错误引起的失败。在很多情况下，简单的重试可能就是解决问题的最好方式。。。。。。。
image: ../../title_pic/32.jpg
slug: '202307120927'
tags:
- python
- 开发语言
title: Python错误处理的艺术：使用retrying库实现高效重试机制
---

<!--more-->

## 简介
学习如何使用 Python 的 retrying 库来处理在程序运行过程中可能出现的各种异常和错误。
retrying 是一种简单、易于使用的重试机制，帮助我们处理由网络问题或其他暂时性错误引起的失败。在很多情况下，简单的重试可能就是解决问题的最好方式。通过本篇博客，你将了解到如何在 Python 中使用 retrying。
## 安装retrying库

要安装 retrying 库，我们可以使用 pip 命令：
```python
pip install retrying
```
## retrying的功能
- 一般装饰器api
- 特定的停止条件（限制尝试次数）
- 特定的等待条件（每次尝试之间的指数增长的时间等待）
- 自定义的异常进行尝试
- 自定义的异常进行尝试返回结果
- 最简单的一个使用方法是无论有任何异常出现，都会一直重新调用一个函数、方法，直到返回一个值
## 基础使用
让我们从一个简单的例子开始。假设我们有一个经常会失败的函数，我们希望在这个函数失败时进行重试。以下是如何使用 retrying 库实现这个目标：
```python
from retrying import retry

@retry
def make_trouble():
    print("Trying...")
    raise Exception("Exception!")

try:
    make_trouble()
except Exception:
    print("Failed, even with retrying.")
```
在这个例子中，我们使用了 retry 修饰器（decorator）。如果 make_trouble 函数引发异常，retry 会捕获这个异常并重试函数。如果在尝试一定次数后仍然失败，那么异常将会被抛出。
![在这里插入图片描述](../../image/00783b82235048e69230f5dd7150ae89.png)
## 自定义重试
在默认情况下，retry 会在每次失败后立即重试，直到成功为止。然而，在很多情况下，我们可能希望自定义重试的行为。retrying 库提供了一些参数，让我们能够进行自定义：
- stop_max_attempt_number：最大重试次数。
- stop_max_delay：最大延迟毫秒数。
- wait_fixed：每次重试之间的固定等待时间（毫秒）。
- wait_random_min，wait_random_max：每次重试之间的随机等待时间（毫秒）。

```python
from retrying import retry

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def make_trouble():
    print("Trying...")
    raise Exception("Exception!")

try:
    make_trouble()
except Exception:
    print("Failed, even with retrying.")
```
在这个例子中，make_trouble 函数会最多尝试3次，每次尝试之间等待2秒。
![在这里插入图片描述](../../image/56112de62b184aa4b2f2080fe7135f16.png)
## 更复杂的重试条件
除了自定义重试次数和等待时间，我们还可以自定义重试的条件。例如，我们可能只希望在特定的异常出现时进行重试。这可以通过在 retry 修饰器中添加一个 retry_on_exception 函数来实现。
```python
from retrying import retry

def retry_if_io_error(exception):
    """Return True if we should retry (in this case when it's an IOError), False otherwise"""
    return isinstance(exception, IOError)

@retry(retry_on_exception=retry_if_io_error,stop_max_attempt_number=3, wait_fixed=2000)
def might_io_error():
    print("Trying...")
    raise IOError("IO Error!")

try:
    might_io_error()
except Exception:
    print("Failed, even with retrying.")
```
在上面的代码中，我们定义了一个函数 retry_if_io_error，只有当异常是 IOError 类型时，我们才进行重试。
![在这里插入图片描述](../../image/6446956377bb42b39a8e3b02e2c72ff2.png)
## 结束

使用 retrying 库，我们可以很容易地在 Python 中实现错误重试机制。这在处理网络请求、数据库操作或任何可能因暂时性问题失败的操作时都非常有用。希望你已经对如何使用 retrying 有了一个基本的了解，并能在你的 Python 项目中找到它的用武之地。

## 参考文档
[https://juejin.cn/post/7108202816665026573](https://juejin.cn/post/7108202816665026573)
