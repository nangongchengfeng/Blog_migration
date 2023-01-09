+++
author = "南宫乘风"
title = "Linux shell for循环结构"
date = "2019-03-21 22:33:39"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/16.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88727764](https://blog.csdn.net/heian_99/article/details/88727764)

# **Linux Shell   for循环结构**

## **循环结构<br>      <br>      1：循环开始条件<br>      2：循环操作<br>      3：循环终止的条件**

 

### **shell语言<br>     <br>     for，while，util**

### **  <br> for循环**

### **语法：**

**（1）**

**for 变量 in 取值列表；do<br>     statement<br>     statement<br> done**

**（2）**

**for 变量 in 取值列表<br> do<br>     statement<br>     statement<br> done**

**上面两个用法的效果是一样的。**

 

##  

<br>**取值列表：<br>     数字<br>         10 20 30<br>         使用seq命令生成数字的序列<br>             seq 10<br>             seq 3 10<br>             seq 1 2 10<br>     <br>     字符<br>         aa bb  cc<br>     <br>     文件<br>         **

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

### <br>**示例：1--100的累加和**

 

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

### <br>**示例：1--100的奇数累加和**

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

### <br>**创建10个用户，初始密码为：root，登陆重新修改密码**

```
#!/bin/bash
#

for i in `seq 10`
do
    if ! id user$i &amp;&gt; /dev/null ; then
        useradd user$i
        echo "root" | passwd --stdin user$i &amp;&gt; /dev/null
        passwd -e user$i &amp;&gt; /dev/null
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

<br>**以文件作为取值列表**

### **        `cat file`<br>         <br>编写脚本，读取文本**

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

 
