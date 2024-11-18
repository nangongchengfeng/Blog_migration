---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-14 22:59:14
description: 的表示方法：，正则表达式，格式为以冒号为分隔符，显示以开头的行的第一段以冒号为分隔符，显示以结尾的行的第一段以冒号为分隔符，显示以或者开头的行的第一段写出的软链接的名字，表达式，有下面操作符组成的表达。。。。。。。
image: ../../title_pic/49.jpg
slug: '201904142259'
tags:
- linux
title: Linux shell awk模式使用
---

<!--more-->

# **awk的PATTERN表示方法：**

### **1，正则表达式，格式为/regex/**

**以冒号为分隔符，显示/etc/passwd以r开头的行的第一段**

```
[root@wei awk]# awk -F: '/^r/{print $1}' /etc/passwd
root
```

**以冒号为分隔符，显示/etc/passwd以nologin结尾的行的第一段**

```
[root@wei awk]# awk -F: '/nologin$/{print $1}' /etc/passwd
bin
daemon
adm
lp
mail
```

**以冒号为分隔符，显示/etc/passwd以r或者h开头的行的第一段**

```
[root@wei awk]# awk -F: '/^[rh]/{print $1}' /etc/passwd
root
halt
hei
```

  
**写出/etc/的软链接的名字**

```
[root@wei awk]# ls -l /etc/ |awk '/^l/{print $NF}'
/usr/share/icons/hicolor/16x16/apps/fedora-logo-icon.png
../boot/grub2/grub.cfg
```

### **2，表达式，有下面操作符组成的表达式**

#   
**awk的操作符**

### **1 ，算术操作符**

**\-x 负值  
+x 转换为数值，正值  
x\^y x\*\*y  次方  
x/y  
x\*y  
x-y  
x+y  
x\%y**

## **2 ,字符串操作符**

**+：实现字符串连接    "ab"+"cd"    abcd**

### **3 ,赋值操作符**

**\=  
+=  
\-+  
\*=  
、=  
\%=  
\^=  
\*\*=**

### **4 ,比较操作符**

**x\<y  
x\<=y  
x>y  
x>=y  
x==y  
x\!=y  
x\~y:x为字符串，y为模式，如果x可以被模式匹配则为真，否则为假  
x\!\~y**

### **5 ,逻辑关系符**

**\&\& 与  
|| 或者**

**显示uid大于等于500的用户的及uid**

```
[root@wei awk]# awk -F: '$3>=500{print $1,$3}' /etc/passwd
polkitd 999
saslauth 998
hei 1200
wei 1001
```

###   
**3 ，指定范围，格式为pattern,pattern2**

**以冒号为分隔符，显示uid=0到最后一个字段为nologin结尾中间所有的用户名称，uid及shell**

```
[root@wei awk]# awk -F: '$3==0,$7~"nologin$"{print $1,$3,$7}' /etc/passwd
root 0 /bin/bash
bin 1 /sbin/nologin
```

###   
**4 ，BEGIN/END, 特殊模式  
    BEGIN表示awk进行处理前执行一次操作  
    END表示awk处理完最后一行结束前执行一次操作  
      
使用BEGIN打印表头**

```
[root@wei awk]# awk -F: 'BEGIN{printf "%-10s%-10s%-20s\n","username","uid","shell"}$3==0,$7 ~ "nologin$"{printf "%-10s%-10s%-10s\n",$1,$3,$7}' /etc/passwd
username  uid       shell               
root      0         /bin/bash 
bin       1         /sbin/nologin
```

###   
**使用END打印表尾**

```
[root@wei awk]# awk -F: 'BEGIN{printf "%-10s%-10s%-20s\n","username","uid","shell"}$3==0,$7 ~ "nologin$"{printf "%-10s%-10s%-10s\n",$1,$3,$7}END{print "END OFFILE..."}' /etc/passwd
username  uid       shell               
root      0         /bin/bash 
bin       1         /sbin/nologin
END OFFILE...
```