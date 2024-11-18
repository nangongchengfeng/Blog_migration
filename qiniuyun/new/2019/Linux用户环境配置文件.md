---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-25 21:36:47
description: 用户操作环境配置文件：从目录复制过来打开新终端用户登录系统注销系统示例：设置命令别名临时命令别名关机重启，就没有了命令别名命令永久别名可以一直存在针对单个用户设置别名创建用户，修改进入，在最后一行添加。。。。。。。
image: http://image.ownit.top/4kdongman/06.jpg
tags:
- linux
title: Linux用户环境配置文件
---

<!--more-->

  
**用户操作环境配置文件：**

**从/etc/skel目录复制过来**

**![](http://image.ownit.top/csdn/20190125210956175.png)**

**.bashrc             打开新终端           /etc/bashrc  
.bash\_profile       用户登录系统         /ect/profile  
.bash\_logout        注销系统             **

  
**示例：设置命令别名**

## **临时命令别名（关机重启，就没有了）**

**\# alias 命令别名=‘命令’**

```
alias ipshow='cat /etc/sysconfig/network-scripts/ifcfg-ens33'
```

![](http://image.ownit.top/csdn/20190125211616558.png)

##   
**永久别名（可以一直存在）**

**针对单个用户设置别名**

（1）创建hei用户，修改vim /home/hei/.bashrc 

![](http://image.ownit.top/csdn/20190125212504317.png)

（2）进入  /home/hei/.bashrc ，在最后一行添加  ** alias ipshow=' cat /etc/sysconfig/network-scripts/ifcfg-ens33' 保存退出**

![](http://image.ownit.top/csdn/20190125212435357.png)

（3）切换到hei用户下查看

![](http://image.ownit.top/csdn/2019012521312935.png)

  
**针对所有用户设置别名**

**这个方法和上面的一样，只需要修改的文件不一样。下面已经列出**

**（1）修改/etc/bashrcde文件**

**（2）添加命令别名代码**

**（3）刷新文件即可**  
 

```
root@wei ~]# vim /etc/bashrc
 
   alias ipshow=' cat /etc/sysconfig/network-scripts/ifcfg-ens33'
[root@wei ~]# source /etc/bashrc
```