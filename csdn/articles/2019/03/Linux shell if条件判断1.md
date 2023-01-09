+++
author = "南宫乘风"
title = "Linux shell if条件判断1"
date = "2019-03-17 20:00:00"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/50.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88625227](https://blog.csdn.net/heian_99/article/details/88625227)

 

### **shell 逻辑控制语句：<br>      <br>      分支判断结构<br>        if<br>        case<br>     循环结构<br>         for<br>         while<br>         until<br>         **

# <br>**if语句结构**

### **用法1**

**if CONDITON； then<br>    statement<br>    statement<br>    <br> fi**

<br>**CONDITION条件的写法：**

**       COMMAND<br>       [ expression ]<br>       <br> expression表达式：<br>      <br>      数学表达式<br>      字符表达式<br>      文件目录表达式<br>      <br> 数学表达式：<br>     [ number1 -eq number2 ]           等于<br>     [ number1 -ne number2 ]           不等于<br>     [ number1 -gt number2 ]           大于<br>     [ number1 -ge number2 ]           大于等于<br>     [ number1 -lt number2 ]           小于<br>     [ number1 -le number2 ]           小于等于<br>     **

### **编写脚本，有用户输入用户名，判断用户不存在则创建**

 

```
[root@wei shell]# vim if.sh
```

```
#!/bin/bash
#
read -p "请输入用户名： " name

id $name &amp;&gt; /dev/null
if [ $? -ne 0 ];then
read -p "输入密码：" passwd
useradd $name
echo "$passwd" | passwd --stdin $name &amp;&gt; /dev/null
echo "用户$name创建完成，初始密码为：$passwd"
fi
```

### <br>**检测语法执行状况**

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

**if CONDITON； then<br>    statement<br>    statement**

**else<br>    statement<br>    statement<br> fi**

<br>**编写脚本，由用户输入用户名，判断用户不存在则创建，并设置用户第一次登陆系统时需要修改密码。否则提示用户已存在**

```
#!/bin/bash
#
read -p "请输入用户名： " name

if id $name &amp;&gt; /dev/null ;then
   echo " 用户$name已经存在"
else
   useradd $name
   read -p "输入密码：" passwd
   echo "$passwd" | passwd --stdin $name &amp;&gt; /dev/null
   passwd -e $name &amp;&gt; /dev/null   
   echo "用户$name创建完成，初始密码为：$passwd"
fi
```

## **由用户输入一个用户名，判断用户的UID和GID**

### **判断的方式**

**[root@wei shell]# grep "hei" /etc/passwd<br> hei:x:1000:1000::/home/hei:/bin/bash<br> [root@wei shell]# grep "hei" /etc/passwd | awk -F: '{print $3,$4}'<br> 1000 1000<br> [root@wei shell]# id -u hei<br> 1000<br> [root@wei shell]# id -g hei<br> 1000**

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

### <br>**执行结果**

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

 
