---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-17 20:00:00
description: 逻辑控制语句：分支判断结构循环结构语句结构用法；条件的写法：表达式：数学表达式字符表达式文件目录表达式数学表达式：等于不等于大于大于等于小于小于等于编写脚本，有用户输入用户名，判断用户不存在则创建请输。。。。。。。
image: ../../title_pic/52.jpg
slug: '201903172000'
tags:
- linux
title: Linux shell if条件判断1
---

<!--more-->

 

### **shell 逻辑控制语句：  
       
     分支判断结构  
       if  
       case  
     循环结构  
        for  
        while  
        until  
        **

#   
**if语句结构**

### **用法1**

**if CONDITON； then  
   statement  
   statement  
     
fi**

  
**CONDITION条件的写法：**

**       COMMAND  
      \[ expression \]  
        
expression表达式：  
       
     数学表达式  
     字符表达式  
     文件目录表达式  
       
数学表达式：  
    \[ number1 \-eq number2 \]           等于  
    \[ number1 \-ne number2 \]           不等于  
    \[ number1 \-gt number2 \]           大于  
    \[ number1 \-ge number2 \]           大于等于  
    \[ number1 \-lt number2 \]           小于  
    \[ number1 \-le number2 \]           小于等于  
    **

### **编写脚本，有用户输入用户名，判断用户不存在则创建**

 

```
[root@wei shell]# vim if.sh
```

```
#!/bin/bash
#
read -p "请输入用户名： " name

id $name &> /dev/null
if [ $? -ne 0 ];then
read -p "输入密码：" passwd
useradd $name
echo "$passwd" | passwd --stdin $name &> /dev/null
echo "用户$name创建完成，初始密码为：$passwd"
fi
```

###   
**检测语法执行状况**

```
[root@wei shell]# bash -x if.sh 
+ read -p '请输入用户名： ' name
请输入用户名： wei
+ id wei
+ '[' 1 -ne 0 ']'
+ read -p 输入密码： passwd
输入密码：123456
+ useradd wei
+ echo 123456
+ passwd --stdin wei
+ echo 用户wei创建完成，初始密码为：123456
用户wei创建完成，初始密码为：123456
```

## **检测语法错误**

```
[root@wei shell]# bash -n if.sh 
```

## **条件语言脚本**

# **用法2： 单分支if**

**if CONDITON； then  
   statement  
   statement**

**else  
   statement  
   statement  
fi**

  
**编写脚本，由用户输入用户名，判断用户不存在则创建，并设置用户第一次登陆系统时需要修改密码。否则提示用户已存在**

```
#!/bin/bash
#
read -p "请输入用户名： " name

if id $name &> /dev/null ;then
   echo " 用户$name已经存在"
else
   useradd $name
   read -p "输入密码：" passwd
   echo "$passwd" | passwd --stdin $name &> /dev/null
   passwd -e $name &> /dev/null   
   echo "用户$name创建完成，初始密码为：$passwd"
fi
```

## **由用户输入一个用户名，判断用户的UID和GID**

### **判断的方式**

**\[root\@wei shell\]# grep "hei" /etc/passwd  
hei:x:1000:1000::/home/hei:/bin/bash  
\[root\@wei shell\]# grep "hei" /etc/passwd | awk \-F: '\{print \$3,\$4\}'  
1000 1000  
\[root\@wei shell\]# id \-u hei  
1000  
\[root\@wei shell\]# id \-g hei  
1000**

### **脚本语法**

```
#!/bin/bash
#
read -p "输入用户名：" name
user_id=$(id -u $name)
group_id=$(id -g $name)

if [ $user_id -eq $group_id  ];then
   echo "Good"
else
   echo "Bad"
fi
```

###   
**执行结果**

```
[root@wei shell]# bash id.sh 
输入用户名：hei
Good
[root@wei shell]# id hei
uid=1000(hei) gid=1000(hei) 组=1000(hei)
[root@wei shell]# usermod -u 1200 hei
[root@wei shell]# id hei
uid=1200(hei) gid=1000(hei) 组=1000(hei)
[root@wei shell]# bash id.sh 
输入用户名：hei
Bad
```