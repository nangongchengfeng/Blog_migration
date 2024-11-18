---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-07 23:55:11
description: 座右铭：长风破浪会有时，直挂云帆济沧海。一般查看文件或者目录有几种方法。查看文件类容只能查看文本型查看文件较少的类容查看未知类容看未知的类容文件，我们不知道有多大，就用和查看比较方便使用两者相同点：可。。。。。。。
image: ../../title_pic/09.jpg
slug: '201901072355'
tags:
- linux
title: Linux命令查找文件目录
---

<!--more-->

**座右铭：长风破浪会有时，直挂云帆济沧海。**

**linux一般查看文件或者目录有几种方法。**

**/查看文件类容--------cat/more/less/head/tail   只能查看文本型（txt）**

**（1）查看文件较少的类容**

**cat /etc/fstab**

**![](../../image/20190107233111669.png)**

**cat \-n /etc/fstab**

**![](../../image/2019010723333718.png)**

**（2）查看未知类容**

**看未知的类容文件，我们不知道有多大，就用more和less查看比较方便使用**

### **两者相同点：可以 翻页 或者 一行一行查看**

## **       不同点：more只能往下翻页，有的翻过了，就不能翻回去了**

## **                     less可以往上往下随意查看翻动**

 

### **more/less  分页显示类容**

### **more 只能往下翻（空格：翻页   回车：一行一行   q：退出）**

### **less   可以上下翻**

**less /usr/share/dict/words**

**![](../../image/2019010723400934.png)**

**（3）head/tail（头部/尾巴）**

**head**

**不写-n显示前10行类容**

**![](../../image/2019010723430748.png)**

**\[root\@chengfeng \~\]# head \-n 3 /etc/passwd\(显示前三行\)**

**![](../../image/20190107234153885.png)**

**Tail**

**不写-n显示后10行类容**

**\[root\@chengfeng \~\]# tail-n 3 /etc/passwd\(显示前三行\)**

**![](../../image/20190107234448629.png)**

**（4）查看文件类型**

 

```
[root@chengfeng ~]# file /etc/passwd  （查看文件类型）
```

**![](../../image/20190107234655848.png)**

** （5）查看命令所在的路径**

```
[root@chengfeng ~]# which ls
alias ls='ls --color=auto'
	/usr/bin/ls
[root@chengfeng ~]# which cd
/usr/bin/cd
```

**（6）|  :管道符  连接命令  前面的命令给后面命令当参数**

```
[root@chengfeng ~]# head -n 5 /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
[root@chengfeng ~]# head -n 5 /etc/passwd | tail -n 1（显示passwd第5行的类容）
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
```

** 显示前4个最大文件**

```
root@chengfeng ~]# ls -lhS /etc/ | head -n 5
总用量 1.4M
-rw-r--r--.  1 root root   655K 6月   7 2013 services
-rw-r--r--   1 root root    92K 1月   7 14:35 ld.so.cache
-rw-r--r--   1 root root    51K 5月  15 2013 mime.types
-rw-r--r--   1 root root    15K 10月 31 08:17 autofs.conf
```

** 显示最近修改的文件**

```
[root@chengfeng ~]# ls -lt /etc/ |head -n 11
总用量 1396
drwxr-xr-x   5 root lp        304 1月   7 19:01 cups
-rw-r--r--   1 root root       57 1月   7 19:01 resolv.conf
-rw-r--r--   1 root root     1992 1月   7 14:51 passwd
----------   1 root root     1138 1月   7 14:50 shadow
----------   1 root root      690 1月   7 14:50 gshadow
-rw-r--r--   1 root root      862 1月   7 14:50 group
-rw-r--r--.  1 root root      850 1月   7 14:49 group-
----------.  1 root root      682 1月   7 14:49 gshadow-
```

**（7）查找文件或目录**

**\# find 路径 查找方式**

 

**按文件名称查找**

```
[root@chengfeng ~]# find /etc/ -name "*.conf"
/etc/resolv.conf
/etc/pki/ca-trust/ca-legacy.conf
/etc/yum/pluginconf.d/fastestmirror.conf

```

**统计查找的文件个数**

```
[root@chengfeng ~]# find /etc/ -name "*.conf" |wc -l
352
```

**按文件大小查找**

 

**查找大于1M的文件**

```
[root@chengfeng ~]# find /etc/ -size +1M
/etc/udev/hwdb.bin
/etc/selinux/targeted/contexts/files/file_contexts.bin
/etc/selinux/targeted/policy/policy.31
/etc/selinux/targeted/active/policy.kern
/etc/selinux/targeted/active/policy.linked
```

** 按文件的修改时间查找**

 

**查找7前修改的文件**

```
[root@chengfeng ~]# find / -mtime +7
```

**查找7内修改的文件**

```
[root@chengfeng ~]# find / -mtime -7
```

** 按文件的类型查找**

```
[root@chengfeng ~]# find /dev/ -type b
/dev/dm-1
/dev/dm-0
/dev/sda2
/dev/sda1
/dev/sda
/dev/sr0
[root@chengfeng ~]# find /dev/ -type l
```

**复合条件查文件**

 

**\[root\@chengfeng \~\]# find / \-mtime +7 \-a \-size +100k（a：and并列）**

 

**Find /bj/ \-name “\*.txt”  \-exec rm \-rf \{\}\\;  删除**

**\# Find /bj/ \-name “\*.txt”  \-exec cp \{\} /root \\;复制**