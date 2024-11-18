---
author: 南宫乘风
categories:
- Docker
date: 2020-03-31 15:34:57
description: 安装配置二进制安装、下载最新版的二进制执行文件。、配置可执行权限。、测试是否安装成功。使用启动，一键配置和启动容器对于容器开机启动，本地数据持续化，保留数据安装运行：但是这样运行的话，可能会运行，但是。。。。。。。
image: ../../title_pic/60.jpg
slug: '202003311534'
tags:
- 企业级-Shell脚本案例
- docker
- linux
- gitlab
- centos
- 运维
title: Docker一键部署GitLab+Jenkins【本地持久化】
---

<!--more-->

### docker-compose安装配置

**二进制安装**

1、下载最新版的 docker-compose 二进制执行文件。

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

2、配置可执行权限。

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

3、测试是否安装成功。

```bash
docker-compose --version 
```

![](../../image/20200331153131369.png)

**使用docker-compose启动yml，一键配置和启动容器**

**对于容器开机启动，本地数据持续化，保留数据**

**安装docker-compose**

**运行：**

```bash
docker-compose up -d
```

**但是这样运行的话，可能jenkins会运行，但是会报错，因为jenkins\_home的权限不够，导致无法写入数据。**

**编写一个shell脚本，和这个docker-compose.yml放在一个目录下**

**直接运行这个脚本，就可以实现gitlab和jenkins的完美运行。**

**两个 开始消耗的内存和cpu过大，需要等待一会就可以了。**

**git.sh**

```bash
#!/bin/bash
mkdir -p /usr/local/docker/jenkins/jenkins_home
chown -R 1000:1000 /usr/local/docker/jenkins/jenkins_home
docker-compose up -d
```

**docker-compose.yml**

```bash
version: '3'
services:
    gitlab:
      image: twang2218/gitlab-ce-zh:9.4
      restart: always
      hostname: 192.168.1.100
      environment:
        TZ: 'Asia/Shanghai'
        GITLAB_OMNIBUS_CONFIG: |
          external_url 'http://192.168.1.100:8080'
          gitlab_rails['gitlab_shell_ssh_port'] = 2222
          unicorn['port'] = 8888
          nginx['listen_port'] = 8080
      ports:
        - '8080:8080'
        - '8443:443'
        - '2222:22'
      volumes:
        - /usr/local/docker/gitlab/config:/etc/gitlab
        - /usr/local/docker/gitlab/repo:/var/opt/gitlab
        - /usr/local/docker/gitlab/logs:/var/log/gitlab

    jenkins:
      restart: always
      image: jenkins/jenkins
      container_name: docker_jenkins
      ports:
        - '8081:8080'
        - '50000:50000'
      volumes:
        - /usr/local/docker/jenkins/jenkins_home:/var/jenkins_home
      environment:
            JAVA_OPTS: '-Djava.util.logging.config.file=/var/jenkins_home/log.properties'
```

![](../../image/20200331153328896.png)

 

![](../../image/20200331153406300.png)

![](../../image/20200331153421909.png)