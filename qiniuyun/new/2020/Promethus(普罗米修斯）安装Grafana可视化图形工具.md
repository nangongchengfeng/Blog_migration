---
author: 南宫乘风
categories:
- Prometheus监控
date: 2020-01-13 14:27:19
description: 相关博文：、安装普罗米修斯监控系统完整版、普罗米修斯监控数据库、普罗米修斯安装可视化图形工具、的图形显示监控数据、普罗米修斯的实现报警功能教程使用的软件：链接提取码环境配置服务器地址服务器被监控服务器。。。。。。。
image: http://image.ownit.top/4kdongman/43.jpg
tags:
- Grafana
- Promethus
- 监控
title: Promethus(普罗米修斯）安装Grafana可视化图形工具
---

<!--more-->

 

# 相关博文：

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)

 

![](http://image.ownit.top/csdn/20200113144441132.png)

教程使用的软件：链接: <https://pan.baidu.com/s/1QV4KYZksyIp65UsScioq4Q> 提取码: vcej

环境配置

<table border="1" cellpadding="1" cellspacing="1"><tbody><tr><td>服务器</td><td>IP地址</td></tr><tr><td>Prometneus服务器</td><td>192.168.116.129</td></tr><tr><td>被监控服务器（mysql）</td><td>192.168.116.130</td></tr><tr><td>grafana服务器</td><td>192.168.116.131</td></tr></tbody></table>

# 1、什么是Grafana

 Grafana是一个开源的度量分析和可视化工具，可以通过将采集的数据分 析，查询，然后进行可视化的展示,并能实现报警。

![](http://image.ownit.top/csdn/20200113140317374.png)

 

网址: <https://grafana.com/>

# 2、使用Grafana连接Prometheus

 

## ① 在grafana服务器上安装grafana

下载地址:<https://grafana.com/grafana/download>

上传grafana-5.3.4-1.x86\_64.rpm

![](http://image.ownit.top/csdn/20200113140643778.png)

我这里选择的rpm包，下载后直接rpm \-ivh安装就OK【失败原因缺少组件，可以yum安装组件】

```bash
rpm -ivh /root/Desktop/grafana-5.3.41.x86_64.rpm
```

![](http://image.ownit.top/csdn/20200113140719321.png)

或者第二种方法【yum安装会自动安装缺少的组件的】

```bash
yum install -y grafana-5.3.4-1.x86_64.rpm 
```

![](http://image.ownit.top/csdn/20200113140902426.png)

启动服务

```
systemctl start grafana-server 
systemctl enable grafana-server 
```

确认端口\(3000\)

```
lsof -i:3000
```

![](http://image.ownit.top/csdn/20200113141145828.png)

## ② 通过浏览器访问 http:// grafana服务器IP:3000就到了登录界面,使用默 认的admin用户,admin密码就可以登陆了

![](http://image.ownit.top/csdn/20200113141221182.png)

## ③ 下面我们把prometheus服务器收集的数据做为一个数据源添加到 grafana,让grafana可以得到prometheus的数据。

![](http://image.ownit.top/csdn/20200113141320184.png)

 

![](http://image.ownit.top/csdn/20200113141836837.png)

![](http://image.ownit.top/csdn/20200113141918275.png)

## ④ 然后为添加好的数据源做图形显示

![](http://image.ownit.top/csdn/20200113141945357.png)

![](http://image.ownit.top/csdn/20200113141955537.png)

 

![](http://image.ownit.top/csdn/20200113142000200.png)

![](http://image.ownit.top/csdn/20200113142330949.png)

## ⑤ 保存

![](http://image.ownit.top/csdn/20200113142408364.png)

## ⑥ 最后在dashboard可以查看到

![](http://image.ownit.top/csdn/2020011314245957.png)

⑦ 匹配条件显示

![](http://image.ownit.top/csdn/20200113142634216.png)

# 相关博文：

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)