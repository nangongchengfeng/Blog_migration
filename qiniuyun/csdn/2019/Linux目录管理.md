---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-05 14:53:31
description: 文件目录管理：目录管理切换目录目录名称退到上一目录：创建目录文件名称文件名称递归创建目录利用来查看结果：文件管理查看文件目录名称：参数以详细信息显示出来月解释：前面这些等符合的意思文件目录软链接文件类。。。。。。。
image: ../../title_pic/30.jpg
slug: '201901051453'
tags:
- linu
title: Linux目录管理
---

<!--more-->

**Linux文件目录管理**

**1：目录管理**

**1）切换目录**

**\# cd  \[ 目录名称\]**

**2）退到上一目录**

**\# cd ..**

**2：创建目录**

**mkdir  \[文件名称\]**

**mkdir \-p  \[文件名称\] 递归创建目录**

```
mkdir -p /root/linux/zhang/wei
```

**利用tree来查看结果**

```
tree /root/linux
```

**![](../../image/20190105144105344.png)**

**3：文件管理**

**1）查看文件**

**ls  \<option>  \[目录名称\]**

**【option】：参数**

**\-l 以详细信息显示出来**

**\-rw-r--r--.  1 root root       16 12月  4 21:42 adjtime**

**![](../../image/20190105144623577.png)**

**解释：前面这些- r d l等符合的意思**

**\-  文件**

**d  目录**

**l   软链接文件（link）类似快捷方式**

**b   块设备文件（block），硬盘，硬盘分区，u盘，光盘**

**c   字符设备文件（chaeacter）键盘，鼠标，显示器**

**ls  \<option>  \[目录名称\]**

**参数：**

**\-l    更加可视化的显示文件信息**

**\-d   显示目录自身的信息**

**\-a    显示目录的隐藏文件（以.开头的文件）**

**\-t     按文件修改时间降序排列**

**\-S     按文件大小降序排列**

**各个参数可以组合**

**du \-sh  \[目录名称\] 用来统计文件和目录占的大小**

**![](../../image/2019010514493984.png)**

**du \-ah  \[目录名称\] 用来分享每个文件和目录占的大小**

**![](../../image/20190105145107632.png)**

 

 

![](../../image/20190105150620896.png)