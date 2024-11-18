---
author: 南宫乘风
categories:
- Python学习
date: 2022-03-18 21:44:27
description: 组件使用内集成了管理工具，在启动过程中会执行文件，初始化内置组件、注册、添加环境变量等极简美化效果图登录页面主页面使用模块；直接安装即可：然后在中注册即可：主要是这个美化页面的注册应用注册应用然后就完。。。。。。。
image: ../../title_pic/56.jpg
slug: '202203182144'
tags:
- django
- python
title: Django admin极简美化
---

<!--more-->

1.Admin组件使用

　　Django内集成了web管理工具，Django在启动过程中会执行setting.py文件，初始化Django内置组件、注册APP、添加环境变量等

## **极简美化**

**效果图**

**登录页面**

![](../../image/20a4ac473af44d8587b65f007c67bdcb.png)

**主页面**

![](../../image/9b631272724348e4b0e3cf14626c7b2c.png)

使用django-simpleui模块；

直接pip安装即可：

```python
pip install django-simpleui
```

然后在setting.py中注册即可：

```python
INSTALLED_APPS = [
    'simpleui', #主要是这个美化页面的
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # 注册app应用
    'DjangoUeditor',  # 注册APP应用
]
```

然后就完事了，打开admin即可，如下：

![](../../image/deac3cc0e43341999409c0ad79f7dc96.png)

 ![](../../image/bde8460124fd47bd839c0841a1db421f.png)

 

![](../../image/179ce877005d497da40af113370ceb60.png)