---
author: 南宫乘风
categories:
- Docker
date: 2020-01-03 14:49:12
description: 作用：都是指定一个容器启动时要运行的命令中可以有多个指令，但只有最后一个生效，会被之后的参数替换实例的讲解演示之后的参数会被当做参数传递给，之后形成新的命令组合实例制作版可以查询信息的容器命令解释命令。。。。。。。
image: http://image.ownit.top/4kdongman/62.jpg
tags:
- docker
- dockerfile
- CDM
title: DockerFile的CMD/ENTRYPOINT 镜像案例
---

<!--more-->

 

## 作用：都是指定一个容器启动时要运行的命令

### CMD

Dockerfile 中可以有多个 CMD 指令，但只有最后一个生效，CMD 会被 docker run 之后的参数替换

实例

tomcat的讲解演示

```
docker run -it -p 8080:8080 tomcat
```

### ![](http://image.ownit.top/csdn/20200103143318730.png)

```
docker run -it -p 8080:8080 tomcat ls -l
```

### ![](http://image.ownit.top/csdn/20200103143227449.png)

### **ENTRYPOINT **

docker run 之后的参数会被当做参数传递给 ENTRYPOINT，之后形成新的命令组合

实例

![](http://image.ownit.top/csdn/20200103142026490.png)

制作CMD版可以查询IP信息的容器

```bash
FROM centos
RUN yum install -y curl
CMD [ "curl", "-s", "http://ip.cn" ]
```

![](http://image.ownit.top/csdn/20200103142104726.png)

**crul命令解释**

curl命令可以用来执行下载、发送各种HTTP请求，指定HTTP头部等操作。

如果系统没有curl可以使用yum install curl安装，也可以下载安装。

curl是将下载文件输出到stdout

使用命令：curl http://www.baidu.com  
执行后，www.baidu.com的html就会显示在屏幕上了

这是最简单的使用方法。用这个命令获得了http://curl.haxx.se指向的页面，同样，如果这里的URL指向的是一个文件或者一幅图都可以直接下载到本地。如果下载的是HTML文档，那么缺省的将只显示文件头部，即HTML文档的header。要全部显示，请加参数 \-i

### **问题**

如果我们希望显示 HTTP 头信息，就需要加上 \-i 参数

![](https://image.ownit.top/csdn/20200103142220735.png)

**WHY**

我们可以看到可执行文件找不到的报错，executable file not found。

之前我们说过，跟在镜像名后面的是 command，运行时会替换 CMD 的默认值。

因此这里的 \-i 替换了原来的 CMD，而不是添加在原来的 curl \-s http://ip.cn 后面。而 \-i 根本不是命令，所以自然找不到。

那么如果我们希望加入 \-i 这参数，我们就必须重新完整的输入这个命令：

```
$ docker run myip curl -s http://ip.cn -i
```

制作ENTROYPOINT版查询IP信息的容器

```bash
FROM centos
RUN yum install -y curl
ENTRYPOINT [ "curl", "-s", "http://ip.cn" ]
```

![](http://image.ownit.top/csdn/20200103142315187.png)