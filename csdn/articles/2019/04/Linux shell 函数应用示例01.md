+++
author = "南宫乘风"
title = "Linux shell 函数应用示例01"
date = "2019-04-01 23:03:40"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/58.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88959650](https://blog.csdn.net/heian_99/article/details/88959650)

**函数Function的使用**

**定义函数**

### **（1）**

**函数名称() {<!-- --><br>     ...<br>     ...**

**}**

### **(2)**

**function 函数名称{<!-- --><br>     ...<br>     ...<br> }**

### **调用函数<br>     <br>     函数名称**

**也可以通过位置变量的方式给函数传递参数**
- 1、可以带function fun() 定义，也可以直接fun() 定义,不带任何参数。- 2、参数返回，可以显示加：return 返回，如果不加，将以最后一条命令运行结果，作为返回值。 return后跟数值n(0-255）
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

![20190401230150113.png](https://img-blog.csdnimg.cn/20190401230150113.png)

## 编写脚本，实现下面的功能<br>==============<br>    目录管理<br> 1：创建目录<br> 2：删除目录<br> 3：退出脚本<br> ==============

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
cat &lt;&lt; eof
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

![20190401230323209.png](https://img-blog.csdnimg.cn/20190401230323209.png)
