---
author: 南宫乘风
categories:
- 技术记录
date: 2019-05-14 22:31:52
description: 第一步：下载压缩包进入下载压缩包第二步：用工具把压缩包上传到下第三步：解压以及新建目录我们新建目录把剪切进去第四步：配置可以配置端口，编码以及配置项目等等，我们这里就配置一个端口，把默认的第五步：配置。。。。。。。
image: ../../title_pic/34.jpg
slug: '201905142231'
tags:
- 技术记录
title: Centos7安装和配置Tomcat8
---

<!--more-->

**第一步：下载Tomcat8压缩包**

进入 <http://tomcat.apache.org/download-80.cgi>

![](../../image/812323-20170703223844956-1669877808.png)

下载tar.gz压缩包

 

**第二步：用xshell工具把压缩包上传到/home/data/下**

![](../../image/20190514220711262.png)

**第三步：解压以及新建目录**

```
[root@wei data]# tar -zxvf apache-tomcat-8.5.40.tar.gz 
```

![](../../image/20190514220856119.png)

我们新建/home/tomcat/目录 把tomcat剪切进去

![](../../image/20190514221042961.png)

 

**第四步：配置tomcat server.xml**

server.xml可以配置端口，编码以及配置项目等等，我们这里就配置一个端口，把默认的8080

vi /home/tomcat/apache-tomcat-8.5.16/conf/server.xml

![](../../image/20190514223020657.png)

**第五步：配置防火墙，开放8080端口**

firewall-cmd \--zone=public \--add-port=8080/tcp \--permanent

firewall-cmd \--reload

**第六步：启动tomcat**

```
[root@wei home]# /home/tomcat/apache-tomcat-8.5.40/bin/startup.sh 
```

![](../../image/20190514221310361.png)

下面是tomcat启动的界面（端口8080）

![](../../image/20190514222917412.png)

下面是httpd启动的界面（端口80）

 

![](../../image/20190514221502916.png)