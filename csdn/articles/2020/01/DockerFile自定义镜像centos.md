+++
author = "南宫乘风"
title = "DockerFile自定义镜像centos"
date = "2020-01-03 14:13:50"
tags=['docker', 'centos', 'images']
categories=['MySQL']
image = "post/4kdongman/92.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103818231](https://blog.csdn.net/heian_99/article/details/103818231)

# Base镜像(scratch)

Docker Hub 中 99% 的镜像都是通过在 base 镜像中安装和配置需要的软件构建出来的

![20200103121024908.png](https://img-blog.csdnimg.cn/20200103121024908.png)

# 自定义镜像mycentos

### 1、编写

![20200103121118879.png](https://img-blog.csdnimg.cn/20200103121118879.png)

**自定义mycentos目的使我们自己的镜像具备如下：**
1.          登陆后的默认路径1.          vim编辑器1.          查看网络配置ifconfig支持
**准备编写DockerFile文件**

![20200103134141368.png](https://img-blog.csdnimg.cn/20200103134141368.png)

**myCentOS内容DockerFile**

```
 #基于本地的centos
FROM centos   
 #作者、邮件
MAINTAINER cf&lt;1794748404@qq.com&gt;
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

```
docker build -f /root/docker/dockerfile1 -t mycentos:1.3 .


```

![20200103135523341.png](https://img-blog.csdnimg.cn/20200103135523341.png)

![20200103140335411.png](https://img-blog.csdnimg.cn/20200103140335411.png)

### 3、运行

```
docker run -it 新镜像名字:TAG 
```

可以看到，我们自己的新镜像已经支持vim/ifconfig命令，扩展成功了

![20200103140700790.png](https://img-blog.csdnimg.cn/20200103140700790.png)

### 4、列出镜像的变更历史

docker history 镜像名

![20200103140409352.png](https://img-blog.csdnimg.cn/20200103140409352.png)
