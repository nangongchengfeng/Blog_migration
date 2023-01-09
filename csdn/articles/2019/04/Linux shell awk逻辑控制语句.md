+++
author = "南宫乘风"
title = "Linux shell awk逻辑控制语句"
date = "2019-04-15 23:14:25"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/01.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89323274](https://blog.csdn.net/heian_99/article/details/89323274)

# **awk逻辑控制语句**

## **1，if...else**

**格式：**

**if（条件）{语句；语句} else {语句1；语句2}**

**如果statement只有一条语句，{}可以不写**

### **以冒号为分隔符，判断第一个字段，如果为root，则显示用户为administrator，否则显示用户问common user**

```
[root@wei csdn]# awk -F: '{if($3==0){print $1,"is administrator."}else {print $1,"is common user"}}' /etc/passwd
root is administrator.
bin is common user
```

### **编写uid大于500的用户个数**

```
[root@wei csdn]# awk -F: -v count=0 '{if($3&gt;500) {count++}}END{print "uid大于500的用户数量：",count}' /etc/passwd
uid大于500的用户数量： 19
```

### **判断系统的bash用户和nologin用户**

```
[root@wei csdn]# awk -v num1=0 -v num2=0 -F: '/bash$/ || /nologin$/{if($7=="/bin/bash"){num1++} else {num2++}}END{print "bash用户数量：",num1,"nologin用户数量：",num2}' /etc/passwd
bash用户数量： 17 nologin用户数量： 20
```

 

## <br>**2，while**

**格式：**

**while(条件) {语句1;语句2;.....}**

### **passwd前3行进行输出，输出3次**

```
[root@wei csdn]# head -n 3 /etc/passwd | awk '{i=1;while(i&lt;=3){print $0; i++}}'
root:x:0:0:root:/root:/bin/bash
root:x:0:0:root:/root:/bin/bash
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```

### **以冒号为分割符，判断每一行的每一个字段的长度如果大于4，则显之**

```
[root@wei awk]# head -n 3 /etc/passwd | awk -F: '{i=1;while(i&lt;=7){if(length($i)&gt;4){print $i};i++}}'
/root
/bin/bash
/sbin/nologin
daemon
daemon
/sbin
/sbin/nologin
```

### **统计test.txt的文件长度大小为5的单词**

```
[root@wei awk]# awk '{i=1;while(i&lt;NF) {if(length($i)&gt;5){print $i};i++}}' print.txt 
```

## <br>**3，for   遍历数组**

**格式：**

**for（变量定义；循环终止的条件；改变循环条件的语句） {语句；语句...}**

**    for(i=1;i&lt;=4;i++) {......}**

### **以冒号为分隔符，显示/etc/passwd每一行的前3个字段**

```
[root@wei awk]# awk -F: '{for (i=1;i&lt;=3;i++) { print $i} }' /etc/passwd
root
x
0
bin


```

## <br>**4， break contiune    <br>     <br>     用于中断循环**
