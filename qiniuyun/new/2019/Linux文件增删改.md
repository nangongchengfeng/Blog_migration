---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-06 13:58:06
description: 目录文件增删改创建文件文件名称花括号展开批量创建文件删除文件文件名代表强制删除批量删除文件复制文件只能复制文件可以复制目录源文件目标文件复制文件目录强制覆盖移动文件源文件目标文件文件重名。。。。。。。
image: http://image.ownit.top/4kdongman/31.jpg
tags:
- linux
title: Linux文件增删改
---

<!--more-->

**Linux目录/文件增删改**

**创建文件**

**\(1\)**

**\# touch  \<文件名称>**

**![](http://image.ownit.top/csdn/2019010613380274.png)**

 

**\(2\)**

**花括号展开**

**touch /root/\{1,3,9\}.txt**

**![](http://image.ownit.top/csdn/20190106134002790.png)**

**touch /root/\{0..100\}.txt  批量创建文件**

**![](http://image.ownit.top/csdn/20190106134135947.png)**

**删除文件**

**rm \-f \[文件名\] **

**\-rf  代表强制删除**

**![](http://image.ownit.top/csdn/20190106134510587.png)**

**批量删除文件**

**rm \-f \*txt**

**![](http://image.ownit.top/csdn/20190106134738416.png)**

 

**复制文件**

**cp 只能复制文件**

**cp \-r  可以复制目录**

**\# cp \[option\] 源文件  目标文件**

```
[root@zhang ~]# mkdir /root/{linux,windown}
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# touch /root/linux/{1,2,3}.txt
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# cd linux/
[root@zhang linux]# ls
1.txt  2.txt  3.txt
[root@zhang linux]# cd /r
root/ run/  
[root@zhang linux]# cd /root/
[root@zhang ~]# cp /root/linux/1.txt /root/windown/
[root@zhang ~]# cd windown/
[root@zhang windown]# ls
1.txt
[root@zhang windown]# cd ..
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# cp /root/linux/2.txt /root/windown/2.jpg
[root@zhang ~]# cd windown/
[root@zhang windown]# ls
1.txt  2.jpg
```

** \-r   复制文件目录**

```
[root@zhang ~]# cp -r /root/linux/ windown/
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# cd windown/
[root@zhang windown]# ls
1.txt  2.jpg  linux
[root@zhang windown]# cd linux/
[root@zhang linux]# ls
1.txt  2.txt  3.txt
```

**\-fn 强制覆盖**

```
[root@zhang ~]# cp -fn /root/linux/1.txt /root/windown/
```

**移动文件**

**#mv 源文件 目标文件**

 

**文件重名**

**![](http://image.ownit.top/csdn/2019010613525846.png)**

 

 

**![](http://image.ownit.top/csdn/20190106135739271.png)**