+++
author = "南宫乘风"
title = "Linux shell awk数组使用"
date = "2019-04-15 23:18:25"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/39.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89323328](https://blog.csdn.net/heian_99/article/details/89323328)

# **awk中使用数组**

**一.数组格式**

**数组是一个包含一系列元素的表.**

**格式如下：**

**    abc[1]=”xiaohong”**

**    abc[2]=”xiaolan”**

**解释：**

**abc      ：为数组名称**

**[1]、[2]：为数组元素下标，可以理解为数组的第1个元素、数组的第2个元素**

**”xiaohong”、”xiaolan”： 元素内容**

**数组<br> arrray[index-expression]**

**数组下从1开始，也可以使用字符串作为数组的下标**

**index-expression可以使用任意的字符串<br> 需注意的是：如果某数组元素事先不存在，那么引用其时，awk会自动创建次元素并初始化为0，要判断某数组中是否存在某元素，需要<br> 使用index in arrary的方式**

### **要遍历数组中每一个元素，需要使用 如下的特殊结构：**

**for（变量 in 数组名称）{print 数组名称[小标]}**

**其中，vae是数组的下标**

### **统计每个shell的使用次数**<br>  

```
[root@wei awk]# awk -F: '{shell[$7]++}END{for(i in shell){print i,shell[i]}}' /etc/passwd
/bin/sync 1
/bin/bash 17
/sbin/nologin 20
/sbin/halt 1
/sbin/shutdown 1 
```

### <br>** <br> 统计每个状态下的tcp连接个数<br>  **

```
[root@wei awk]# netstat -antp | awk '/^tcp/{state[$6]++}END{for(i in state){print i,state[i]}}'
LISTEN 9
ESTABLISHED 2
```

 
