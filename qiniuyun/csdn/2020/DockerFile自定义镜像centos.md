---
author: 南宫乘风
categories:
- MySQL
date: 2020-01-03 14:13:50
description: 镜像中的镜像都是通过在镜像中安装和配置需要的软件构建出来的自定义镜像、编写自定义目的使我们自己的镜像具备如下：登陆后的默认路径编辑器查看网络配置支持准备编写文件内容基于本地的作者、邮件来设置环境变量登。。。。。。。
image: ../../title_pic/50.jpg
slug: '202001031413'
tags:
- docker
- centos
- images
title: DockerFile自定义镜像centos
---

<!--more-->

# Base镜像\(scratch\)

Docker Hub 中 99\% 的镜像都是通过在 base 镜像中安装和配置需要的软件构建出来的

![](../../image/20200103121024908.png)

# 自定义镜像mycentos

### 1、编写

![](../../image/20200103121118879.png)

**自定义mycentos目的使我们自己的镜像具备如下：**

1.           登陆后的默认路径
2.           vim编辑器
3.           查看网络配置ifconfig支持

**准备编写DockerFile文件**

![](../../image/20200103134141368.png)

**myCentOS内容DockerFile**

```bash
 #基于本地的centos
FROM centos   
 #作者、邮件
MAINTAINER cf<1794748404@qq.com>
 #来设置环境变量
ENV MYPATH /uer/local 
#登录进去的路径
WORKDIR $MYPATH
##安装下面的软件
RUN yum -y install vim
RUN yum -y install net-tools
#暴露80端口
EXPOSE 80
#打印信息
CMD echo $MYPATH
CMD echo "success-----------------ok"
#使用bash
CMD /bin/bash
```

### 2、构建

```bash
docker build -f /root/docker/dockerfile1 -t mycentos:1.3 .

```

![](../../image/20200103135523341.png)

![](../../image/20200103140335411.png)

### 3、运行

```bash
docker run -it 新镜像名字:TAG 
```

可以看到，我们自己的新镜像已经支持vim/ifconfig命令，扩展成功了

![](../../image/20200103140700790.png)

### 4、列出镜像的变更历史

docker history 镜像名

![](../../image/20200103140409352.png)