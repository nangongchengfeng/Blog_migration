+++
author = "南宫乘风"
title = "Jenkins安装部署使用"
date = "2022-05-16 21:47:34"
tags=['jenkins', '运维', 'ci']
categories=['Jenkins']
image = "post/4kdongman/70.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/124808858](https://blog.csdn.net/heian_99/article/details/124808858)

## 介绍

Jenkins是一个独立的开源软件项目，是基于Java开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。前身是Hudson是一个可扩展的持续集成引擎。可用于自动化各种任务，如构建，测试和部署软件。Jenkins可以通过本机系统包Docker安装，甚至可以通过安装Java Runtime Environment的任何机器独立运行。

## **Jenkins特点**
- 开源免费;- 跨平台，支持所有的平台;- master/slave支持分布式的build;- web形式的可视化的管理页面;- 安装配置超级简单;- tips及时快速的帮助；- 已有的200多个插件
![86052dfea3b0439bbca0450729bbbb67.png](https://img-blog.csdnimg.cn/86052dfea3b0439bbca0450729bbbb67.png)

 

## 安装教程

这里我们使用的是离线包方式安装。

官网镜像地址: [Index of /](https://mirrors.jenkins.io/)<br> 下载地址： [Jenkins download and deployment](https://jenkins.io/download/)<br> 华为镜像地址: [华为开源镜像站_软件开发服务_华为云](https://mirrors.huaweicloud.com/home)

直接下载war包，并安装好jdk之后，输入:nohup java -jar jenkins.war --httpPort=8888 &amp;<br> 进行启动，然后网页浏览器输入 ip:8888打开设置好账号密码之后登录即可，插件安装推荐使用官方推荐。



![07ec709025734dc3abde51e5eea918e7.png](https://img-blog.csdnimg.cn/07ec709025734dc3abde51e5eea918e7.png)

 

##  Docker安装



拉取Jenkins镜像

```
docker pull jenkins/jenkins
```

编写docker-compose.yml

```
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

![62f58ce9ce6d41a58af241b832b40ee0.png](https://img-blog.csdnimg.cn/62f58ce9ce6d41a58af241b832b40ee0.png)

 

首次启动会因为数据卷data目录没有权限导致启动失败，设置data目录写权限

![661580a6b2534c2888bfb7a2e03155e3.png](https://img-blog.csdnimg.cn/661580a6b2534c2888bfb7a2e03155e3.png)

```
chmod -R a+w data/ 
```

重新启动Jenkins容器后，由于Jenkins需要下载大量内容，但是由于默认下载地址下载速度较慢，需要重新设置下载地址为国内镜像站

```
# 修改数据卷中的hudson.model.UpdateCenter.xml文件
&lt;?xml version='1.1' encoding='UTF-8'?&gt;
&lt;sites&gt;
  &lt;site&gt;
    &lt;id&gt;default&lt;/id&gt;
    &lt;url&gt;https://updates.jenkins.io/update-center.json&lt;/url&gt;
  &lt;/site&gt;
&lt;/sites&gt;
# 将下载地址替换为http://mirror.esuni.jp/jenkins/updates/update-center.json
&lt;?xml version='1.1' encoding='UTF-8'?&gt;
&lt;sites&gt;
  &lt;site&gt;
    &lt;id&gt;default&lt;/id&gt;
    &lt;url&gt;http://mirror.esuni.jp/jenkins/updates/update-center.json&lt;/url&gt;
  &lt;/site&gt;
&lt;/sites&gt;
# 清华大学的插件源也可以https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json
```

再次重启Jenkins容器，访问Jenkins（需要稍微等会）

```
docker-compose restart
```

![7ce8b117fb53454e8058546550c9fe0e.png](https://img-blog.csdnimg.cn/7ce8b117fb53454e8058546550c9fe0e.png)

 查看密码登录Jenkins，并登录下载插件

```
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

![fa7589e1e1394ff8b6d2714363813f7c.png](https://img-blog.csdnimg.cn/fa7589e1e1394ff8b6d2714363813f7c.png)

![5abb45aa916a4a128883e68eed03fab5.png](https://img-blog.csdnimg.cn/5abb45aa916a4a128883e68eed03fab5.png) 

 ![4b4be6f3cd8641c291b3c1a3eb6cfbee.png](https://img-blog.csdnimg.cn/4b4be6f3cd8641c291b3c1a3eb6cfbee.png)

 

![3a2abc00ac6d4289b96654fcea395fed.png](https://img-blog.csdnimg.cn/3a2abc00ac6d4289b96654fcea395fed.png)

 

![4ae63c3c631d42e5a67b96c810a22ace.png](https://img-blog.csdnimg.cn/4ae63c3c631d42e5a67b96c810a22ace.png)

![86d90cfe377942d3ade053fd48f021fd.png](https://img-blog.csdnimg.cn/86d90cfe377942d3ade053fd48f021fd.png) 

 ![935c92d6ed8249e9acef95793cc67cdf.png](https://img-blog.csdnimg.cn/935c92d6ed8249e9acef95793cc67cdf.png)

 



![59d332cba48f4a648a538bc891b6e6f4.png](https://img-blog.csdnimg.cn/59d332cba48f4a648a538bc891b6e6f4.png)

 


