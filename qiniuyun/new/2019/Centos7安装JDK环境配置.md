---
author: 南宫乘风
categories:
- 技术记录
date: 2019-05-14 21:52:01
description: 作为一名程序员，各种环境搭建都要会。下面介绍关于操作系统之位安装以及环境配置。下面开始学习吧查看并卸载自带的安装好的会自带用命令，会有下面的信息：最好还是先卸载掉在安装公司的先查看显示如下信息：卸载：。。。。。。。
image: http://image.ownit.top/4kdongman/02.jpg
tags:
- 技术记录
title: Centos7安装JDK环境配置
---

<!--more-->

作为一名程序员，各种环境搭建都要会。

下面介绍关于Linux操作系统之centos7（64位）安装JDK以及环境配置。

下面开始学习吧

# 查看并卸载CentOS自带的OpenJDK

 -    ##  安装好的CentOS会自带OpenJdk,用命令 java -version ，会有下面的信息：

```
    java version "1.6.0"
   OpenJDK Runtime Environment (build 1.6.0-b09)
   OpenJDK 64-Bit Server VM (build 1.6.0-b09, mixed mode)
```

最好还是先卸载掉openjdk,在安装sun公司的jdk.

- ## 先查看 rpm -qa | grep java

显示如下信息：

```
    java-1.4.2-gcj-compat-1.4.2.0-40jpp.115
    java-1.6.0-openjdk-1.6.0.0-1.7.b09.el5
```

卸载：

```
    rpm -e --nodeps java-1.4.2-gcj-compat-1.4.2.0-40jpp.115
    rpm -e --nodeps java-1.6.0-openjdk-1.6.0.0-1.7.b09.el5
```

**STEP 1：**

现在JDK12都出来了，所以我们也要紧跟着技术的潮流走。

所有下载的jdk-12.0.1\_linux-x64\_bin.rpm

官网链接：[JDK官网下载](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)

![](http://image.ownit.top/csdn/20190514213931610.png)

 

选择与自己系统相匹配的版本，我的是Centos7 64位的，所以如果是我的是jdk-12.0.1\_linux-x64\_bin.rpm

 

**STEP 2：**

利用Xshell工具进行Linux命令处理，进行安装。

![](http://image.ownit.top/csdn/20190514214220477.png)

进行rpm安装jdk

```
[root@wei ~]# rpm -ivh jdk-12.0.1_linux-x64_bin.rpm 
```

![](http://image.ownit.top/csdn/20190514214307395.png)

下面以及安装成功过jdk。

注意：安装成功，但是环境变量没有配置，需要配置环境变量。

（1）找到jdk安装路径

```
[root@wei ~]# cd /usr/java/jdk-12.0.1/
[root@wei jdk-12.0.1]# ls
bin  conf  include  jmods  legal  lib  man  release
[root@wei jdk-12.0.1]# pwd
/usr/java/jdk-12.0.1
```

![](http://image.ownit.top/csdn/2019051421453052.png)

（2）复制路径，开始配置环境变量（/usr/java/jdk-12.0.1）

编辑：/etc/profile文件，在最后面加入下面的代码

```
export JAVA_HOME=/usr/java/jdk-12.0.1
export PATH=$PATH:JAVA_HOME/bin
```

```
[root@wei jdk-12.0.1]# source /etc/profile
```

（3）保存，重新加载配置文件

 

![](http://image.ownit.top/csdn/20190514214834746.png)

（4）查看jdk的配置信息，看是否配置完成

```
[root@wei jdk-12.0.1]# java -version
```

![](http://image.ownit.top/csdn/20190514214924827.png)

 

### **ok，jdk已经成功安装成功。恭喜你有学会一个新的技能。**

### **加油。**