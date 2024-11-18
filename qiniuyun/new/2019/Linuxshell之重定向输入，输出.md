---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-12 22:28:21
description: 是一个命令解释器，它在操作系统的最外层，负责直接与用户对话，把用户的输入解释给操作系统，并处理各种各样的操作系统的输出结果，输出到屏幕返回给用户。这种对话方式可以是交互的方式从键盘输入命令，可以立即得。。。。。。。
image: http://image.ownit.top/4kdongman/63.jpg
tags:
- linux
title: Linux shell之重定向输入，输出
---

<!--more-->

shell是一个命令解释器，它在操作系统的最外层，负责直接与用户对话，把用户的输入解释给操作系统，并处理各种各样的操作系统的输出结果，输出到屏幕返回给用户。这种对话方式可以是交互的方式（从键盘输入命令，可以立即得到shell的回应），或非交互（执行脚本程序）的方式。  
下图的黄色部分就是命令解释器shell处于的操作系统中位置形象图解。

![](http://image.ownit.top/csdn/1066162-20180726074043035-450540228.png)

# **Linux SHELL 脚本**

     大量重复执行的工作  
       
     shell（Linux壳）， 一类程序的名称  
       
     文本文件----->shell命令，/bin/bash提供逻辑控制语句

###   
重定向向符号的使用  
    /dev/stdin     标准输入设备（键盘）        0  
    /dev/stdout    标准输出设备（显示器）      1  
    /dev/stderr    标准错误输出设备（显示器）  2

![](http://image.ownit.top/csdn/20190312222311388.png)

      
输出重定向符号  
      
    >  覆盖原文件信息  
    >>  往原文件后面追加类容  
    

    >  >>   用于重定向标准输出  
          
      

```
[root@wei ~]# ls -ldh /etc/ /tmp/1.txt
[root@wei ~]# ls -ldh /tmp/ >>/tmp/1.txt 
```

    2>  2>>     用于重定向标准错误输出  
       

```
 [root@wei ~]# ls -ldh /qwertyuasdfgh 2> /tmp/1.txt   
```

   

    \&>  同时重定向标准输出及标准错误输出  
      
        特殊设备文件：/dev/null （垃圾站）  
          
  

```
      [root@wei ~]# ls -ldh /etc/ &>/dev/null 
      [root@wei ~]# grep "root" /etc/passwd &> /dev/null 
```

  
输入重定向符号  
 

```
[root@wei ~]# cat /tmp/1.txt 
chengfeng
[root@wei ~]# tr 'a-z' 'A-Z' < /tmp/1.txt 
CHENGFENG
```

##    
输出信息：

### 1  echo

```
[root@wei ~]# echo "请输出你的选择"    #默认会打印换行符
请输出你的选择

[root@wei ~]# echo -n "请输出你的选择"
请输出你的选择[root@wei ~]# 

[root@wei ~]# echo -e "a\nbb\nccc"     # \n 回车
a
bb
ccc

[root@wei ~]# echo -e "a\tbb\tccc"     # \t tab键
a    bb    ccc
```

###   
2  printf

```
[root@wei ~]# printf "hello wowrd"
hello wowrd[root@wei ~]# 
```

3 HERE DOCUMENT   \----->输出多行信息

```
[root@wei ~]# cat << eof  （eof为提示符，可以任意定义）
> 选择
> 安装
> 重启
> 关机
> eof
选择
安装
重启
关机
```

## 双引号和单引号的区别：

单引号：所有字符会失去原有的含义  
双引号：特殊的字符会转义

### 如何交互命令:

```
[root@wei ~]# echo "root" | passwd --stdin hei &> /dev/null

[root@wei ~]# echo -e "n\rp\r1\r+100M\rw\r" | fdisk /dev/vdb &> /dev/null 
```

显示历史命令

```
[root@wei ~]# history
```

执行历史命令的某一条

```
[root@wei ~]# !254
```

清空历史命令

```
[root@wei ~]# history -c
```