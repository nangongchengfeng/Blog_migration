---
author: 南宫乘风
categories:
- Python学习
date: 2019-09-07 16:45:11
description: 目录正则表达式正则表达式普通字符作为原子非打印字符作为原子通用字符作为原子作用非常大通用字符作为原子作用非常大原子表几个原子组成一个原子表几个原子组成一个元字符元字符模式修正符模式修正符贪婪模式和懒惰。。。。。。。
image: http://image.ownit.top/4kdongman/27.jpg
tags:
- 技术记录
title: Python的正则表达式
---

<!--more-->

**目录**

 

[\# 正则表达式](<## 正则表达式>)

[#普通字符作为原子](#%23%E6%99%AE%E9%80%9A%E5%AD%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%E5%8E%9F%E5%AD%90)

[#非打印字符作为原子](#%23%E9%9D%9E%E6%89%93%E5%8D%B0%E5%AD%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%E5%8E%9F%E5%AD%90)

[\# 通用字符作为原子（作用非常大）](<## 通用字符作为原子（作用非常大）>)

[\# 原子表\(几个原子组成一个\)](<## 原子表(几个原子组成一个)>)

[\# 元字符](<## 元字符>)

[\# 模式修正符](<## 模式修正符>)

[\# 贪婪模式和懒惰模式](<## 贪婪模式和懒惰模式>)

[\# 正则表达式函数](<## 正则表达式函数>)

[#示例：匹配.com和.cn网址​​​​​](#%23%E7%A4%BA%E4%BE%8B%EF%BC%9A%E5%8C%B9%E9%85%8D.com%E5%92%8C.cn%E7%BD%91%E5%9D%80%E2%80%8B%E2%80%8B%E2%80%8B%E2%80%8B%E2%80%8B)

[#示例：匹配电话号码](#%23%E7%A4%BA%E4%BE%8B%EF%BC%9A%E5%8C%B9%E9%85%8D%E7%94%B5%E8%AF%9D%E5%8F%B7%E7%A0%81)

---

# \# 正则表达式

 

```
import re
str ="weidongliang"
```

##    \#普通字符作为原子

```python
pat ="wei"
rsr=re.search(pat,str)
print(rsr)
```

##    \#非打印字符作为原子

  
#\\n:换行符   \\t：制表符

```python
str ='''baidusdfs
baidu
'''
pat="\n"
rest=re.search(pat,str)
print(rest)
```

##   
\# 通用字符作为原子（作用非常大）  
 

1.  \\w:匹配任何字母，数字，下划线
2.  \\W:除匹配任何字母，数字，下划线
3.  \\d:十进制数字
4.  \\D:除十进制数字
5.  \\s:空白字符
6.  \\S:除空白字符

 

```python
string="taobao4 59454baidu"
pat="\w\d\s\d\d"
print(re.search(pat,string))
```

## \# 原子表\(几个原子组成一个\)

```python
string="taobao4 59454baidu"
pat="tao[zub]ao"
pat="tao[^zuq]ao"
print(re.search(pat,string))
```

## \# 元字符  
 

 1.     . :出换行外任意一个字符
 2.     \^ ：开始位置
 3.     \$ :结束位置
 4.     \* ：0\\1\\多次
 5.     ？：0\\1次
 6.     \+ ：1\\多次
 7.     \{n\} ：恰好n次
 8.     \{n,\} ：至少n次
 9.     \{n，m\}：至少n，最多m
 10.     |  ：模式选择符
 11.     \(\) :模式单元

```python
wei="taoyun14524baidu"
pat="tao.un"
pat="bai..$"
ce=re.search(pat,wei)
print(ce)
```

## \# 模式修正符  
 

 1.     I 匹配时忽悠大小写 \*
 2.     M 多行匹配 \*
 3.     L 本地化识别匹配
 4.     U Unicode
 5.     S 让.匹配包括换行符 \*

```python
str="Python"
pat="pyt"
ce=re.search(pat,str,re.I)
print(ce)
```

## \# 贪婪模式和懒惰模式

  
\# 默认是贪婪模式

```python
str="pythony"
pat="p.*y" #贪婪模式，模糊
pat2="p.*?y" #懒惰模式，精准
ce=re.search(pat,str,re.I)
ce2=re.search(pat2,str,re.I)
print(ce)
print(ce2)
```

## \# 正则表达式函数

  
#1，match 重头开始匹配

```python
str="poyajgsdabskjdbaiush"
pat="p.*?y"
ce=re.match(pat,str,re.I)
print(ce)
```

#2，search  任何地方都可以匹配

#3，全局匹配函数

```python
str="efdrpoyajgspnyskjdbapyth"
pat="p.*?y"
```

  
\# 全局匹配格式re.compile\(正则表达式\).findall\(数据\)

```python
ce=re.compile(pat).findall(str)
print(ce)
```

 

## #示例：匹配.com和.cn网址  
​​​​​

```python
string="<a href='http://www.baidu.com'>百度</a>"
pat="[a-zA-Z]+://[^\s]*[.com|.cn]"
ce=re.search(pat,string)
print(ce)
```

## #示例：匹配电话号码

```python
string="adsgdiasdiauhdaj012-754745745dasd0773-46853415adasda"
pat="\d{4}-\d{7}|\d{3}-\d{8}"
ce=re.compile(pat).findall(string)
print(ce)
```