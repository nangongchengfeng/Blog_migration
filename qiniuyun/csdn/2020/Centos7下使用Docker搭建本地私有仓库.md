---
author: 南宫乘风
categories:
- Docker
date: 2020-01-11 16:17:03
description: 和的管理一样，不仅提供了一个中央仓库，同时也允许我们使用搭建本地私有仓库。使用私有仓库有许多优点：一、节省网络带宽，针对于每个镜像不用每个人都去中央仓库上面去下载，只需要从私有仓库中下载即可；二、提供。。。。。。。
image: ../../title_pic/59.jpg
slug: '202001111617'
tags:
- Centos
- Docker
- 本地仓库
- 私有仓库
title: Centos7下使用Docker搭建本地私有仓库
---

<!--more-->

和Mavan的管理一样，Dockers不仅提供了一个中央仓库，同时也允许我们使用registry搭建本地私有仓库。使用私有仓库有许多优点：

一、节省网络带宽，针对于每个镜像不用每个人都去中央仓库上面去下载，只需要从私有仓库中下载即可；

二、提供镜像资源利用，针对于公司内部使用的镜像，推送到本地的私有仓库中，以供公司内部相关人员使用。

接下来我们就大致说一下如何在本地搭建私有仓库。

### 1.拉取镜像仓库

```
docker  pull  registry 
```

### 2.查看所有镜像

```
 docker images
```

![](../../image/20200111160352917.png)

### 3.启动镜像服务器registry

首先在在主机上新建一个目录，供存储镜像

```
cd /usr/local/
mkdir docker_registry 
```

**启动镜像**

```
docker run -d -p 5000:5000 --name=jackspeedregistry --restart=always --privileged=true  -v /usr/local/docker_registry:/var/lib/registry  docker.io/registry
```

解释：  
  \-p 5000:5000 端口  
  \--name=jackspeedregistry 运行的容器名称  
  \--restart=always 自动重启  
   \--privileged=true centos7中的安全模块selinux把权限禁止了，加上这行是给容器增加执行权限  
  \-v /usr/local/docker\_registry:/var/lib/registry 把主机的/usr/local/docker\_registry 目录挂载到registry容器的/var/lib/registry目录下，假如有删除容器操作，我们的镜像也不会被删除  
  docker.io/registry  镜像名称  
查看启动的容器

![](../../image/20200111160523133.png)

### 4.从公有仓库拉取一个镜像下来，然后push到私有仓库中进行测试

### 当前用nginx镜像做测试

```
docker pull  nginx 
docker images
```

![](../../image/20200111160758579.png)

### 5.给docker注册https协议，支持https访问

```
vim /etc/docker/daemon.json
```

如果daemon文件不存在，vim会自己创建一个，假如一下代码，  
  \{<!-- -->  
  "insecure-registries":\["主机的IP地址或者域名:5000"\],  
   "registry-mirrors": \["[https://registry.docker-cn.com](https://registry.docker-cn.com/)"\]  
  \}  
注释：  
  insecure-registries----->开放注册https协议  
  registry-mirrors----->仓库源

![](../../image/20200111160928574.png)

### 6.新建一个tag，把docker.io/nginx名称变成域名或者IP/镜像名称

```
docker tag docker.io/nginx ip或者域名:5000/nginx
```

**推送到本地仓库**

```
docker push ip或者域名:5000/nginx
```

![](../../image/20200111161202963.png)

### 7.进入刚才新建的nginx仓库目录得到

![](../../image/20200111161246783.png)

### 删除刚刚tag的镜像 （192.\*\*\*\*\*\*\*:5000/nginx刚才创建的镜像的tag）

```
docker rmi 196.*******:5000/nginx
docker rmi  nginx 
docker images
```

![](../../image/2020011116145613.png)

拉取刚刚自己创建的镜像

```
docker pull 192.168.116.131:5000/nginx:1.2
```

![](../../image/20200111161607528.png)

**已经完成**