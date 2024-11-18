---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-21 22:33:39
description: 循环结构循环结构：循环开始条件：循环操作：循环终止的条件语言，，循环语法：变量取值列表；变量取值列表上面两个用法的效果是一样的。取值列表：数字使用命令生成数字的序列字符文件示例可以快速去值，奇数等示例。。。。。。。
image: ../../title_pic/50.jpg
slug: '201903212233'
tags:
- linux
title: Linux shell for循环结构
---

<!--more-->

# **Linux Shell   for循环结构**

## **循环结构  
       
     1：循环开始条件  
     2：循环操作  
     3：循环终止的条件**

 

### **shell语言  
      
   for，while，util**

### **    
for循环**

### **语法：**

**（1）**

**for 变量 in 取值列表；do  
    statement  
    statement  
done**

**（2）**

**for 变量 in 取值列表  
do  
    statement  
    statement  
done**

**上面两个用法的效果是一样的。**

 

 

  
**取值列表：  
    数字  
        10 20 30  
        使用seq命令生成数字的序列  
            seq 10  
            seq 3 10  
            seq 1 2 10  
      
    字符  
        aa bb  cc  
      
    文件  
        **

**示例**

seq可以快速去值，奇数等

 

```
[root@wei for]# seq 5
1
2
3
4
5
[root@wei for]# seq 2 6
2
3
4
5
6
```

###   
**示例：1--100的累加和**

 

```
#!/bin/bash
#
sum=0
for i in `seq 1 100`
do
    let sum=$sum+$i
done
echo $sum 

[root@wei for]# bash 1.sh 
5050
```

###   
**示例：1--100的奇数累加和**

```
#!/bin/bash

sum=0

for i in `seq 100`
do
    let ys=$i%2
    if [ $ys -ne 0 ];then
        let sum=$sum+$i
    fi

done

echo $sum

[root@wei for]# bash 2.sh 
2500
```

###   
**创建10个用户，初始密码为：root，登陆重新修改密码**

```
#!/bin/bash
#

for i in `seq 10`
do
    if ! id user$i &> /dev/null ; then
        useradd user$i
        echo "root" | passwd --stdin user$i &> /dev/null
        passwd -e user$i &> /dev/null
        echo "用户user$i创建完成，初始密码为：root"
    else
        echo "用户user$i已经存在"
    fi
done
```

### **以字符作为取值类表**

```
#!/bin/bash
#

for name in a d c d ;do
    useradd $name
    echo "$name create finishe"
done
```

  
**以文件作为取值列表**

### **        \`cat file\`  
          
编写脚本，读取文本**

```
#!/bin/bash 
#
for i in `cat /shell/for/1.txt`;do
    echo "line:$i"
done
[root@wei for]# ./wen.sh 
line:nangong
line:chengfneg
```