+++
author = "南宫乘风"
title = "Linux shell awk中printf使用"
date = "2019-04-14 21:29:21"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/22.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89302303](https://blog.csdn.net/heian_99/article/details/89302303)

# **printf 是 awk 的重要格式化输出命令**

### **printf格式化输出内容**

### **格式：<br>     printf format，item1，item2...<br>     <br>要点：**

**1，printf输出时要指定格式format<br> 2，formay用于指定后面的每个item输出的格式<br> 3，printf语句不会自动打印换行符\n**

## **format格式：**

**%c:显示单个字符<br> %d,%i:十进制整数<br> %e,%E:科学计数法显示数值<br> %f:显示浮点数<br> %g,%G:以科学计数法的格式或浮点数的格式显示数值<br> %s:显示字符串<br> %u:无符号整数<br> %%:显示%自身**

## **修饰符:<br> N:显示宽度，N为数字<br> -:左对齐，默认为右对齐<br> +:显示数值符号**

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

 
