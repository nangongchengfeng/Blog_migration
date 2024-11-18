---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-03-20 21:03:56
description: 语句使用于需要进行多重分支的应用情况分支判断结构语法：变量名称语句结构特点如下：行尾必须为单词每个模式必须以右括号结束双分号表示命令序列结束语句结构特点如下：匹配模式中可是使用方括号表示一个连续的范围。。。。。。。
image: http://image.ownit.top/4kdongman/93.jpg
tags:
- linux
title: Linux shell case条件判断及位置变量
---

<!--more-->

### case语句使用于需要进行多重分支的应用情况

###   
case分支判断结构

**语法：**

**case 变量名称 in  
     value1\)  
         statement  
         statement  
         ;;  
     value2\)  
         statement  
         statement  
         ;;  
     \*\)  
         statement  
         statement  
         ;;       
esac**  
     

**case语句结构特点如下：  
case行尾必须为单词 in 每个模式必须以右括号 ） 结束  
双分号 ;; 表示命令序列结束  
case语句结构特点如下：  
匹配模式中可是使用方括号表示一个连续的范围，如\[0-9\]；使用竖杠符号“|”表示或。  
最后的“\*）”表示默认模式，当使用前面的各种模式均无法匹配该变量时，将执行“\*）”后的命令序列。**

 

## 编写脚本，判断用户输入的字符串

```
#!/bin/bash
#

read -p "输入字符串：" str

case $str in
     linux|Linux)
        echo "windows"
        ;;
     windows|Windows)
        echo "linux"
        ;;
     *)
        echo "other"
        ;;
esac
```

### 运行效果：

```
[root@wei case]# bash 1.sh 
输入字符串：linux
windows
```

##   
特殊变量：  
     
   位置变量  
       \$1,\$2,\$3...........\$9,\$1\{10\}  
         
        \$1:命令的第1个参数  
               
        \$0  命令本身  
          
        \$#  命令参数的个数  
          
使用位置变量

```
#!/bin/bash
#


case $1 in
        linux|Linux)
                echo "windows"
                ;;
        windows|Windows)
                echo "linux"
                ;;
        *)
                echo "other"
esac
```

###   
执行效果

```
[root@wei case]# ./2.sh linux
windows
```

## 判断字符是为空

```
#!/bin/bash
#

if [ -z $1 ];then #判断字符串是否为空
    echo "使用：./2.sh{linux/windows}"
    exit 9
fi

case $1 in
    linux|Linux)
        echo "windows"
        ;;
    windows|Windows)
        echo "linux"
        ;;
    *)
        echo "other"
esac
```

### 执行效果

```
[root@wei case]# ./2.sh 
使用：./2.sh{linux/windows}
```

### **\$0  命令本身      
\$#  命令参数的个数**

### **示例：**

```
#!/bin/bash
#

if [ $# -ne 1 ];then
    echo "使用：$0{linux/windows}"
    exit 9
fi

case $1 in
    linux|Linux)
        echo "windows"
        ;;
    windows|Windows)
        echo "linux"
        ;;
    *)
        echo "other"
esac

```

###   
执行效果：

```
[root@wei case]# /shell/case/2.sh 
使用：/shell/case/2.sh{linux/windows}
[root@wei case]# ./2.sh 
使用：./2.sh{linux/windows}        
```

###   
          
去除文件所在的路径名：

**basename \[路径文件\]**

```
[root@wei case]# basename /etc/fstab 
fstab
```

获取文件所在的路径名：

**dirname \[路径文件\]**  
        

```
[root@wei case]# dirname /etc/fstab 
/etc
```

### 脚本

```
#!/bin/bash
#

if [ $# -ne 1 ];then
    echo "使用：$(basename $0){linux/windows}"
    exit 9
fi

case $1 in
    linux|Linux)
        echo "windows"
        ;;
    windows|Windows)
        echo "linux"
        ;;
    *)
        echo "other"
esac
        
```

###   
执行效果   

```

[root@wei case]# /shell/case/2.sh 
使用：2.sh{linux/windows}
```