---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-01 19:32:44
description: ：明确循环次数：不确定循环换次数循环；改变循环条件真假的语句编写脚本，计算的和编写循环，输入退出不输入，不退出请输入你的选择：输入错误加的颜色代码请输入你的选择：；退出编写循环，输入退出不输入，不退出。。。。。。。
image: http://image.ownit.top/4kdongman/99.jpg
tags:
- linux
title: Linux shell while循环语句
---

<!--more-->

### **for ：明确循环次数  
while ：不确定循环换次数**

### **while循环**

### （1）

**while CONDITION；do  
      statement  
      statement  
      \<改变循环条件真假的语句>  
done**

### 编写脚本，计算1--100的和

```
#!/bin/bash
#
sum=0
i=1

while [ $i -le 100  ];do
    let sum=$sum+$i
    let i=$i+1
done

echo $sum
```

###   
编写while循环，输入q退出（不输入q，不退出）

```
#!/bin/bash
#
read -p "请输入你的选择：" choice

while [ $choice != q  ];do
    echo -e "\033[31m输入错误\033[0m" #加的颜色代码
    read -p "请输入你的选择：" choice
done
```

### ![](http://image.ownit.top/csdn/20190401192859102.png)  
**（2）**

while true；do  
      statement  
      statement  
      \<break退出>  
done

 

### 编写while循环，输入q退出（不输入q，不退出）

```
#/bin/bash
#
while true;do
    read -p "请输入你的选择" str
    echo "输入错误"
    if [ $str == q ];then
        break
    fi
done
```

### 编写脚本，每4秒查看系统的内存

```
#!/bin/bash
#
while true;do
    uptime
    sleep 3
done
```

![](http://image.ownit.top/csdn/20190401193025486.png)  
**（3）**

while read line;do  
    statement  
    statement  
done \< file

###   
编写脚本，向系统每个用户打招呼

```
v#!/bin/bash
#
while read line;do
    sh_name=$(echo $line | awk -F: '{print $1}')
    echo "Hello $sh_name"

done < /etc/passwd
```

### ![](http://image.ownit.top/csdn/20190401193117987.png)  
编写脚本，统计/bin/bash /sbin/nologin的个数

```
[root@wei while]# cat 6.sh 
#!/bin/bash
#
bash_number=0
nologin_number=0

while read line;do
    sh_name=$(echo $line | awk -F: '{print $7}')
    case $sh_name in
        /bin/bash)
            let bash_number=$bash_number+1
            ;;
        /sbin/nologin)
            let nologin_number=$nologin_number+1
            ;;
    esac

done < /etc/passwd

echo "bash用户数量：$bash_number"
echo "nologin_number用户数量：$nologin_number"
```

### 执行效果

```
[root@wei while]# ./6.sh 
bash用户数量：17
nologin_number用户数量：17
```

![](http://image.ownit.top/csdn/20190401193158805.png)

###   
util循环：

### util CONDITION；do  
    statement  
    statement  
done

### **条件为假时，执行循环，条件为真时，结束循环**

#   
重点掌握

# if，case

# for，while