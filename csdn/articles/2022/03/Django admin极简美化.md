+++
author = "南宫乘风"
title = "Django admin极简美化"
date = "2022-03-18 21:44:27"
tags=['django', 'python']
categories=['Python学习']
image = "post/4kdongman/97.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/123584909](https://blog.csdn.net/heian_99/article/details/123584909)

# 

1.Admin组件使用

　　Django内集成了web管理工具，Django在启动过程中会执行setting.py文件，初始化Django内置组件、注册APP、添加环境变量等

## **极简美化**

**效果图**

**登录页面**

![20a4ac473af44d8587b65f007c67bdcb.png](https://img-blog.csdnimg.cn/20a4ac473af44d8587b65f007c67bdcb.png)



**主页面**

![9b631272724348e4b0e3cf14626c7b2c.png](https://img-blog.csdnimg.cn/9b631272724348e4b0e3cf14626c7b2c.png)

使用django-simpleui模块；

直接pip安装即可：

```
pip install django-simpleui
```

然后在setting.py中注册即可：

```
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

![deac3cc0e43341999409c0ad79f7dc96.png](https://img-blog.csdnimg.cn/deac3cc0e43341999409c0ad79f7dc96.png)

 ![bde8460124fd47bd839c0841a1db421f.png](https://img-blog.csdnimg.cn/bde8460124fd47bd839c0841a1db421f.png)

 

![179ce877005d497da40af113370ceb60.png](https://img-blog.csdnimg.cn/179ce877005d497da40af113370ceb60.png)

 
