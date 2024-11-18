---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-09 22:21:30
description: 处理文本文件的工具过滤文件内容编辑文件内容正则表达式正则表达式在处理文本时是逐行读取文件内容，读到匹配的行就根据指令做操作，不匹配就跳过。是下一款功能强大的非交互流式文本编辑器，可以对文本文件进行增、。。。。。。。
image: ../../title_pic/57.jpg
slug: '201904092221'
tags:
- linux
title: Linux shell sed命令使用
---

<!--more-->

**Linux处理文本文件的工具:**

**    grep        过滤文件内容  
    sed            编辑文件内容  
    awk  
            正则表达式Regex  
              
正则表达式Regex**

 

**sed在处理文本时是逐行读取文件内容，读到匹配的行就根据指令做操作，不匹配就跳过。**

**sed是Linux下一款功能强大的非交互流式文本编辑器，可以对文本文件进行增、删、改、查等操作，支持按行、按字段、按正则匹配文本内容，灵活方便，特别适合于大文件的编辑。本文主要介绍sed的一些基本用法，并通过shell脚本演示sed的使用实例。**

 

### **\(1\)匹配单个字符的元字符**

**    .  
      
    \[abc\]    \[a-z\]    \[A-Z\]    \[0-9\]    \[a-zA-Z0-9\]    \[\^a-z\]  
      
    \[\[:alpha:\]\]        \[\[:upper:\]\]        \[\[:lower:\]\]     \[\[:digit:\]\]**

###   
**      
\(2\)匹配字符出现位置**

**    \^str   以...开头  
    str\$   以...结尾  
    \^\$        空行**

### **\(3\)匹配字符出现的次数**

**    \*      
    \\\?  
    \\+  
    \\\{3\\\}  
    \\\{2,5\\\}  
    \\\{2,\\\}**

#   
**      
sed: Stream Editor 流编辑器**

**    行编辑器  逐行编辑  
      
将每行内容读入到内存中，在内存中进行处理，将结果返回给屏幕，此段内存空间称为摸索空间**

**默认不编写原文件，仅对模式空间的数据进行处理，处理结束后，将模式空间的内容显示到屏幕**

### **sed命令的使用格式**

**\# sed \[option\] scripts file1 file2...**

**\# sed \[option\] 'AddressCommand' file1 file ...**

**    Address:表示对那些进行处理  
    Command：操作命令  
      
    option选项：  
        \-n:不在显示模式空间的内容（默认显示）  
        \-i：直接修改原文件  
        \-e：‘AddressCommand’ \-e ‘AddressCommand’：同时执行多个匹配操作  
             \[root0shell \~\]+ sed \-e ‘/\^#/d’ \-e '/\^5/d' /etc/fstab  
          
        \-f：FILE将多个AddressCommand保存至文件中，每行一个AddressCommand;读取该文件中的操作同时执行多个操作**

  
**         \-r:表示使用扩展正则表达式**

  
**Address表示方法:  
\(1\)StartLine, EndLine  
    1, 100  
    1,\$**

**\(2\)lineNumber  
    3**

**\(3\)Startline, tn**

**    5,+2     /root/,+2**

**\(4\)/正则表达式/**

**    /root/  
    /bash\$/**

**\(5\)/正则表达式1/, /正则表达式2/  
    第1次被Regex1匹配的行升始，到第1次被Regex2匹配的行中同的所有行**

# **d删除**

**删除前4行**

```
[root@wei init.d]# sed '1,4d' nginx.sh 
```

**删除最后一行**

```
[root@wei init.d]# sed '$d' nginx.sh 
```

**删除#开头的行**

```
[root@wei ~]# sed '/^#/d' /etc/fstab
```

**删除/开头的行**

```
[root@wei ~]# sed '/^\//d' /etc/fstab 
```

**删除带数字的行**

```
[root@wei ~]# sed '/[0-9]/d' /etc/fstab 
```

### **p 显示符合条件的行**

  
**   
 显示以/开头的行**

```
[root@wei ~]# sed -n '/^\//p' /etc/fstab 
```

### **a  \\string  在符合条件的行后追加新行，string为追加的内容**

**    在以/开头的行后面追加# hello word  
    **

```
    [root@wei ~]# sed '/^\//a\# hello word' /etc/fstab 
```

**    在以/开头的行后面分别追加# hello word  # hello linux**

```
    [root@wei ~]# sed '/^\//a\# hello word' /etc/fstab 
```

### **i     \\string  在符合条件的行前追加新行，string为追加的内容**

  
**    在文件的第一行追加 # hello linux  
    **

```
    [root@wei ~]# sed '1i \# hello linux' /etc/fstab 
```

### **c   \\string 替换指定的内容**

**    将文件中最后一行的内容替换为 end of file  
    **

```
    [root@wei ~]# sed '$c\end of file' /etc/fstab 
```

### **      
\=   用于显示每一行的行号**

  
**    显示/etc/passwd文件最后一行的行号**

```
    [root@wei ~]# sed -n '$=' /etc/passwd

```

###   
**r  file\_name   将指定的文件的内容添加到符合条件的后面**

**    将文件的第二行后面追加/etc/fstab  
    **

```
    [root@wei ~]# sed '2r /etc/issue' /etc/fstab 
```

###   
**w  file\_name   将符合条件的内容另存到指定的文件中**

  
**    将以#开头的行另存到/1.txt中  
    **

```
    [root@wei ~]# sed '/^#/w /root/1.txt' /etc/fstab 
```

#   
**查找并替换**

**默认情况下，只替换每一行第一次出现的字符**

**s  /old/new/\[修饰符\]  
      
    old:正则表达式/  
    new：替换的内容  
      
    修饰符  
        g：替换第一行所有的字符  
        i：忽略大小写**

### **查找文件的UUID，并替换成uuid**

```
[root@wei ~]# sed 's/UUID/uuid/' /etc/fstab 
```

### **将行首的/替换成#**

```
[root@wei ~]# sed 's/^\//#/' /etc/fstab 
```

```
[root@wei ~]# sed 's|/|#|g' /etc/fstab 
```

### **将每一行出现的所有/替换成\@**

```
[root@wei ~]# sed 's/\//@/g' /etc/fstab
```