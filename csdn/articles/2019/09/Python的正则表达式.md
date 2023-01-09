+++
author = "南宫乘风"
title = "Python的正则表达式"
date = "2019-09-07 16:45:11"
tags=[]
categories=['Python学习']
image = "post/4kdongman/66.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100601244](https://blog.csdn.net/heian_99/article/details/100601244)

**目录**

 

[# 正则表达式](#%23%20%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F)

[#普通字符作为原子](#%23%E6%99%AE%E9%80%9A%E5%AD%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%E5%8E%9F%E5%AD%90)

[#非打印字符作为原子](#%23%E9%9D%9E%E6%89%93%E5%8D%B0%E5%AD%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%E5%8E%9F%E5%AD%90)

[# 通用字符作为原子（作用非常大）](#%23%20%E9%80%9A%E7%94%A8%E5%AD%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%E5%8E%9F%E5%AD%90%EF%BC%88%E4%BD%9C%E7%94%A8%E9%9D%9E%E5%B8%B8%E5%A4%A7%EF%BC%89)

[# 原子表(几个原子组成一个)](#%23%20%E5%8E%9F%E5%AD%90%E8%A1%A8%28%E5%87%A0%E4%B8%AA%E5%8E%9F%E5%AD%90%E7%BB%84%E6%88%90%E4%B8%80%E4%B8%AA%29)

[# 元字符](#%23%20%E5%85%83%E5%AD%97%E7%AC%A6)

[# 模式修正符](#%23%20%E6%A8%A1%E5%BC%8F%E4%BF%AE%E6%AD%A3%E7%AC%A6)

[# 贪婪模式和懒惰模式](#%23%20%E8%B4%AA%E5%A9%AA%E6%A8%A1%E5%BC%8F%E5%92%8C%E6%87%92%E6%83%B0%E6%A8%A1%E5%BC%8F)

[# 正则表达式函数](#%23%20%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E5%87%BD%E6%95%B0)

[#示例：匹配.com和.cn网址​​​​​](#%23%E7%A4%BA%E4%BE%8B%EF%BC%9A%E5%8C%B9%E9%85%8D.com%E5%92%8C.cn%E7%BD%91%E5%9D%80%E2%80%8B%E2%80%8B%E2%80%8B%E2%80%8B%E2%80%8B)

[#示例：匹配电话号码](#%23%E7%A4%BA%E4%BE%8B%EF%BC%9A%E5%8C%B9%E9%85%8D%E7%94%B5%E8%AF%9D%E5%8F%B7%E7%A0%81)

# # 正则表达式

 

```
import re
str ="weidongliang"
```

## <br> #普通字符作为原子

```
pat ="wei"
rsr=re.search(pat,str)
print(rsr)
```

## <br> #非打印字符作为原子

<br> #\n:换行符   \t：制表符

```
str ='''baidusdfs
baidu
'''
pat="\n"
rest=re.search(pat,str)
print(rest)
```

## <br> # 通用字符作为原子（作用非常大）<br>  
1. \w:匹配任何字母，数字，下划线1. \W:除匹配任何字母，数字，下划线1. \d:十进制数字1. \D:除十进制数字1. \s:空白字符1. \S:除空白字符
 

```
string="taobao4 59454baidu"
pat="\w\d\s\d\d"
print(re.search(pat,string))
```

## # 原子表(几个原子组成一个)

```
string="taobao4 59454baidu"
pat="tao[zub]ao"
pat="tao[^zuq]ao"
print(re.search(pat,string))
```

## # 元字符<br>  
1. . :出换行外任意一个字符1. ^ ：开始位置1. $ :结束位置1. * ：0\1\多次1. ？：0\1次1. + ：1\多次1. {n} ：恰好n次1. {n,} ：至少n次1. {n，m}：至少n，最多m1. |  ：模式选择符1. () :模式单元
```
wei="taoyun14524baidu"
pat="tao.un"
pat="bai..$"
ce=re.search(pat,wei)
print(ce)
```

## # 模式修正符<br>  
1. I 匹配时忽悠大小写 *1. M 多行匹配 *1. L 本地化识别匹配1. U Unicode1. S 让.匹配包括换行符 *
```
str="Python"
pat="pyt"
ce=re.search(pat,str,re.I)
print(ce)
```

## # 贪婪模式和懒惰模式

<br> # 默认是贪婪模式

```
str="pythony"
pat="p.*y" #贪婪模式，模糊
pat2="p.*?y" #懒惰模式，精准
ce=re.search(pat,str,re.I)
ce2=re.search(pat2,str,re.I)
print(ce)
print(ce2)
```

## # 正则表达式函数

<br> #1，match 重头开始匹配

```
str="poyajgsdabskjdbaiush"
pat="p.*?y"
ce=re.match(pat,str,re.I)
print(ce)
```

#2，search  任何地方都可以匹配

#3，全局匹配函数

```
str="efdrpoyajgspnyskjdbapyth"
pat="p.*?y"

```

<br> # 全局匹配格式re.compile(正则表达式).findall(数据)

```
ce=re.compile(pat).findall(str)
print(ce)
```

 

## #示例：匹配.com和.cn网址<br> ​​​​​

```
string="&lt;a href='http://www.baidu.com'&gt;百度&lt;/a&gt;"
pat="[a-zA-Z]+://[^\s]*[.com|.cn]"
ce=re.search(pat,string)
print(ce)
```

## #示例：匹配电话号码

```
string="adsgdiasdiauhdaj012-754745745dasd0773-46853415adasda"
pat="\d{4}-\d{7}|\d{3}-\d{8}"
ce=re.compile(pat).findall(string)
print(ce)

```

 
