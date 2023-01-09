+++
author = "南宫乘风"
title = "Linux shell 数组"
date = "2019-04-11 23:04:58"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/08.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89222331](https://blog.csdn.net/heian_99/article/details/89222331)

 

# **Shell 数组**

**数组中可以存放多个值。Bash Shell 只支持一维数组（不支持多维数组），初始化时不需要定义数组大小（与 PHP 类似）。**

**与大部分编程语言类似，数组元素的下标由0开始。**

**Shell 数组用括号来表示，元素用"空格"符号分割开，语法格式如下：**

```
array_name=(value1 ... valuen)
```

**我们也可以使用下标来定义数组:**

```
array_name[0]=value0
array_name[1]=value1
array_name[2]=value2
```

**读取数组**

**读取数组元素值的一般格式是：**

```
${array_name[index]}
```

**数组 Array<br>     <br>     一段连续的内存空间**

### <br>**    <br>(1)定义数组**

```
[root@wei ~]# aa[0]=hei
[root@wei ~]# aa[1]=wei
[root@wei ~]# aa[2]=zhang
[root@wei ~]# hei=(192.168.196.1 192.168.196.2 192.168.196.3)
[root@wei ~]# echo ${hei[1]}
192.168.196.2
[root@wei ~]# echo ${hei[*]}
192.168.196.1 192.168.196.2 192.168.196.3
```

## **(2)删除数组**

```
[root@wei ~]# unset hei
[root@wei ~]# echo ${hei[*]}
```

### <br>**(3)获取数组的长度**

```
[root@wei ~]# aa=(tom hei zhang wei)
[root@wei ~]# echo ${aa[*]}
tom hei zhang wei
[root@wei ~]# echo ${#aa[*]}
4
[root@wei ~]# echo ${#aa[@]}
4
```

### **编写脚本，找出数组中最大数**

 

```
#!/bin/bash
#

number=(53 54 654 45 677 46 999)
max=${number[0]}
for i in `seq 7`;do
        if [ ${number[$i]} -gt $max ];then
                max=${number[$i]}
        fi
done
echo $max
```

# **随机数**

```
[root@wei ~]# echo $RANDOM
10803
[root@wei ~]# echo $RANDOM
5555
```

 
