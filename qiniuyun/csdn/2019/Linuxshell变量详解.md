---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-14 20:16:52
description: 是一个用语言编写的程序，它是用户使用的桥梁。既是一种命令语言，又是一种程序设计语言。是指一种应用程序，这个应用程序提供了一个界面，用户通过这个界面访问操作系统内核的服务。的是第一种，是一个典型的图形界。。。。。。。
image: ../../title_pic/44.jpg
slug: '201903142016'
tags:
- linux
title: Linux shell变量详解
---

<!--more-->

Shell 是一个用 C 语言编写的程序，它是用户使用 Linux 的桥梁。Shell 既是一种命令语言，又是一种程序设计语言。

Shell 是指一种应用程序，这个应用程序提供了一个界面，用户通过这个界面访问操作系统内核的服务。

Ken Thompson 的 sh 是第一种 Unix Shell，Windows Explorer 是一个典型的图形界面 Shell。

## Shell 脚本

Shell 脚本（shell script），是一种为 shell 编写的脚本程序。

业界所说的 shell 通常都是指 shell 脚本，但读者朋友要知道，shell 和 shell script 是两个不同的概念。

 

**SHELL 变量**  
     
   变量（内存空间）  
   增加脚本的灵活性，适用性  
     
**类型：**  
     自定义变量  
     环境变量（Path）  
     特殊变量  
       
自定义变量

**变量名称规范：**

- 命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。
- 中间不能有空格，可以使用下划线（\_）。
- 不能使用标点符号。
- 不能使用bash里的关键字（可用help命令查看保留关键字）。

### 1  声明变量

\# 变量名称=变量值

```
[root@wei csdn]# name=wei
```

###   
2  调用变量的值

   \$变量名称  
   \$\{变量名称\}    变量名称或紧跟数字，字符的时候

输出时，由变量名，必须用双引号

```
[root@wei csdn]# name=cat
[root@wei csdn]# echo "this is $name"
this is cat
   
[root@wei csdn]# echo "this is ${name}"
this is cat
   
[root@wei csdn]# echo "this is ${name}s"
this is cats
```

### 3  SHELL变量的值默认全做为字符处理

```
[root@wei csdn]# a=10
[root@wei csdn]# b=20
[root@wei csdn]# c=a+b
[root@wei csdn]# echo $c
a+b

[root@wei csdn]# a=10
[root@wei csdn]# b=20
[root@wei csdn]# c=$a+$b
[root@wei csdn]# echo $c
10+20
```

### 数学运算：

方法1：\$\(\(\)\)

```
[root@wei csdn]# a=10
[root@wei csdn]# b=20
[root@wei csdn]# c=$((a+b))
[root@wei csdn]# echo $c
30
```

方法2：关键字：let

```
[root@wei csdn]# a=10
[root@wei csdn]# b=20
[root@wei csdn]# let c=a+b
[root@wei csdn]# echo $c
30
```

方法3：关键字：declare

```
[root@wei csdn]# a=10
[root@wei csdn]# b=20
[root@wei csdn]# declare -i c=a+b
[root@wei csdn]# echo $c
30
```

数学运算符：  
         +  
         \-  
         \*  
         /     整除  
         \%     取余

## 生成随机数

```
[root@wei csdn]# echo $RANDOM 
11400
[root@wei csdn]# echo $RANDOM 
9702
[root@wei csdn]# echo $RANDOM 
21328
```

生成10以内的随机数：

```
[root@wei csdn]# echo $((RANDOM%10))
4
[root@wei csdn]# echo $((RANDOM%10))
2
```

###   
4 命令引用

  
   反引号 \`COMMAND\`  
   \$\(COMMAND\)

```
[root@wei csdn]# a=`ls -ldh /etc/`
[root@wei csdn]# echo $a
drwxr-xr-x. 77 root root 8.0K 3月 14 16:23 /etc/

[root@wei csdn]# b=$(ls -ldh /etc/)
[root@wei csdn]# echo $b
drwxr-xr-x. 77 root root 8.0K 3月 14 16:23 /etc/
```

## 提取ip

```
[root@wei csdn]# ifconfig ens33 |grep "netmask" | awk '{print $2}'
192.168.196.131
```

```
[root@wei csdn]# head -n 3 /etc/passwd |awk -F: '{print $1,$6,$7}'
root /root /bin/bash
bin /bin /sbin/nologin
daemon /sbin /sbin/nologin
```

###   
5  删除变量

\# unset 变量名称

### 环境变量

**（1）查看环境变量**

```
[root@wei csdn]# env | less
```

**（2）定义环境变量：修改环境变量的值**

#export 变量名称=变量值

```
[root@wei csdn]# vim /etc/profile
[root@wei csdn]# source /etc/profile

```

  
\$\?判断上个命令的执行状态（0--255）

0：代表成功  
其余:代表失败

![](../../image/20190314201632223.png)