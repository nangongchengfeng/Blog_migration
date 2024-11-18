---
author: 南宫乘风
categories:
- Docker
date: 2021-07-25 23:24:21
description: 什么是是的图形化管理工具，提供状态显示面板、应用模板快速部署、容器镜像网络数据卷的基本操作包括上传下载镜像，创建容器等操作、事件日志显示、容器控制台操作、集群和服务等集中管理和操作、登录用户管理和控制。。。。。。。
image: http://image.ownit.top/4kdongman/59.jpg
tags:
- docker
- docker-compose
title: Docker集群可视化管理平台（Portainer）
---

<!--more-->

## 什么是Portainer

`Portainer`是`Docker`的图形化管理工具，提供状态显示面板、应用模板快速部署、容器镜像网络数据卷的基本操作（包括上传下载镜像，创建容器等操作）、事件日志显示、容器控制台操作、Swarm集群和服务等集中管理和操作、登录用户管理和控制等功能。功能十分全面，基本能满足中小型单位对容器管理的全部需求。

## 汉化界面

![](http://image.ownit.top/csdn/20210725231911721.png)

 

## 安装Docker

如果已经安装了Docker环境直接跳过本步骤即可

```
#CentOS 6
rpm -iUvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
yum update -y
yum -y install docker-io
service docker start
chkconfig docker on

#CentOS 7、Debian、Ubuntu
curl -sSL https://get.docker.com/ | sh
systemctl start docker
systemctl enable docker.service
```

安装Portainer版本： portainer-ce:2.0.1

汉化地址：<https://github.com/eysp/public/releases>

此版本已经测试，暂无bug，可以正常汉化显示，推荐

## Portainer中文汉化

```bash
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:2.0.1
```

![](http://image.ownit.top/csdn/20210725232147729.png)

进入这个目录把汉化的文件全部解压覆盖到： `public` 目录下

![](http://image.ownit.top/csdn/20210725232244219.png)

 ![](http://image.ownit.top/csdn/20210725232323132.png)