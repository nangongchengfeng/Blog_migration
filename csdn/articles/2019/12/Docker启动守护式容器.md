+++
author = "南宫乘风"
title = "Docker启动守护式容器"
date = "2019-12-10 15:01:46"
tags=['docker\xa0', '容器', '守护']
categories=['Docker']
image = "post/4kdongman/54.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103474709](https://blog.csdn.net/heian_99/article/details/103474709)

**目录**

[启动守护式容器](#%E5%90%AF%E5%8A%A8%E5%AE%88%E6%8A%A4%E5%BC%8F%E5%AE%B9%E5%99%A8)

[查看容器日志](#%E6%9F%A5%E7%9C%8B%E5%AE%B9%E5%99%A8%E6%97%A5%E5%BF%97)

[docker后台运行](#docker%E5%90%8E%E5%8F%B0%E8%BF%90%E8%A1%8C)

[查看容器内运行的进程](#%E6%9F%A5%E7%9C%8B%E5%AE%B9%E5%99%A8%E5%86%85%E8%BF%90%E8%A1%8C%E7%9A%84%E8%BF%9B%E7%A8%8B)

[​查看容器内部细节](#%E2%80%8B%E6%9F%A5%E7%9C%8B%E5%AE%B9%E5%99%A8%E5%86%85%E9%83%A8%E7%BB%86%E8%8A%82)

[进入正在运行的容器并以命令行交互](#%E8%BF%9B%E5%85%A5%E6%AD%A3%E5%9C%A8%E8%BF%90%E8%A1%8C%E7%9A%84%E5%AE%B9%E5%99%A8%E5%B9%B6%E4%BB%A5%E5%91%BD%E4%BB%A4%E8%A1%8C%E4%BA%A4%E4%BA%92)

[重新进入](#%E9%87%8D%E6%96%B0%E8%BF%9B%E5%85%A5)

[上述两个区别](#%E4%B8%8A%E8%BF%B0%E4%B8%A4%E4%B8%AA%E5%8C%BA%E5%88%AB)

[从容器内拷贝文件到主机上](#%E4%BB%8E%E5%AE%B9%E5%99%A8%E5%86%85%E6%8B%B7%E8%B4%9D%E6%96%87%E4%BB%B6%E5%88%B0%E4%B8%BB%E6%9C%BA%E4%B8%8A)

## **启动守护式容器**

```
docker run -d 容器名
```

#使用镜像centos:latest以后台模式启动一个容器

```
docker run -d centos
```

 问题：然后docker ps -a 进行查看, 会发现容器已经退出

![20191210143129964.png](https://img-blog.csdnimg.cn/20191210143129964.png)

很重要的要说明的一点: Docker容器后台运行,就必须有一个前台进程.

容器运行的命令如果不是那些一直挂起的命令（比如运行top，tail），就是会自动退出的。

 这个是docker的机制问题,比如你的web容器,我们以nginx为例，正常情况下,我们配置启动服务只需要启动响应的service即可。例如

```
service nginx start
```

但是,这样做,nginx为后台进程模式运行,就导致docker前台没有运行的应用,

这样的容器后台启动后,会立即自杀因为他觉得他没事可做了.

所以，最佳的解决方案是,将你要运行的程序以前台进程的形式运行

## **查看容器日志**

```
docker logs -f -t --tail 容器ID
```
- *   -t 是加入时间戳- *   -f 跟随最新的日志打印- *   --tail 数字 显示最后多少条
![20191210143340560.png](https://img-blog.csdnimg.cn/20191210143340560.png)

## docker后台运行

```
 docker run -d centos /bin/sh -c "while true;do echo hello zzyy;sleep 2;done"
```

## ![20191210144121681.png](https://img-blog.csdnimg.cn/20191210144121681.png)

## **查看容器内运行的进程**

```
docker top 容器ID
```

## ![2019121014422663.png](https://img-blog.csdnimg.cn/2019121014422663.png)**查看容器内部细节**

```
docker inspect 容器ID
```

## ![20191210144339876.png](https://img-blog.csdnimg.cn/20191210144339876.png)

## **进入正在运行的容器并以命令行交互**

```
docker exec -it 容器ID bashShell
```

## ![20191210145040348.png](https://img-blog.csdnimg.cn/20191210145040348.png)

## 重新进入

```
docker attach 容器ID
```

## ![20191210145325824.png](https://img-blog.csdnimg.cn/20191210145325824.png)

## 上述两个区别
- attach： 直接进入容器启动命令的终端，不会启动新的进程- exec： 是在容器中打开新的终端，并且可以启动新的进程
## **从容器内拷贝文件到主机上**

```
docker cp  容器ID:容器内路径 目的主机路径
```

![20191210150015467.png](https://img-blog.csdnimg.cn/20191210150015467.png)

 
