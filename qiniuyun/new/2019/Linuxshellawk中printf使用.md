---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-14 21:29:21
description: 是的重要格式化输出命令格式化输出内容格式：，，要点：，输出时要指定格式，用于指定后面的每个输出的格式，语句不会自动打印换行符格式：显示单个字符十进制整数科学计数法显示数值显示浮点数以科学计数法的格式或。。。。。。。
image: http://image.ownit.top/4kdongman/47.jpg
tags:
- linux
title: Linux shell awk中printf使用
---

<!--more-->

# **printf 是 awk 的重要格式化输出命令**

### **printf格式化输出内容**

### **格式：  
    printf format，item1，item2...  
      
要点：**

**1，printf输出时要指定格式format  
2，formay用于指定后面的每个item输出的格式  
3，printf语句不会自动打印换行符\\n**

## **format格式：**

**\%c:显示单个字符  
\%d,\%i:十进制整数  
\%e,\%E:科学计数法显示数值  
\%f:显示浮点数  
\%g,\%G:以科学计数法的格式或浮点数的格式显示数值  
\%s:显示字符串  
\%u:无符号整数  
\%\%:显示\%自身**

## **修饰符:  
N:显示宽度，N为数字  
\-:左对齐，默认为右对齐  
+:显示数值符号**

```
weizhang[root@wei awk]# awk '{printf "%s\n", $3}' print.txt 
wei
zhang
```

 

```
[root@wei awk]# awk '{printf "%6s\n", $3}' print.txt 
   wei
 zhang
```

## **显示前三个用户的用户名，uid，家目录**

```
[root@wei awk]# head -n 3 /etc/passwd | awk -F: '{printf "%-8s%-3d%-6s\n",$1,$3,$6}'
root    0  /root 
bin     1  /bin  
daemon  2  /sbin 
```