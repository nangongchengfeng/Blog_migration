+++
author = "南宫乘风"
title = "Centos7安装dubbo与zookeeper服务配置"
date = "2019-09-28 14:22:52"
tags=[]
categories=['软件', 'Java', ' Linux实战操作']
image = "post/4kdongman/66.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/101613518](https://blog.csdn.net/heian_99/article/details/101613518)

**目录**

[环境： ](#%E7%8E%AF%E5%A2%83%EF%BC%9A%C2%A0)

[第一步：安装jdk，并且配置环境变量](#%E7%AC%AC%E4%B8%80%E6%AD%A5%EF%BC%9A%E5%AE%89%E8%A3%85jdk%EF%BC%8C%E5%B9%B6%E4%B8%94%E9%85%8D%E7%BD%AE%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%EF%BC%88*%EF%BC%89%C2%A0)

[ 1.解压jdk：](#%C2%A01.%E8%A7%A3%E5%8E%8Bjdk%EF%BC%9A)

[2.配置环境变量：](#2.%E6%8F%90%E5%8F%96%E6%9D%83%E9%99%90%EF%BC%9A)

[3.保存并使文件立即生效：](#4.%E4%BF%9D%E5%AD%98%E5%B9%B6%E4%BD%BF%E6%96%87%E4%BB%B6%E7%AB%8B%E5%8D%B3%E7%94%9F%E6%95%88%EF%BC%9A)

[4.立即重启虚拟机，进行下面的安装](#5.%E7%AB%8B%E5%8D%B3%E9%87%8D%E5%90%AF%E8%99%9A%E6%8B%9F%E6%9C%BA%EF%BC%8C%E8%BF%9B%E8%A1%8C%E4%B8%8B%E9%9D%A2%E7%9A%84%E5%AE%89%E8%A3%85)

[第二步：安装注册中心zookeeper ](#%E7%AC%AC%E4%BA%8C%E6%AD%A5%EF%BC%9A%E5%AE%89%E8%A3%85%E6%B3%A8%E5%86%8C%E4%B8%AD%E5%BF%83zookeeper%C2%A0)

[1.解压zookeeper：](#1.%E8%A7%A3%E5%8E%8Bzookeeper%EF%BC%9A)

[2.在zookeeper目录下创建data和logs目录：](#2.%E5%9C%A8zookeeper%E7%9B%AE%E5%BD%95%E4%B8%8B%E5%88%9B%E5%BB%BAdata%E5%92%8Clogs%E7%9B%AE%E5%BD%95%EF%BC%9A)

[3.将/usr/local/zookeeper3.4.6/zookeeper-3.4.6/conf 目录下的 zoo_sample.cfg拷贝：](#3.%E5%B0%86%2Fusr%2Flocal%2Fzookeeper3.4.6%2Fzookeeper-3.4.6%2Fconf%20%E7%9B%AE%E5%BD%95%E4%B8%8B%E7%9A%84%20zoo_sample.cfg%E6%8B%B7%E8%B4%9D%EF%BC%9A)

[4.修改配置文件：](#4.%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9A)

[​](#5.%E5%9C%A8zookeeper%E7%9A%84%E5%88%9A%E5%BB%BA%E7%AB%8B%E7%9A%84data%E6%96%87%E4%BB%B6%E5%AE%B6%E4%B8%8B%E5%88%9B%E5%BB%BAmyid%E6%96%87%E4%BB%B6%EF%BC%8C%E5%B9%B6%E4%B8%94%E7%BC%96%E8%BE%91myid%E6%96%87%E4%BB%B6%EF%BC%8C%E5%85%B6%E4%B8%AD%E5%86%99%E5%85%A51%EF%BC%88%E6%88%91%E8%BF%99%E9%87%8C%E6%98%AF%E5%8D%95%E8%8A%82%E7%82%B9%E5%AE%89%E8%A3%85%EF%BC%89)

[5.在vi /etc/profile末尾添加zookeeper配置](#6.%E5%9C%A8vi%20%2Fetc%2Fprofile%E6%9C%AB%E5%B0%BE%E6%B7%BB%E5%8A%A0zookeeper%E9%85%8D%E7%BD%AE)

[6.配置文件立即生效：](#7.%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E7%AB%8B%E5%8D%B3%E7%94%9F%E6%95%88%EF%BC%9A)

[7.关闭防火墙，并且启动测试](#8.%E5%85%B3%E9%97%AD%E9%98%B2%E7%81%AB%E5%A2%99%EF%BC%8C%E5%B9%B6%E4%B8%94%E5%90%AF%E5%8A%A8%E6%B5%8B%E8%AF%95)

[第三步：安装dubbo-admin-war和tomcat ](#%E7%AC%AC%E4%B8%89%E6%AD%A5%EF%BC%9A%E5%AE%89%E8%A3%85dubbo-admin-war%E5%92%8Ctomcat%C2%A0)

[1.解压tomcat:](#1.%E8%A7%A3%E5%8E%8Btomcat%3A)

[2.解压dubbo文件](#2.%E8%A7%A3%E5%8E%8B%E5%90%8E%E7%9A%84%E6%96%87%E4%BB%B6%E5%A4%B9%E9%87%8D%E6%96%B0%E5%91%BD%E5%90%8D%E4%B8%BA%3Adubbo-admin-tomcat)

[3.进入tomcat的conf目录下修改server.xml](#3.%E7%A7%BB%E9%99%A4dubbo-admin-tomcat%2Fwebapps%E6%89%80%E6%9C%89%E6%96%87%E4%BB%B6%EF%BC%9A)

[4.修改server.xml](#4.%E4%B8%8A%E4%BC%A0%E5%B9%B6%E4%B8%94%E8%A7%A3%E5%8E%8Bdubbo-tomcat-2.5.3.war%2C%E5%B9%B6%E4%B8%94%E6%8A%8A%E7%9B%AE%E5%BD%95%E5%91%BD%E5%90%8Droot)

[5.启动tomcat服务，进入tomcat的bin下](#5.%E9%85%8D%E7%BD%AEdubbo.properties)

[6.启动zookeeper服务，进入zookeeper的bin下](#6.%E5%90%AF%E5%8A%A8zookeeper%E6%9C%8D%E5%8A%A1%EF%BC%8C%E8%BF%9B%E5%85%A5zookeeper%E7%9A%84bin%E4%B8%8B)

[第四步：在浏览器中输入地址显示如下： ](#%E7%AC%AC%E5%9B%9B%E6%AD%A5%EF%BC%9A%E5%9C%A8%E6%B5%8F%E8%A7%88%E5%99%A8%E4%B8%AD%E8%BE%93%E5%85%A5%E5%9C%B0%E5%9D%80%E6%98%BE%E7%A4%BA%E5%A6%82%E4%B8%8B%EF%BC%9A%C2%A0)

## 环境： 

<br> 1.centos7 <br> 2.jdk-7u76-linux-x64.tar.gz <br> 2.tomcat:apache-tomcat-7.0.59.tar.gz <br> 3.zookeeper-3.4.6.tar.gz <br> 4.dubbo-admin-2.5.3.war

![20190928141819246.png](https://img-blog.csdnimg.cn/20190928141819246.png)

具体的流程： 

## <br> 第一步：安装jdk，并且配置环境变量

<br> xshell5命令:

###  <br> 1.解压jdk：

```
tar zxvf  jdk-7u76-linux-x64.tar.gz
```

### 2.配置环境变量：

/opt/jdk1.8.0_152  :为jdk解压的路径

![20191008212949409.png](https://img-blog.csdnimg.cn/20191008212949409.png)

```
[root@localhost~]# vi  /etc/profile 
```

```
export JAVA_HOME=/opt/jdk1.8.0_152
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH
```

### 3.保存并使文件立即生效：

```
保存：点击ESC键，并且输入:wq;
立即生效：source /etc/profile
```

### 4.立即重启虚拟机，进行下面的安装

```
shutdown -r now
```

## 第二步：安装注册中心zookeeper 

### <br> 1.解压zookeeper：

```
tar zxvf zookeeper-3.4.6.tar.gz 
```

### 2.在zookeeper目录下创建data和logs目录：

```
mkdir data


```

### 3.将/usr/local/zookeeper3.4.6/zookeeper-3.4.6/conf 目录下的 zoo_sample.cfg拷贝：

```
 cp zoo_sample.cfg zoo.cfg
```

### 4.修改配置文件：

```
vi zoo.cfg
```

### ![20191008213223570.png](https://img-blog.csdnimg.cn/20191008213223570.png)

### 5.在vi /etc/profile末尾添加zookeeper配置

```
export ZOOKEEPER_HOME=/opt/zookeeper-3.4.11
export PATH=$ZOOKEEPER_HOME/bin:$PATH

```

### 6.配置文件立即生效：

```
source /etc/profile
```

### 7.关闭防火墙，并且启动测试

```
systemctl stop firewalld.service
在zookeeper的bin目录下执行： ./zkServer.sh start
```

## 第三步：安装dubbo-admin-war和tomcat 

### <br> 1.解压tomcat:

```
tar zxvf apache-tomcat-7.0.59.tar.gz 
```

### 2.解压dubbo文件

```
unzip dubbo-admin-2.6.0.war -d dubbo

```

### 3.进入tomcat的conf目录下修改server.xml

![20191008213748704.png](https://img-blog.csdnimg.cn/20191008213748704.png)

### 4.修改server.xml

![20191008213844490.png](https://img-blog.csdnimg.cn/20191008213844490.png)

```
&lt;Context path="/dubbo" docBase="/opt/dubbo" debug="0" privileged="true" /&gt;


```

### <br> 5.启动tomcat服务，进入tomcat的bin下

```
startup.sh
```

### 6.启动zookeeper服务，进入zookeeper的bin下

 

```
bash zkServer.sh start

bash zkServer.sh status

```

 

## 第四步：在浏览器中输入地址显示如下： 

账号：root

密码：root

![20190928142526505.png](https://img-blog.csdnimg.cn/20190928142526505.png)

 

![20190928142559185.png](https://img-blog.csdnimg.cn/20190928142559185.png)
