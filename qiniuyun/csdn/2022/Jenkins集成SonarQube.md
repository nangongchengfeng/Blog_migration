---
author: 南宫乘风
categories:
- Jenkins
date: 2022-05-17 10:06:54
description: 前文目录安装部署使用南宫乘风的博客博客安装部署使用南宫乘风的博客博客入门配置南宫乘风的博客博客入门配置南宫乘风的博客博客介绍是一个开源的代码分析平台，支持、、、、等种以上的语言，可以检测出重复代码、代。。。。。。。
image: ../../title_pic/41.jpg
slug: '202205171006'
tags:
- jenkins
- 运维
title: Jenkins集成Sonar Qube
---

<!--more-->

# 前文目录

[Jenkins安装部署使用\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858 "Jenkins安装部署使用_南宫乘风的博客-CSDN博客")

[Jenkins入门配置\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124809338 "Jenkins入门配置_南宫乘风的博客-CSDN博客")

# Sonar Qube介绍

Sonar Qube是一个开源的代码分析平台，支持Java、Python、PHP、JavaScript、CSS等25种以上的语言，可以检测出重复代码、代码漏洞、代码规范和安全性漏洞的问题。

Sonar Qube可以与多种软件整合进行代码扫描，比如Maven，Gradle，Git，Jenkins等，并且会将代码检测结果推送回Sonar Qube并且在系统提供的UI界面上显示出来

![](../../image/8ca6ab5caeac4a33819290d82400e416.png)

 

# Sonar Qube环境搭建

Sonar Qube安装

Sonar Qube在7.9版本中已经放弃了对MySQL的支持，并且建议在商业环境中采用PostgreSQL，那么安装Sonar Qube时需要依赖PostgreSQL。

并且这里会安装Sonar Qube的长期支持版本[8.9]()

  - 拉取镜像

```bash
docker pull postgres
docker pull sonarqube:8.9.3-community
```

编写docker-compose.yml

```bash
version: "3.1"
services:
  db:
    image: postgres
    container_name: db
    ports:
      - 5432:5432
    networks:
      - sonarnet
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
  sonarqube:
    image: sonarqube:8.9.3-community
    container_name: sonarqube
    depends_on:
      - db
    ports:
      - "9000:9000"
    networks:
      - sonarnet
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
networks:
  sonarnet:
    driver: bridge
```

启动容器

```bash
docker-compose up -d
```

需要设置sysctl.conf文件信息

设置vm.max\_map\_count

![](../../image/31649b32f80f48dc89aa370d701adfa4.png)

 并执行命令刷新

```bash
sysctl -p
```

重新启动需要一定时间启动，可以可以查看容器日志，看到如下内容代表启动成功

容器日志

![](../../image/3dd7b55369524f7e9408b0df578897a3.png)

 访问Sonar Qube首页

![](../../image/2b30dc4d08ce4142a169549e1b5319cb.png)

 

还需要重新设置一次密码 ![](../../image/fe9085ce4e634ebdb8e559a7d6ad47f8.png)

 Sonar Qube首页

![](../../image/4f533f30087841a7ae5b98f1d2b99d37.png)

 

安装中文插件

![](../../image/9f7e9aec00634d43bf690217d42040cf.png)

 

安装成功后需要重启，安装失败重新点击install重装即可。

安装成功后，会查看到重启按钮，点击即可

![](../../image/e3536c65b6cb403d83011da3d9404b61.png)

 重启后查看效果

![](../../image/cdfbb859c349429d83e3090e9b9f4de0.png)

 

## Sonar Qube基本使用

Sonar Qube的使用方式很多，Maven可以整合，也可以采用sonar-scanner的方式，再查看Sonar Qube的检测效果

## Maven实现代码检测

  - 修改Maven的settings.xml文件配置Sonar Qube信息

```bash
<profile>
    <id>sonar</id>
    <activation>
        <activeByDefault>true</activeByDefault>
    </activation>
    <properties>
        <sonar.login>admin</sonar.login>
        <sonar.password>admin123456</sonar.password>
        <sonar.host.url>http://172.17.1.22:9000</sonar.host.url>
    </properties>
</profile>
```

在代码位置执行命令：mvn sonar:sonar

![](../../image/5ebc436dfe5d4ed0a994b2e534c98db9.png)

 查看Sonar Qube界面检测结果

![](../../image/4a691677a8d74e00a2089e7f496815e0.png)

 

## Sonar-scanner实现代码检测

- 下载Sonar-scanner：<https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/>

  下载4.6.x版本即可，要求Linux版本

  - 解压并配置sonar服务端信息

  - 由于是zip压缩包，需要安装unzip解压插件     

```bash
yum -y install unzip
```

解压压缩包

```bash
unzip sonar-scanner-cli/sonar-scanner-cli-4.6.0.2311-linux.zip
```

配置sonarQube服务端地址，修改conf下的sonar-scanner.properties

![](../../image/b0f89eb4e7d7432d90f38ddeae1d647a.png)

 

执行命令检测代码

```bash
# 在项目所在目录执行以下命令
~/sonar-scanner/bin/sonar-scanner -Dsonar.sources=./ -Dsonar.projectname=demo -Dsonar.projectKey=java -Dsonar.java.binaries=target/
```

查看日志信息

![](../../image/f2f928ad1af34e5fb26eaad897850e1b.png)

 查看SonarQube界面检测结果

![](../../image/bf4673fda3164d289dad73bff4610ca0.png)

 

# Jenkins集成Sonar Qube

Jenkins继承Sonar Qube实现代码扫描需要先下载整合插件

Jenkins安装插件

![](../../image/73e7e4c30fac4b2d91895ea7a70cffb0.png)

 

Jenkins配置Sonar Qube

开启Sonar Qube权限验证

![](../../image/618cd3f1cec44319b5fb47a88fd079cc.png)

 获取Sonar Qube的令牌

![](../../image/7d5cc9a2e4b74b30a1c08617b458b4a5.png)

 配置Jenkins的Sonar Qube信息

![](../../image/2c8ec7a11b574c7d97abb8d01c069ea8.png)

![](../../image/b146b6549894423fa65deb5a06d0b6a3.png)

 

![](../../image/6be851129a93498fa47164082700717d.png)

 

配置Sonar-scanner

- 将Sonar-scaner添加到Jenkins数据卷中并配置全局配置

 ![](../../image/260c400694784b5fa48108bf9916c40b.png)

配置任务的Sonar-scanner  

![](../../image/abfb1624026742649689eae2ab81ef97.png)

```bash
~/sonar-scanner/bin/sonar-scanner -Dsonar.sources=./ -Dsonar.projectname=demo -Dsonar.projectKey=java -Dsonar.java.binaries=target/


#主要下面这个
sonar.projectname=${JOB_NAME}
sonar.projectKey=${JOB_NAME}
sources=./
sonar.java.binaries=target/
```

构建任务

 ![](../../image/5777ed541ffb4a01b8b8970630f5c593.png)

![](../../image/279a56a4e4804b7c97a7525c4f8ab923.png)

已经上传镜像包

![](../../image/931d6c12d1aa497ea2c91f625a5adbc1.png) 

 ![](../../image/398317c8afd647f8bb3ed893b0cb39a7.png)

**注意：我这里代码编译这一块，缺少那个 切换分支编译，如果有需要，需要自己配置** 

![](../../image/a43bfb64795148819d7e5361ed6a1b1d.png)