---
author: 南宫乘风
categories:
- Jenkins
date: 2022-05-16 21:47:34
description: 介绍是一个独立的开源软件项目，是基于开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。前身是是一个可扩展的持续集成引擎。可用于自动化各种任务，如。。。。。。。
image: ../../title_pic/54.jpg
slug: '202205162147'
tags:
- jenkins
- 运维
- ci
title: Jenkins安装部署使用
---

<!--more-->

## 介绍

Jenkins是一个独立的开源软件项目，是基于Java开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。前身是Hudson是一个可扩展的持续集成引擎。可用于自动化各种任务，如构建，测试和部署软件。Jenkins可以通过本机系统包Docker安装，甚至可以通过安装Java Runtime Environment的任何机器独立运行。

## **Jenkins特点**

- 开源免费;
- 跨平台，支持所有的平台;
- master/slave支持分布式的build;
- web形式的可视化的管理页面;
- 安装配置超级简单;
- tips及时快速的帮助；
- 已有的200多个插件

![](../../image/86052dfea3b0439bbca0450729bbbb67.png)

 

## 安装教程

这里我们使用的是离线包方式安装。

官网镜像地址: [Index of /](https://mirrors.jenkins.io/ "Index of /")  
下载地址： [Jenkins download and deployment](https://jenkins.io/download/ "Jenkins download and deployment")  
华为镜像地址: [华为开源镜像站\_软件开发服务\_华为云](https://mirrors.huaweicloud.com/home "华为开源镜像站_软件开发服务_华为云")

直接下载war包，并安装好jdk之后，输入:nohup java \-jar jenkins.war \--httpPort=8888 \&  
进行启动，然后网页浏览器输入 ip:8888打开设置好账号密码之后登录即可，插件安装推荐使用官方推荐。

![](../../image/07ec709025734dc3abde51e5eea918e7.png)

 

##  Docker安装

拉取Jenkins镜像

```bash
docker pull jenkins/jenkins
```

编写docker-compose.yml

```bash
version: "3.1"
services:
  jenkins:
    image: jenkins/jenkins
    container_name: jenkins
    ports:
      - 8080:8080
      - 50000:50000
    volumes:
      - ./data/:/var/jenkins_home/
      - /usr/bin/docker:/usr/bin/docker
      - /var/run/docker.sock:/var/run/docker.sock
      - /etc/docker/daemon.json:/etc/docker/daemon.json
```

![](../../image/62f58ce9ce6d41a58af241b832b40ee0.png)

 

首次启动会因为数据卷data目录没有权限导致启动失败，设置data目录写权限

![](../../image/661580a6b2534c2888bfb7a2e03155e3.png)

```bash
chmod -R a+w data/ 
```

重新启动Jenkins容器后，由于Jenkins需要下载大量内容，但是由于默认下载地址下载速度较慢，需要重新设置下载地址为国内镜像站

```bash
# 修改数据卷中的hudson.model.UpdateCenter.xml文件
<?xml version='1.1' encoding='UTF-8'?>
<sites>
  <site>
    <id>default</id>
    <url>https://updates.jenkins.io/update-center.json</url>
  </site>
</sites>
# 将下载地址替换为http://mirror.esuni.jp/jenkins/updates/update-center.json
<?xml version='1.1' encoding='UTF-8'?>
<sites>
  <site>
    <id>default</id>
    <url>http://mirror.esuni.jp/jenkins/updates/update-center.json</url>
  </site>
</sites>
# 清华大学的插件源也可以https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json
```

再次重启Jenkins容器，访问Jenkins（需要稍微等会）

```bash
docker-compose restart
```

![](../../image/7ce8b117fb53454e8058546550c9fe0e.png)

 查看密码登录Jenkins，并登录下载插件

```bash
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

![](../../image/fa7589e1e1394ff8b6d2714363813f7c.png)

![](../../image/5abb45aa916a4a128883e68eed03fab5.png) 

 ![](../../image/4b4be6f3cd8641c291b3c1a3eb6cfbee.png)

 

![](../../image/3a2abc00ac6d4289b96654fcea395fed.png)

 

![](../../image/4ae63c3c631d42e5a67b96c810a22ace.png)

![](../../image/86d90cfe377942d3ade053fd48f021fd.png) 

 ![](../../image/935c92d6ed8249e9acef95793cc67cdf.png)

 

![](../../image/59d332cba48f4a648a538bc891b6e6f4.png)