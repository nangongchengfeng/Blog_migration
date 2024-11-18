---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-14 20:59:55
description: 处理文本工具：过滤文本内容：编辑文本内容显示文本：报告生成器，以特定的条件查找文本内容，在以特定的格式显示命令的格式：：用文本字符与正则表达式元字符描述的条件，可以省略不写指定输出项的格式：格式必须写。。。。。。。
image: http://image.ownit.top/4kdongman/74.jpg
tags:
- linux
title: Linux shell awk中print及变量使用
---

<!--more-->

## **Linux处理文本工具  
    grep： 过滤文本内容  
    sed：  编辑文本内容  
    awk:   显示文本  
      
awk：  Aho Peter Weinberger  Kernighan  
报告生成器，以特定的条件查找文本内容，在以特定的格式显示**

### **awk命令的格式：**

**\# awk \[option\] 'script' file1 file2...**

**\# awk \[option\] 'PATTERM\{action\}' file1 file2...**

**PATTERN：  
    用文本字符与正则表达式元字符描述的条件，可以省略不写**

**action:  
    print  
    printf  指定输出项的格式：格式必须写**

### **option选项：  
    -F  指定文本分割符  
      
awk处理文本机制：  
awk将符合PATTERN的文本逐渐取出，并按照指定的分割符（默认为空白，通过—F选项可以指定分割符）进行分割，然后将分割后的每段按照特定的格式输出**

##   
**awk的输出：**

**一 print**

**print的使用格式：  
    print item1，item,...**

### **注意：**

  
**1，各项目间使用逗号分隔开，而输出时以空白字符串为分隔  
2，输出的item可以为字符串，数值，当前的记录的字段（\$1）,变量或者awk的表达式，数值会先转换字符串，然后输出  
3，print命令后面的item可以省略，此时其功能相当于print（\$0代表未分割的整行文本内容），因此，如果想输出空行，则需要使用print "";**

###   
**以空白分割，显示文本的第一段及第二段内容**

```
[root@wei awk]# awk '{print $1,$3}' print.txt 
i wei
i zhang
```

```
[root@wei awk]# awk '{print "hello",$3}' print.txt 
hello wei
hello zhang
```

###   
**显示passwd的用户名称**

```
[root@wei awk]# awk -F: '{print $1}' /etc/passwd
root
bin
daemon
adm
lp
```

###   
**显示设备的挂载情况**

```
[root@wei awk]# df -hT | sed '1d' | awk '{print "设备名称：",$1,"挂载点：",$7,"总容量：",$3}'
设备名称： /dev/mapper/centos-root 挂载点： / 总容量： 17G
设备名称： devtmpfs 挂载点： /dev 总容量： 476M
设备名称： tmpfs 挂载点： /dev/shm 总容量： 488M
```

#   
**awk变量**

### **1 awk内置变量之记录变量**

**FS：指定读取文本时，所使用的行分隔符，默认为空白字符，相当于awk的—F选项  
OFS：指定输出的分隔符，默认为空白字符；**

 

```
[root@wei awk]# head -n 1 /etc/passwd | awk -F: '{print $1,$7}'
root /bin/bash
```

**FS模式**

```
[root@wei awk]# head -n 1 /etc/passwd | awk 'BEGIN{FS=":"}{print $1,$7}'
root /bin/bash
```

**OFS模式**

```
[root@wei awk]# head -n 1 /etc/passwd | awk -F: 'BEGIN{OFS="---"}{print $1,$7}'
root---/bin/bash
```

  
**模式混合**

```
[root@wei awk]# head -n 1 /etc/passwd | awk 'BEGIN{FS=":";OFS="---"}{print $1,$7}'
root---/bin/bash
```

###   
**2  awk内置变量之数据变量**

**NR：记录awk所处理的文本行数，如果有多个文件，所有的文件统一进行计数**

```
第 1 行内容： 127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
第 2 行内容： ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
第 3 行内容： \S
第 4 行内容： Kernel \r on an \m
第 5 行内容： 
```

**注意：  
print在显示变量值时，不要使用\$**

**FNR：记录awk所处理的文本行数，如果有多个文件，所有的文件分别进行计数**

```
[root@wei awk]# awk '{print "第",FNR,"行内容：",$0}' /etc/hosts /etc/issue
第 1 行内容： 127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
第 2 行内容： ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
第 1 行内容： \S
第 2 行内容： Kernel \r on an \m
第 3 行内容：
```

  
**NF：记录awk正在处理的当前行被分隔成几个字段**

```
[root@wei awk]# cat print.txt 
i am wei
i am zhang
[root@wei awk]# awk '{print NF}' print.txt 
3
3
[root@wei awk]# awk '{print $NF}' print.txt 
wei
zhang
```

### **3 用户自定义的变量**

**awk允许用户自定义变量，变量名称不能以数字开头，且区分大小写**

**示例： **

**方法一：使用-v选项**

```
[root@wei awk]# head -n 3 /etc/passwd | awk -v test="hello" -F: '{print test,$1}'
hello root
hello bin
hello daemon
```

**方法二：在BEGIN\{\}模式自定义变量**

```
[root@wei awk]# head -n 3 /etc/passwd | awk -F: 'BEGIN{test="hello"}{print test,$1}'
hello root
hello bin
hello daemon
```