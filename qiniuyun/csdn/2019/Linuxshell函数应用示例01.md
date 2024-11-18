---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-01 23:03:40
description: 函数的使用定义函数函数名称函数名称调用函数函数名称也可以通过位置变量的方式给函数传递参数、可以带定义，也可以直接定义不带任何参数。、参数返回，可以显示加：返回，如果不加，将以最后一条命令运行结果，作为。。。。。。。
image: ../../title_pic/20.jpg
slug: '201904012303'
tags:
- linux
title: Linux shell 函数应用示例01
---

<!--more-->

**函数Function的使用**

**定义函数**

### **（1）**

**函数名称\(\) \{<!-- \-->  
    ...  
    ...**

**\}**

### **\(2\)**

**function 函数名称\{<!-- \-->  
    ...  
    ...  
\}**

### **调用函数  
      
    函数名称**

**也可以通过位置变量的方式给函数传递参数**

- 1、可以带function fun\(\) 定义，也可以直接fun\(\) 定义,不带任何参数。
- 2、参数返回，可以显示加：return 返回，如果不加，将以最后一条命令运行结果，作为返回值。 return后跟数值n\(0-255）

### 编写脚本，编写函数，并调用

```
#!/bin/bash
#

sayhei() {
 echo "$1"
}

sayhei wei
sayhei linux
sayhei windows
```

### **执行效果**

![](../../image/20190401230150113.png)

## 编写脚本，实现下面的功能  
\==============  
   目录管理  
1：创建目录  
2：删除目录  
3：退出脚本  
\==============

```
#!/bin/bash
#
create_dir(){
    read -p "输入目录名称：" dir
    if [ ! -e $dir ];then
        mkdir -p $dir
        echo “目录$dir创建完成”
    else
        echo "目录$dir存在"
    fi

}

remove_dir(){
    read -p "输入目录名称" dir
    if [ -e $dir  ];then
        rm -r $dir
        echo "目录$dir删除成功"
    fi

}
showmenu(){
cat << eof
==============
   目录管理
1.创建目录
2.删除目录
3.退出脚本
==============
eof
}
while true;do
read -p "请输入你的选择:显示菜单[m] " choice
    case $choice in
        1)
            create_dir
            ;;
        2)
            remove_dir
            ;;
        3)    
            exit 0
            ;;
        m)
            showmenu
            ;;
        *)
            echo "输入错误,请重新选择"
            ;;
    esac

done
```

## 执行效果

![](../../image/20190401230323209.png)