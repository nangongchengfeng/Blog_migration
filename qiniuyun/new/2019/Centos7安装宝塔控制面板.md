---
author: 南宫乘风
categories:
- Linux实战操作
date: 2019-09-24 09:48:52
description: 目录宝塔面板安装和使用图文教程通过工具登录服务器，安装宝塔面板，登录宝塔面板，设置宝塔面板，首先我们进入面板设置，更改面板端口，绑定域名，绑定，更改默认的面板用户和密码，绑定宝塔账号，绑定微信小程序，。。。。。。。
image: http://image.ownit.top/4kdongman/81.jpg
tags:
- 技术记录
title: Centos7安装宝塔控制面板
---

<!--more-->

**目录**

[宝塔面板安装和使用图文教程](#%E5%AE%9D%E5%A1%94%E9%9D%A2%E6%9D%BF%E5%AE%89%E8%A3%85%E5%92%8C%E4%BD%BF%E7%94%A8%E5%9B%BE%E6%96%87%E6%95%99%E7%A8%8B)

[1,通过ssh工具登录服务器](#1%2C%E9%80%9A%E8%BF%87ssh%E5%B7%A5%E5%85%B7%E7%99%BB%E5%BD%95%E6%9C%8D%E5%8A%A1%E5%99%A8)

[2，安装宝塔面板](#2%EF%BC%8C%E5%AE%89%E8%A3%85%E5%AE%9D%E5%A1%94%E9%9D%A2%E6%9D%BF)

[2，登录宝塔面板](#2%EF%BC%8C%E7%99%BB%E5%BD%95%E5%AE%9D%E5%A1%94%E9%9D%A2%E6%9D%BF)

[3，设置宝塔面板](#3%EF%BC%8C%E8%AE%BE%E7%BD%AE%E5%AE%9D%E5%A1%94%E9%9D%A2%E6%9D%BF)

[3.1，首先我们进入面板设置](#3.1%EF%BC%8C%E9%A6%96%E5%85%88%E6%88%91%E4%BB%AC%E8%BF%9B%E5%85%A5%E9%9D%A2%E6%9D%BF%E8%AE%BE%E7%BD%AE)

[3.2，更改面板端口](#3.2%EF%BC%8C%E6%9B%B4%E6%94%B9%E9%9D%A2%E6%9D%BF%E7%AB%AF%E5%8F%A3)

[3.3，绑定域名](#3.3%EF%BC%8C%E7%BB%91%E5%AE%9A%E5%9F%9F%E5%90%8D)

[3.4，绑定ip](#3.4%EF%BC%8C%E7%BB%91%E5%AE%9Aip)

[3.5，更改默认的面板用户和密码](#3.5%EF%BC%8C%E6%9B%B4%E6%94%B9%E9%BB%98%E8%AE%A4%E7%9A%84%E9%9D%A2%E6%9D%BF%E7%94%A8%E6%88%B7%E5%92%8C%E5%AF%86%E7%A0%81)

[3.5，绑定宝塔账号](#3.5%EF%BC%8C%E7%BB%91%E5%AE%9A%E5%AE%9D%E5%A1%94%E8%B4%A6%E5%8F%B7)

[3.6，绑定微信小程序](#3.6%EF%BC%8C%E7%BB%91%E5%AE%9A%E5%BE%AE%E4%BF%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F)

[4，宝塔面板安全设置](#4%EF%BC%8C%E5%AE%9D%E5%A1%94%E9%9D%A2%E6%9D%BF%E5%AE%89%E5%85%A8%E8%AE%BE%E7%BD%AE)

[5，安装面板环境](#5%EF%BC%8C%E5%AE%89%E8%A3%85%E9%9D%A2%E6%9D%BF%E7%8E%AF%E5%A2%83)

[6，创建网站](#6%EF%BC%8C%E5%88%9B%E5%BB%BA%E7%BD%91%E7%AB%99)

[7，购买插件](#7%EF%BC%8C%E8%B4%AD%E4%B9%B0%E6%8F%92%E4%BB%B6)

[8，升级为专业版](#8%EF%BC%8C%E5%8D%87%E7%BA%A7%E4%B8%BA%E4%B8%93%E4%B8%9A%E7%89%88)

 

---

# 宝塔面板安装和使用图文教程

 

如果你要安装宝塔linux面板,你要准备好一个纯净版的linux操作系统，没有安装过其它环境带的Apache/Nginx/php/MySQL（已有环境不可安装）。支持的操作系统有CentOS，Ubuntu、Debian、Fedora。这里给大家演示的是centos7.5。

## 1,通过ssh工具登录服务器

这里推荐大家使用xshell进行登录。注意要开放ssh连接的端口，一般默认是22，为了网站安全推荐大家更换ssh登录端口。设置为不常用的端口。![](http://image.ownit.top/csdn/2019092409444732.png)

输入账号和密码，注意密码在输入时是不显示的，大家不要以为密码没输入。

## 2，安装宝塔面板

执行以下代码进行安装宝塔6.9免费版。宝塔6.9版本已经很稳定了，推荐大家直接安装6.9版本（注意：宝塔linux6.0版本是基于centos7开发的，务必使用centos7.x 系统

```
[root@wei ~]# yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh
```

如果大家系统是centos7以下的大家还是乖乖使用宝塔5.9的安装脚本（Centos官方已宣布在2020年停止对Centos6的维护更新，推荐大家装系统直接安装centos7）

```
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install.sh && sh install.sh
```

回车进行安装。

[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180923232554.png)

输入y，并回车。接下来便是等待宝塔面板进行安装。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180923232950.png)

我们得到登录宝塔面板的URL,账号和密码。

## 2，登录宝塔面板

安装完成宝塔面板后，我们就可以在浏览器中访问了。复制Bt-panel中的URL到浏览器上访问。注意要打开服务器上的8888端口，关于如何打开服务器端口，你可以在本站中搜索答案。[![宝塔面板安装和使用图文教程](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180923233955.png)[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180923233704.png)

输入默认的账号和密码进行登录。

## 3，设置宝塔面板

登陆后进入宝塔面板我们可以看到如下图所示，你可以选择LNMP或者LAMP进行安装。看大家网站需要什么环境进行选择。如果是生产环境推荐大家使用编译安装，如果只是测试环境选择极速安装。两者的区别是编译安装慢但稳定，极速安装虽然慢但是没编译安装稳定。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180923234416.png)

推荐大家首次进入宝塔面板前不要进行环境的安装，因为在安装环境不能更改宝塔面板的设置。推荐大家先更改宝塔面板的默认设置，编译安装环境将近一个小时。在这段时间里我们先将宝塔面板设置好提高面板的安全性。

### 3.1，首先我们进入面板设置

[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180923235657.png)

### 3.2，更改面板端口

将端口更改为不常用的端口。

### 3.3，绑定域名

你可以绑定一个域名绑定完域名后只能通过你绑定的域名来访问面板。

### 3.4，绑定ip

如果你有固定的ip，你可绑定ip访问，绑定了ip访问你只能通过绑定得这个ip进行访问。如果你是家用电脑就不要绑定ip了，因为家用电脑的ip是动态的。这就会造成ip发生改变面板访问不了。

### 3.5，更改默认的面板用户和密码

更改宝塔安装完成时的默认用户名和密码，设置一个自己能记住的用户名和密码，密码不要太简单了。

### 3.5，绑定宝塔账号

如果你有宝塔账号你可以绑定下，没有的话可以去宝塔官网申请。宝塔账号在购买付费插件，开通专业版时要用到。要去注册账号

### 3.6，绑定微信小程序

由于微信小程序是付费插件，你只有购买了或者开通专业版才能使用。微信小程序能够监控服务器，方便用户随时查看服务器状态。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924002728.png)

## 4，宝塔面板安全设置

在这里你可以开启和禁用一些端口。推荐大家更改ssh端口，和禁用ping。更改FTP端口。更改phpadmin默认端口。不常用的端口可以把它关闭，等要使用了在开启。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924004619.png)

 

## 5，安装面板环境

在软件管理选择你所需要的网站环境进行安装。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924002833.png)

在这里老杨选择LNMP进行安装，即Linux+Nginx+Mysql+Php。

## 6，创建网站

等网站环境安装完成后便可以创建网站，有两种方法可以创建网站。第一种直接在选择网站，选择添加站点，进行创建网站。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924005213.png)

第二种在软件管理中的宝塔插件中安装宝塔一键部署源码插件进行创建网站。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924004255.png)

## 7，购买插件

如果你在使用过程中需要用到某款插件你可以到软件管理>付费插件进行购买。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924005542.png)

选择购买时间进行购买。

## 8，升级为专业版

如果你在使用过程中需要使用到多款付费插件推荐大家升级专业版。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924005822.png)

选择时间并进行支付。

如果你有账号有购买过专业版你可以选择代金劵进行支付。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924010421.png)

[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924010655.png)

刷新下面板在到期时间可以看到永久授权四个字。[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924010814.png)

如果升级不成功可以ssh登录到服务器执行升级代码进行升级。

```html
 ```

1.  wget -O update.sh http://download.bt.cn/install/update\_pro.sh \&\& bash update.sh pro

[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924011530.png)

或者进入文件管理器，打开终端，粘贴升级代码，然后点击“发送”，手动升级到专业版。

[![](format,png)](https://www.laoyangblog.com/wp-content/uploads/2018/09/20180924011916.png)