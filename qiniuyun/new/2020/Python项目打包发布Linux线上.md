---
author: 南宫乘风
categories:
- Python学习
date: 2020-04-18 17:04:28
description: 近期写一个系统硬件监控，准备发布到上。下面一起看看怎么把项目发布到上吧。环境要求版本：运行项目运行项目因为的环境是的。所以我们首先把环境换成的才行。升级版本上面是教程。打包项目的依赖也就是本地安装的项。。。。。。。
image: http://image.ownit.top/4kdongman/84.jpg
tags:
- python
- pip
- linux
title: Python项目打包发布Linux线上
---

<!--more-->

> 近期写一个Python系统硬件监控，准备发布到Linux上。

下面一起看看怎么把项目发布到Linux上吧。

# 环境要求

**Python版本：3.7**

 

# Windows运行项目

![](http://image.ownit.top/csdn/20200418164919336.png)

![](http://image.ownit.top/csdn/20200418164935273.png)

 

# Centos7运行项目

因为centos7的python环境是2.75的。

所以我们首先把Python环境换成3.7的才行。

**[Centos7升级Python3.7.3版本](https://blog.csdn.net/heian_99/article/details/105428325)**

上面是教程。

### （1）打包Python项目的依赖（也就是本地安装的项目依赖）

```
pip3 freeze > requirements.txt
```

![](http://image.ownit.top/csdn/20200418165554759.png)

### （2）压缩Python项目和上传到服务器，解压

![](http://image.ownit.top/csdn/20200418165656154.png)

**zip包的解压命令：unzip 包名**

![](http://image.ownit.top/csdn/20200418165840505.png)

### （3）cd到项目里，安装依赖

```
 pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt
```

![](http://image.ownit.top/csdn/202004181701159.png)

 

### （4）运行项目启动文件

```
python3 manage.py 
```

![](http://image.ownit.top/csdn/20200418170247801.png)

![](http://image.ownit.top/csdn/20200418170257165.png)

**项目已经运行成功，还有最简便的方法就是运行在docker容器里，更加方便，后续会更新**