---
author: 南宫乘风
categories:
- Python学习
date: 2019-09-05 13:51:17
description: 文件操作打开文件地址，操作形式常用四种操作模式：写入：读取：二进制追加文件读取读取一行类容关闭文件文件写入一起去学习。。。。。。。
image: ../../title_pic/24.jpg
slug: '201909051351'
tags:
- 技术记录
title: Python的文件操作
---

<!--more-->

## #文件操作   \#打开   \#open\("文件地址"，"操作形式’\)

## 常用四种操作模式  
'''  
w：写入  
r：读取  
b：二进制  
a+:追加  
'''

```python
fh=open("E:/Code/Python/python.txt","r")
date=fh.read()
```

## #文件读取

```python
date=fh.read()
```

##    \#读取一行类容

```python
line=fh.readline()
```

## #关闭文件

```python
fh.close()
```

## #文件写入  
 

```python
date="一起去学习"
fh2=open("E:/Code/Python/python2.txt","w")
fh2.write(date)
fh2.close()
```