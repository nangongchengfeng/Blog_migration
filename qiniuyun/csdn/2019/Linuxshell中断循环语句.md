---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-23 22:26:25
description: 无限循环：循环有限的生命，他们跳出来，一旦条件是还是取决于循环。由于所需的条件是不符合一个循环可能永远持续下去。永远不会终止执行一个循环执行无限次数。出于这个原因，这样的循环被称为无限循环。语句：语句。。。。。。。
image: ../../title_pic/62.jpg
slug: '201903232226'
tags:
- linux
title: Linux shell 中断循环语句
---

<!--more-->

## 无限循环：

循环有限的生命，他们跳出来，一旦条件是 false 还是 false 取决于循环。

由于所需的条件是不符合一个循环可能永远持续下去。永远不会终止执行一个循环执行无限次数。出于这个原因，这样的循环被称为无限循环。

## break语句：

break语句用于终止整个循环的执行，完成后所有行代码break语句的执行。然后，它逐级的代码跟在循环结束。

## continue 语句:

continue语句break命令类似，但它会导致当前迭代的循环退出，而不是整个循环。

这种参数是有用的，当一个错误已经发生，但你想尝试执行下一个循环迭代。

### 中断循环的语句  
     break     中断整体循环  
     contiune  中断本次循环  
       
break用法：

### 编写脚本，判断大于3000的累加和的数

```
#!/bin/bash
#

sum=0
for i in `seq 100`;do
    let sum=$sum+$i
    if [ $sum -ge 3000 ];then
        echo $i
        break
    fi
done
```

## contiune用法：

###   
编写脚本，求100的奇数的累加和

```
#!/bin/bash 
#

sum=0
for i in `seq 100`;do
    let ys=$i%2
    if [ $ys -eq 0 ];then
        continue
    fi
    let sum=$sum+$i
done
echo $sum
```

##   
编写脚本，输出在/bin/bash的前5个用户

```
#!/bin/bash
#
number=0
line=$(wc -l /etc/passwd |awk '{print $1}')
for i in `seq $line`;do
    sh_name=$(head -n $i /etc/passwd | tail -n 1 | awk -F: '{print $7}')
    if [ $sh_name = "/bin/bash" ]; then
        user_name=$(head -n $i /etc/passwd | tail -n 1 | awk -F: '{print $1}' )
        echo $user_name
        let number=$number+1
    fi

    if [ $number -ge 5 ];then
        break
    fi

done
```

### 执行效果

```
[root@wei break]# bash 2.sh 
root
mysql
hei
wei
a
[root@wei break]# ls /home/
a  c  d  hei  user1  user10  user2  user3  user4  user5  user6  user7  user8  user9  wei
```