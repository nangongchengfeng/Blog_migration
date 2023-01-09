+++
author = "南宫乘风"
title = "Linux shell之重定向输入，输出"
date = "2019-03-12 22:28:21"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/58.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88430654](https://blog.csdn.net/heian_99/article/details/88430654)

shell是一个命令解释器，它在操作系统的最外层，负责直接与用户对话，把用户的输入解释给操作系统，并处理各种各样的操作系统的输出结果，输出到屏幕返回给用户。这种对话方式可以是交互的方式（从键盘输入命令，可以立即得到shell的回应），或非交互（执行脚本程序）的方式。<br> 下图的黄色部分就是命令解释器shell处于的操作系统中位置形象图解。

![1066162-20180726074043035-450540228.png](https://images2018.cnblogs.com/blog/1066162/201807/1066162-20180726074043035-450540228.png)

# **Linux SHELL 脚本**

     大量重复执行的工作<br>      <br>      shell（Linux壳）， 一类程序的名称<br>      <br>      文本文件-----&gt;shell命令，/bin/bash提供逻辑控制语句

### <br>重定向向符号的使用<br>     /dev/stdin     标准输入设备（键盘）        0<br>     /dev/stdout    标准输出设备（显示器）      1<br>     /dev/stderr    标准错误输出设备（显示器）  2

![20190312222311388.png](https://img-blog.csdnimg.cn/20190312222311388.png)

    <br>输出重定向符号<br>     <br>     &gt;  覆盖原文件信息<br>     &gt;&gt;  往原文件后面追加类容<br>     

    &gt;  &gt;&gt;   用于重定向标准输出<br>         <br>       

```
[root@wei ~]# ls -ldh /etc/ /tmp/1.txt
[root@wei ~]# ls -ldh /tmp/ &gt;&gt;/tmp/1.txt 
```

    2&gt;  2&gt;&gt;     用于重定向标准错误输出<br>        

```
 [root@wei ~]# ls -ldh /qwertyuasdfgh 2&gt; /tmp/1.txt   
```

   

    &amp;&gt;  同时重定向标准输出及标准错误输出<br>     <br>         特殊设备文件：/dev/null （垃圾站）<br>         <br>   

```
      [root@wei ~]# ls -ldh /etc/ &amp;&gt;/dev/null 
      [root@wei ~]# grep "root" /etc/passwd &amp;&gt; /dev/null 
```

<br>输入重定向符号<br>  

```
[root@wei ~]# cat /tmp/1.txt 
chengfeng
[root@wei ~]# tr 'a-z' 'A-Z' &lt; /tmp/1.txt 
CHENGFENG
```

##  <br>输出信息：

### 1  echo

```
[root@wei ~]# echo "请输出你的选择"    #默认会打印换行符
请输出你的选择

[root@wei ~]# echo -n "请输出你的选择"
请输出你的选择[root@wei ~]# 

[root@wei ~]# echo -e "a\nbb\nccc"     # \n 回车
a
bb
ccc

[root@wei ~]# echo -e "a\tbb\tccc"     # \t tab键
a    bb    ccc
```

### <br>2  printf

```
[root@wei ~]# printf "hello wowrd"
hello wowrd[root@wei ~]# 
```

3 HERE DOCUMENT   -----&gt;输出多行信息

```
[root@wei ~]# cat &lt;&lt; eof  （eof为提示符，可以任意定义）
&gt; 选择
&gt; 安装
&gt; 重启
&gt; 关机
&gt; eof
选择
安装
重启
关机
```

## 双引号和单引号的区别：

单引号：所有字符会失去原有的含义<br> 双引号：特殊的字符会转义

### 如何交互命令:

```
[root@wei ~]# echo "root" | passwd --stdin hei &amp;&gt; /dev/null

[root@wei ~]# echo -e "n\rp\r1\r+100M\rw\r" | fdisk /dev/vdb &amp;&gt; /dev/null 
```

显示历史命令

```
[root@wei ~]# history
```

执行历史命令的某一条

```
[root@wei ~]# !254
```

清空历史命令

```
[root@wei ~]# history -c
```

 
