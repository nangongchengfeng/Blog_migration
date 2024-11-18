---
author: 南宫乘风
categories:
- Python学习
date: 2021-07-08 18:20:52
description: 实现查询剪贴板自动匹配信息前提：业务太多，每个有不同的主机名和不同的功能。不想每次都要去查，想更方便点，更快一点。通俗点思路：点击，自动监控剪贴板的内容，然后正则取出，接着根据对比业务文档，获取相应的。。。。。。。
image: ../../title_pic/06.jpg
slug: '202107081820'
tags:
- python
- linux
title: Python实现查询剪贴板自动匹配信息
---

<!--more-->

## Python实现查询剪贴板自动匹配信息

前提：业务IP太多，每个有不同的主机名和不同的功能。

            不想每次都要去查execl，想更方便点，更快一点。

![](../../image/20210708181301587.png)

通俗点思路：点击exe，Python 自动监控剪贴板的内容，然后正则取出IP，接着根据IP对比业务文档，获取相应的信息，然后把查询出来的内容，弹出提示，把查询出的内容写入剪贴板。

```python
'''
功能作用：对比剪贴板类容
'''

import win32clipboard as w
import win32con
import xlrd
from tkinter import messagebox
import win32api, win32con
import pyperclip
import re
import sys
import os

# print(__file__)

path = os.path.dirname(os.path.abspath(__file__))
sys.intern(path)


# print(path)
# 获取剪贴板中的内容
def getText():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return (d).decode('GBK')


# 设置剪贴板的类容
def set_text(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()


# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 获取剪贴板中的ip,并判断是否正常
def get_ip(ss_ip):
    ipList = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ss_ip)
    # print(ipList)
    if ipList:
        return ipList
    else:
        win32api.MessageBox(0, "请您检查复制是否带有IP，请重新测试", "提醒", win32con.MB_OK)
        sys.exit(0)


# 获取xls中的数据，和之前剪贴板的数据对比
def host(ss_ip):
    # 获取execl的内容，这边是根据业务来分析
    filename = resource_path(os.path.join("res", "hosts.xls"))
    # print(filename)
    # execl_hosts = './hosts.xls'
    data1 = xlrd.open_workbook(filename)
    page = data1.sheet_by_index(2)
    nrows1 = page.nrows
    ncols1 = page.ncols
    # 获取ip
    host_ip = page.col_values(10)
    app = page.col_values(1)  # 功能集群
    purpose = page.col_values(2)  # 用途
    hostname = page.col_values(11)  # 主机名称
    # print(host_ip)

    # 开始对比数据
    start = 0
    count = 1
    # print(ss_ip)
    if str(ss_ip[0]) not in host_ip:
        win32api.MessageBox(0, f"暂无设备{ss_ip[0]}的信息", "未知设备", win32con.MB_OK)
        sys.exit(0)
    for k, item in enumerate(host_ip, start):
        # print(k,item,ss_ip[0])
        if str(ss_ip[0]) == str(item):
            # print("正常:" + item, k)
            win32api.MessageBox(0, f"\t\t注意\n 主机ip：{item}  主机名称：{hostname[k]} \n 功能集群：{app[k]}  主机用途：{purpose[k]}",
                                "发现设备", win32con.MB_OK)
            pyperclip.copy(f"主机ip：{item}  主机名称：{hostname[k]} \n 功能集群：{app[k]}  主机用途：{purpose[k]}")
            sys.exit(0)

        count = count + 1


def main():
    ss_ip = getText()
    one_ip = get_ip(ss_ip)
    host(one_ip)


if __name__ == '__main__':
    main()
```

测试效果：

![](../../image/20210708181412458.png)

![](../../image/20210708181431902.png)

## 打包资源生成exe

Python打包.exe的方法大致有四种：py2exe, pyinstaller,cx\_Freeze和nuitka。其中最常用的是pyinstaller。Pyinstaller本身不是python库，但依旧可以安装python库安装方式安装，生成的.exe可以跨多平台使用，也能指定图标。  
 

我们需要把使用到的资源文件都放在一个文件夹里。本文在当前目录下新建了一个名为res的子文件夹来存放资源文件，本文假设res内的资源文件为hosts.xls

修改完.py文件后可以先运行一下，保证无误。然后通过cmd指令：

```python
pyi-makespec -F beloved.py
```

  
生成.spec文件。如果要添加Icon等可以在这里就使用pyi-makespec \--icon abc.jpg \-F beloved.py语句生成spec文件。  
接下来，修改.spec文件：  
![](../../image/2020032516311779.jpg)

修改前datas=\[\]，本文这里把它改成上图所示，意思是

> 将beloved.py当前目录下的res目录（及其目录中的文件）加入目标exe中，在运行时放在零时文件的根目录下，名称为res。

## 生成.exe文件以及其他相关文件

接下来，我们便可以放心的生成.exe文件了。执行cmd指令

```bash
pyinstaller -F beloved.spec
```

.exe文件生成在子文件dict中。到此便可以把.exe发给其他电脑端运行了。.exe运行比较慢，建议多等待，只要没出现错误提示就OK。

参考地址：<https://blog.csdn.net/qq_44685030/article/details/105096338>