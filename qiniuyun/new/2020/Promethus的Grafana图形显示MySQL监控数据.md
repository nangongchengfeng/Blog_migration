---
author: 南宫乘风
categories:
- Prometheus监控
date: 2020-01-13 15:42:22
description: 相关博文：、安装普罗米修斯监控系统完整版、普罗米修斯监控数据库、普罗米修斯安装可视化图形工具、的图形显示监控数据、普罗米修斯的实现报警功能目录图形显示监控数据在上修改配置文件并下载安装监控的包含相关文。。。。。。。
image: http://image.ownit.top/4kdongman/14.jpg
tags:
- Grafana
- Promethus
- mysql
- 监控
title: Promethus的Grafana图形显示MySQL监控数据
---

<!--more-->

 

# 相关博文：

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)

 

 

**目录**

[Grafana图形显示MySQL监控数据](#Grafana%E5%9B%BE%E5%BD%A2%E6%98%BE%E7%A4%BAMySQL%E7%9B%91%E6%8E%A7%E6%95%B0%E6%8D%AE)

 

[① 在grafana上修改配置文件,并下载安装mysql监控的dashboard（包含 相关json文件，这些json文件可以看作是开发人员开发的一个监控模板\)](<#① 在grafana上修改配置文件,并下载安装mysql监控的dashboard（包含 相关json文件，这些json文件可以看作是开发人员开发的一个监控模板)>)

[② 在grafana图形界面导入相关json文件](<#② 在grafana图形界面导入相关json文件>)

---

# Grafana图形显示MySQL监控数据

 

## ① 在grafana上修改配置文件,并下载安装mysql监控的dashboard（包含 相关json文件，这些json文件可以看作是开发人员开发的一个监控模板\)

参考网址: <https://github.com/percona/grafana-dashboards>

在grafana配置文件里最后加上以下三行

```bash
vim /etc/grafana/grafana.ini 
[dashboards.json] 
enabled = true 
path = /var/lib/grafana/dashboards
```

![](http://image.ownit.top/csdn/20200113150203274.png)

![](http://image.ownit.top/csdn/20200113150322470.png)

下载配置模板

```bash
cd /var/lib/grafana/ 
```

```
git clone https://github.com/percona/grafana-dashboards.git 
```

```
cp -r /var/lib/grafana/grafana-dashboards-master/dashboards/ /var/lib/grafana/ 
```

![](http://image.ownit.top/csdn/20200113151342364.png)

重启grafana服务

```
systemctl restart grafana-server
```

## ② 在grafana图形界面导入相关json文件

![](http://image.ownit.top/csdn/20200113151442401.png)

![](http://image.ownit.top/csdn/20200113151636828.png)

③ 点import导入后,报prometheus数据源找不到,因为这些json文件里默认 要找的就是叫Prometheus的数据源，但我们前面建立的数据源却是叫 prometheus\_data\(坑啊\)  
那么请自行把原来的prometheus\_data源改名为Prometheus即可\(注意: 第一个字母P是大写\)  
然后再回去刷新,就有数据了\(如下图所示\)

![](http://image.ownit.top/csdn/2020011315383743.png)

# 相关博文：

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)