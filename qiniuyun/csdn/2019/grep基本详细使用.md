---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-23 21:29:45
description: 过滤文件类容正则表达式应用：文件名称模式由普通字符和正则表达式的元字符组构成的条件简单例子正则表达式的元字符匹配单个字符的元字符任意单个字符前面是一个小点注意：代表任意字符，此处有两个，代表两个任意字。。。。。。。
image: ../../title_pic/35.jpg
slug: '201901232129'
tags:
- linux
title: grep基本详细使用
---

<!--more-->

 

# **过滤文件类容---grep**

## grep正则表达式应用：

### **#grep 【option】”pattern” 文件名称**

### pattern模式

###       由普通字符和正则表达式的元字符组构成的条件

 

**简单例子**

```
grep "root" /etc/passwd
```

![](../../image/20190123204009457.png)

## 正则表达式的元字符

### （1）匹配单个字符的元字符

**. 任意单个字符（前面是一个小点）**

```
grep "r..t" /etc/passwd
```

** 注意：.   代表任意字符，此处有两个  .  ，代表两个任意字符，看下面的例子**

![](../../image/20190123204437689.png)

**  \[ \]   代表或者的关系**

** 连续的字符范围**

**\[a-z\]  : a到z的所有小写字母**

**\[A-Z\]   ： A到Z所有的大写字母**

**\[a-zA-Z\] ：包含所有的大小写字母 **

**\[0-9\]  ：0到9的所有数字**

**\[a-zA-Z0-9 \]  ：包含所有大小字母和数字**

## 为了方便后面的练习，在此建立个临时文件，写入字符，当做练习的文件 

```
vim 1.txt
rot
rAt
rBt
r1t
root
rVCt
r4t
```

```
grep "r[a-z]t" 1.txt

grep "r[A-Z]t" 1.txt
```

![](../../image/20190123210234548.png)

**\^ 取反**

**\[\^a-z\]**

```
grep "r[^0-9]t" 1.txt 
```

![](../../image/20190123210505532.png)

### \(2\)匹配字符出现的位置

**\^string  以string开头**

```
 grep "^root" /etc/passwd
```

![](../../image/2019012321070646.png)

**对首行\[rbh\]开头**

```
grep "^[rbh]" /etc/passwd
```

![](../../image/20190123210831400.png)

**不是【rbh】开头**

```
grep "^[^rbh]" /etc/passwd
```

![](../../image/20190123210928496.png)

**string\$  以string\$结尾**

**以bash结尾的**

```
 grep "bash$" /etc/passwd
```

![](../../image/20190123211047362.png)

**查看nologin的行数**

```
grep "nologin$" /etc/passwd | wc -l
```

![](../../image/20190123211230787.png)

 

**\^\$ ： 代表 空行**

 

**查看目录名称（此处是指目录文件）**

```
ls -l /etc/ | grep "^d"
```

![](../../image/20190123211622848.png)

## 为了方便后面的练习，在此建立个临时文件，写入字符，当做练习的文件 

```
vim 2.txt
a
ab
abb
abbbb
abbbbb
abbbbbbb
```

## **\*  匹配其前一个字符出现任意次**

## **  .\*任意字符**

```
 grep "ab*" 3.txt
```

![](../../image/20190123211950512.png)

### \\\?   0次或者1次   可有可无

```
grep "ab\?" 2.txt
```

![](../../image/20190123212046669.png)

### \\+  1次或者多次   最少1次

```
grep "ab\+" 2.txt
```

### ![](../../image/20190123212225265.png)

### \\\{2\\\}    出现两次

```
grep "ab\{2\}" 2.txt
```

### ![](../../image/20190123212324847.png)

### \\\{2，5\\\}    最少2次，最多5次

```
grep "ab\{2,5\}" 2.txt
```

![](../../image/20190123212425325.png)

# option选项

## 1）-i 忽略大小写

 

```
[root@zhang ~]# grep -i "^r" 1.txt
```

 

## 2）-o 仅显示符合正则表达式的内容，不显示整行

```
[root@zhang ~]# grep -o  "r..t" /etc/passwd

root
```

## 3）-v 反向过滤

```
[root@zhang ~]# grep -v "^#" /etc/fstab



/dev/mapper/centos-root /                       xfs     defaults        0 0

UUID=20b4a09c-ba00-41d4-a6d5-7dc24bc0a057 /boot                   xfs     defaults        0 0

/dev/mapper/centos-swap swap                    swap    defaults        0 0
```

 

## 4）-e 根据多条件过滤文件

```
[root@zhang ~]# grep -e "^$" -e "^#" /etc/fstab



#

# /etc/fstab

# Created by anaconda on Mon Jan  7 01:19:06 2019
```

## 4）-E 支持扩展正则表达式

```
grep -E "vmx|svm" /proc/cpuinfo

```

## 5）-A n 显示符合条件的后2行

```
[root@zhang ~]# ifconfig |grep -A 2 "netmask"

        inet 192.168.196.131  netmask 255.255.255.0  broadcast 192.168.196.255

        inet6 fe80::20c:29ff:fe8e:e21b  prefixlen 64  scopeid 0x20<link>

        ether 00:0c:29:8e:e2:1b  txqueuelen 1000  (Ethernet)

--

        inet 127.0.0.1  netmask 255.0.0.0

        inet6 ::1  prefixlen 128  scopeid 0x10<host>

        loop  txqueuelen 1000  (Local Loopback)
```

 

## 6）-B n 显示符合条件的前2行

```
[root@zhang ~]# ifconfig |grep -B 2 "netmask"

ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500

        inet 192.168.196.131  netmask 255.255.255.0  broadcast 192.168.196.255

--



lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536

        inet 127.0.0.1  netmask 255.0.0.0
```

## **博主正在自学Linux云计算，有学习的的小伙伴可以相互交流，增强技术。**

---