---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-14 22:06:35
description: 前面介绍简单的编写规则。现在开始编写一个简单的脚本。介绍编写脚本创建脚本文件根据需求，编写脚本测试执行脚本编写脚本，实现创建用户，病设置用户密码为注释用户创建完成，默认密码是：执行方法：利用执行加权限。。。。。。。
image: ../../title_pic/27.jpg
slug: '201903142206'
tags:
- linux
title: Linux shell简单创建用户脚本
---

<!--more-->

### 前面介绍简单的shell编写规则。

### 现在开始编写一个简单的shell脚本。

### [**Linux shell介绍**](https://blog.csdn.net/heian_99/article/details/88560250)

 

## 编写shell脚本  
   1.创建脚本文件  
   2.根据需求，编写脚本  
   3.测试执行脚本  
     
编写脚本，实现创建用户hei，病设置用户密码为root

```
[root@wei shell]# vim user.sh
```

```
#!/bin/bash
# 注释
useradd hei
echo "root" | passwd --stdin hei &> /dev/null
echo "hei用户创建完成，默认密码是：root"
```

###   
执行方法：

（1）利用bash执行

```
[root@wei shell]# bash user.sh 
```

（2）加权限，在执行

```
[root@wei shell]# chmod a+x user.sh
[root@wei shell]# ./user.sh 
```

## 变量名编写

```
[root@wei shell]# vim users.sh 
```

```
#!/bin/bash

name=wei
passwd=root

useradd $name
echo "$passwd" | passwd --stdin $name &> /dev/null
echo "用户$name创建完成，默认密码是：$passwd"
```

### 输入字符

```
[root@wei shell]# read -p "输入数字：" number
输入数字：99
```

```
#!/bin/bash
#
read -p "输入用户名：" name
read -p "输入密码：" passwd

useradd $name
echo "$name" | passwd --stdin $name &> /dev/null
echo "用户$name创建完成，密码是：$passwd"
```

# 以上三种方法都可以。