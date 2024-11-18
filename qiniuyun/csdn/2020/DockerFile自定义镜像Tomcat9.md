---
author: 南宫乘风
categories:
- Docker
date: 2020-01-03 16:33:10
description: 目录下载容器卷、创建文件夹、在上述目录下、在上述目录下、将和安装的压缩包拷贝进上一步目录、在目录下新建文件、构建、、验证、结合前述的容器卷将测试的服务发布总结下载容器卷、创建文件夹、在上述目录下、将和。。。。。。。
image: ../../title_pic/27.jpg
slug: '202001031633'
tags:
- docker
- dockerfile
- 镜像
title: DockerFile自定义镜像Tomcat9
---

<!--more-->

**目录**

 

[下载tomcat容器卷](#%E4%B8%8B%E8%BD%BDtomcat%E5%AE%B9%E5%99%A8%E5%8D%B7)

[1、创建文件夹](#1%E3%80%81%E5%88%9B%E5%BB%BA%E6%96%87%E4%BB%B6%E5%A4%B9)

[2、在上述目录下touch c.txt](<#2、在上述目录下touch c.txt>)

[3、将jdk和tomcat安装的压缩包拷贝进上一步目录](#3%E3%80%81%E5%B0%86jdk%E5%92%8Ctomcat%E5%AE%89%E8%A3%85%E7%9A%84%E5%8E%8B%E7%BC%A9%E5%8C%85%E6%8B%B7%E8%B4%9D%E8%BF%9B%E4%B8%8A%E4%B8%80%E6%AD%A5%E7%9B%AE%E5%BD%95)

[4、在/heian/mydockerfile/tomcat9目录下新建Dockerfile文件](#4%E3%80%81%E5%9C%A8%2Fheian%2Fmydockerfile%2Ftomcat9%E7%9B%AE%E5%BD%95%E4%B8%8B%E6%96%B0%E5%BB%BADockerfile%E6%96%87%E4%BB%B6)

[5、构建](#5%E3%80%81%E6%9E%84%E5%BB%BA)

[6、run](#6%E3%80%81run)

[7、验证](#7%E3%80%81%E9%AA%8C%E8%AF%81)

[8、结合前述的容器卷将测试的web服务test发布](#8%E3%80%81%E7%BB%93%E5%90%88%E5%89%8D%E8%BF%B0%E7%9A%84%E5%AE%B9%E5%99%A8%E5%8D%B7%E5%B0%86%E6%B5%8B%E8%AF%95%E7%9A%84web%E6%9C%8D%E5%8A%A1test%E5%8F%91%E5%B8%83)

[总结](#%E6%80%BB%E7%BB%93)

---

### [下载tomcat](https://github.com/docker-library/tomcat/blob/46fb91d392f48c4e606cb6f845c4be37d6bacffc/9.0/jdk8/corretto/Dockerfile)容器卷

### 1、创建文件夹

```
mkdir -p /heian/mydockerfile/tomcat9
```

### 2、在上述目录下touch c.txt

```
touch c.txt
```

### 3、将jdk和tomcat安装的压缩包拷贝进上一步目录

apache-tomcat-9.0.8.tar.gz

jdk-8u171-linux-x64.tar.gz

![](../../image/20200103150556666.png)

### 4、在/heian/mydockerfile/tomcat9目录下新建Dockerfile文件

 

```bash
FROM         centos
MAINTAINER    heian<1794748404@126.com>
#把宿主机当前上下文的c.txt拷贝到容器/usr/local/路径下
COPY c.txt /usr/local/cincontainer.txt
#把java与tomcat添加到容器中
ADD jdk-8u152-linux-x64.tar.gz /usr/local/
ADD apache-tomcat-8.5.24.tar.gz /usr/local/
#安装vim编辑器
RUN yum -y install vim
#设置工作访问时候的WORKDIR路径，登录落脚点
ENV MYPATH /usr/local
WORKDIR $MYPATH
#配置java与tomcat环境变量
ENV JAVA_HOME /usr/local/jdk1.8.0_152
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /usr/local/apache-tomcat-8.5.24
ENV CATALINA_BASE /usr/local/apache-tomcat-8.5.24
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin
#容器运行时监听的端口
EXPOSE  8080
#启动时运行tomcat
# ENTRYPOINT ["/usr/local/apache-tomcat-8.5.24/bin/startup.sh" ]
# CMD ["/usr/local/apache-tomcat-8.5.24/bin/catalina.sh","run"]
CMD /usr/local/apache-tomcat-8.5.24/bin/startup.sh && tail -F /usr/local/apache-tomcat-8.5.24/bin/logs/catalina.out
```

![](../../image/20200103151312441.png)

### 5、构建

```
docker build -f Dockerfile -t heiantomcat9 .
```

![](../../image/20200103160233624.png)

**构建完成**

![](../../image/20200103160320912.png)

### 6、run

```
docker run -d -p 9080:8080 --name myt9 -v /heian/mydockerfile/tomcat9/test:/usr/local/apache-tomcat-9.0.8/webapps/test -v /heian/mydockerfile/tomcat9/tomcat9logs/:/usr/local/apache-tomcat-9.0.8/logs --privileged=true heiantomcat9
```

![](../../image/20200103160625359.png)

Docker挂载主机目录Docker访问出现cannot open directory .: Permission denied  
解决办法：在挂载目录后多加一个--privileged=true参数即可

### 7、验证

![](../../image/20200103160704631.png)

### 8、结合前述的容器卷将测试的web服务test发布

![](../../image/20200103161202296.png)

![](../../image/20200103161645120.png)

**a.jsp**

```html
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Insert title here</title>
  </head>
  <body>
    -----------welcome------------
    <%="i am in docker tomcat self "%>
    <br>
    <br>
    <% System.out.println("=============docker tomcat self");%>
  </body>
</html>
```

**web.xml**

```html
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns="http://java.sun.com/xml/ns/javaee"
  xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
  id="WebApp_ID" version="2.5">
  
  <display-name>test</display-name>
 
</web-app>
```

**测试**

![](../../image/20200103162009410.png)

![](../../image/20200103163112368.png)

![](../../image/20200103163123955.png)

![](../../image/20200103163134733.png)

### **总结**

![](../../image/20200103163155505.png)