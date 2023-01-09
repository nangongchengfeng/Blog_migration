+++
author = "南宫乘风"
title = "Linux shell case条件判断及位置变量"
date = "2019-03-20 21:03:56"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/10.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88699584](https://blog.csdn.net/heian_99/article/details/88699584)

### case语句使用于需要进行多重分支的应用情况

### <br> case分支判断结构

**语法：**

**case 变量名称 in<br>      value1)<br>          statement<br>          statement<br>          ;;<br>      value2)<br>          statement<br>          statement<br>          ;;<br>      *)<br>          statement<br>          statement<br>          ;;     <br> esac**<br>      

**case语句结构特点如下：<br> case行尾必须为单词 in 每个模式必须以右括号 ） 结束<br> 双分号 ;; 表示命令序列结束<br> case语句结构特点如下：<br> 匹配模式中可是使用方括号表示一个连续的范围，如[0-9]；使用竖杠符号“|”表示或。<br> 最后的“*）”表示默认模式，当使用前面的各种模式均无法匹配该变量时，将执行“*）”后的命令序列。**

 

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

## <br>特殊变量：<br>    <br>   位置变量<br>        $1,$2,$3...........$9,$1{10}<br>        <br>         $1:命令的第1个参数<br>              <br>         $0  命令本身<br>         <br>         $#  命令参数的个数<br>         <br>使用位置变量

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

### <br>执行效果

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

### **$0  命令本身    <br> $#  命令参数的个数**

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

### <br>执行效果：

```
[root@wei case]# /shell/case/2.sh 
使用：/shell/case/2.sh{linux/windows}
[root@wei case]# ./2.sh 
使用：./2.sh{linux/windows}        
```

### <br>         <br>去除文件所在的路径名：

**basename [路径文件]**

```
[root@wei case]# basename /etc/fstab 
fstab
```

获取文件所在的路径名：

**dirname [路径文件]**<br>         

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

### <br>  执行效果      

```

[root@wei case]# /shell/case/2.sh 
使用：2.sh{linux/windows}
```

<br>         <br>  <br>         <br>         <br>         <br>         
