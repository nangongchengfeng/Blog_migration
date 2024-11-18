---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-19 22:12:21
description: 前面介绍的判断的语法，现在再补充一点。条件判断分支判断结构下面两个结构语法，已经在前面有过示例。结构：；结构：；下面会分享几个我编写的示例，希望对大家有所帮助。编写脚本，有用户输入用户名，判断用户是否。。。。。。。
image: ../../title_pic/67.jpg
slug: '201903192212'
tags:
- linux
title: Linux shell if条件判断2
---

<!--more-->

**前面介绍linux shell的if判断的语法，现在再补充一点。**

**[Linux shell if条件判断1](https://blog.csdn.net/heian_99/article/details/88625227)**

**分支判断结构  
    if , case  
 **

**下面两个结构语法，已经在前面有过示例。**

  
**结构1：  
if CONDITON； then  
   statement  
   statement  
     
fi**

**结构2：**

**if CONDITON； then  
   statement  
   statement**

**else  
   statement  
   statement  
fi**

 

**下面会分享几个我编写的示例，希望对大家有所帮助。**

###   
**编写脚本，有用户输入用户名，判断用户是否存在，如果不存在，就显示用户不存在，如果存在，以下面格式输出用户相关信息：**

**用户名：  
宿主目录：  
shell程序：**

```
[root@wei shell]# cat if2.sh 
#!/bin/bash
#
read -p "请输入用户名：" name

if id $name &> /dev/null; then
   echo "用户名：" $name
   homedir=`grep "^$name:" /etc/passwd | awk -F: '{print $6}' `
   shname=`grep "^$name:" /etc/passwd | awk -F: '{print $7}' `
   echo "宿主目录：$homedir"
   echo "SHELL名称：$shname "
else
   echo "用户$name不存在"
fi
```

###   
**编写脚本，判断文件是否存在空行，有则显示空行个数，没有则显示文件类容，并在每一行显示行号**

```
#!/bin/bash
#
read -p "请输入文件的名称：" file

if grep "^$" $file &> /dev/null; then
   number=`grep "^$" $file | wc -l`
   echo "文件$file中的空行的数量：$number"
else
   echo "文件$file内容如下："
   cat -n $file
fi
```

##   
**用法3 ：多分支if结构**

  
**if CONDITON； then  
   statement  
   statement**

**elif CONDITON； then  
   statement  
   statement  
elif CONDITON； then  
   statement  
   statement  
else  
   statement  
   statement**

**fi**

  
**多个条件的写法：  
   AND        \[conditionl \-a condition2\]          \[conditionl \] \&\& \[ condition2\]  
   OR         \[conditionl \-o condition2\]          \[conditionl \] || \[ condition2\]**

### **编写脚本，判断当前系统时间的小时数字**

**   9--11       morning  
   12--14      noon  
   15--18      afternoon  
               night  
          
        **

```
#!/bin/bash
#
hour=`date +%H`
if [ $hour -ge 9 -a $hour -le 11 ]; then
   echo "Morning" 
elif [ $hour -ge 12 -a $hour -le 14 ]; then
   echo " Noon"
elif [ $hour -ge 15 -a $hour -le 18 ]; then
   echo " Afternoon"
else
   echo "Night"
fi
```

**执行效果：**

```
[root@wei shell]# date
2019年 03月 19日 星期二 18:44:50 CST
[root@wei shell]# bash shi.sh 
 Afternoon
```

**数学表达式**

**字符表达式  
 \[ str1 == str2 \]  
 \[ str1 \!= str2 \]  
 \[ \-z  str1  \]   判断字符串是否为空**

### **判断两次密码是否相同 **

```
#!/bin/bash
#
read -p "请输入密码：" pwd1
read -p "请在一次输入密码：" pwd2
if [ "$pwd1" == "$pwd2" ];then
   echo "密码输入正确"
else
   echo "密码两次输入不一致"
fi
```

**文件目录表达式：  
    
     \[ \-e file \]  判断文件目录是否存在  
     \[ \-f file \]  判断是否为文件  
     \[ \-e file \]  判断是否为目录  
     \[ \-r file \]  判断文件是否有r权限  
     \[ \-w file \]  判断文件是否有w权限  
     \[ \-x file \]  判断文件是否有x权限  
     **

**双目表达式  
单目表达式  \[ \-e file \]  \[ \! \-e file \]**

## **用法4： if的内嵌语法**

  
**if CONDITON； then  
   if CONDITON； then  
      statement  
      statement  
    fi  
else  
   statement  
   statement  
fi**

### **判断用户是否存在，如果用户存在，判断他的root的id和group的id是否相同**

```
#!/bin/bsah
#
read -p "输入用户名： " name

if id $name &> /dev/null; then
   #获取uid，gid进行判断
   user_id=$(id -u $name)
   group_id=$(id -g $name)
   if [ $user_id -eq $group_id ];then
      echo " Good user"
   else
      echo "Bad user"
   fi
else
   echo "用户不存在"
fi
```

### **判断文件是否存在，如果存在输入到备份的文件去**

```
#!/bin/bash
#
read -p "输入文件的路径：" file
if [ -e $file ]; then
   read -p "输入备份的路径：" dir
   if [ -e $dir ]; then
      cp $file $dir
      echo "文件$file备份到$dir目录"
   else
       mkdir -p $dir
       cp $file $dir
       echo "文件$file备份到$dir目录"
   fi
else
   echo “文件$file不存在”
fi
```