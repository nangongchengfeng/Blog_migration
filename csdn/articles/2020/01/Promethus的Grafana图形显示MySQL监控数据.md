+++
author = "南宫乘风"
title = "Promethus的Grafana图形显示MySQL监控数据"
date = "2020-01-13 15:42:22"
tags=['Grafana', 'Promethus', 'mysql', '监控']
categories=['Prometheus监控']
image = "post/4kdongman/24.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103958032](https://blog.csdn.net/heian_99/article/details/103958032)

#  

# 相关博文：

# [1、Centos7安装Promethus(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)

#  

 

**目录**

[Grafana图形显示MySQL监控数据](#Grafana%E5%9B%BE%E5%BD%A2%E6%98%BE%E7%A4%BAMySQL%E7%9B%91%E6%8E%A7%E6%95%B0%E6%8D%AE)

 

[① 在grafana上修改配置文件,并下载安装mysql监控的dashboard（包含 相关json文件，这些json文件可以看作是开发人员开发的一个监控模板)](#%E2%91%A0%20%E5%9C%A8grafana%E4%B8%8A%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%2C%E5%B9%B6%E4%B8%8B%E8%BD%BD%E5%AE%89%E8%A3%85mysql%E7%9B%91%E6%8E%A7%E7%9A%84dashboard%EF%BC%88%E5%8C%85%E5%90%AB%20%E7%9B%B8%E5%85%B3json%E6%96%87%E4%BB%B6%EF%BC%8C%E8%BF%99%E4%BA%9Bjson%E6%96%87%E4%BB%B6%E5%8F%AF%E4%BB%A5%E7%9C%8B%E4%BD%9C%E6%98%AF%E5%BC%80%E5%8F%91%E4%BA%BA%E5%91%98%E5%BC%80%E5%8F%91%E7%9A%84%E4%B8%80%E4%B8%AA%E7%9B%91%E6%8E%A7%E6%A8%A1%E6%9D%BF%29)

[② 在grafana图形界面导入相关json文件](#%E2%91%A1%20%E5%9C%A8grafana%E5%9B%BE%E5%BD%A2%E7%95%8C%E9%9D%A2%E5%AF%BC%E5%85%A5%E7%9B%B8%E5%85%B3json%E6%96%87%E4%BB%B6)

# Grafana图形显示MySQL监控数据

 

## ① 在grafana上修改配置文件,并下载安装mysql监控的dashboard（包含 相关json文件，这些json文件可以看作是开发人员开发的一个监控模板)

参考网址: [https://github.com/percona/grafana-dashboards](https://github.com/percona/grafana-dashboards)

在grafana配置文件里最后加上以下三行

```
vim /etc/grafana/grafana.ini 
[dashboards.json] 
enabled = true 
path = /var/lib/grafana/dashboards

```

![20200113150203274.png](https://img-blog.csdnimg.cn/20200113150203274.png)

![20200113150322470.png](https://img-blog.csdnimg.cn/20200113150322470.png)

下载配置模板

```
cd /var/lib/grafana/ 
```

```
git clone https://github.com/percona/grafana-dashboards.git 
```

```
cp -r /var/lib/grafana/grafana-dashboards-master/dashboards/ /var/lib/grafana/ 

```

![20200113151342364.png](https://img-blog.csdnimg.cn/20200113151342364.png)

重启grafana服务

```
systemctl restart grafana-server
```

## ② 在grafana图形界面导入相关json文件

![20200113151442401.png](https://img-blog.csdnimg.cn/20200113151442401.png)

![20200113151636828.png](https://img-blog.csdnimg.cn/20200113151636828.png)

③ 点import导入后,报prometheus数据源找不到,因为这些json文件里默认 要找的就是叫Prometheus的数据源，但我们前面建立的数据源却是叫 prometheus_data(坑啊)<br> 那么请自行把原来的prometheus_data源改名为Prometheus即可(注意: 第一个字母P是大写)<br> 然后再回去刷新,就有数据了(如下图所示)

![2020011315383743.png](https://img-blog.csdnimg.cn/2020011315383743.png)

# 相关博文：

# [1、Centos7安装Promethus(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)

#  
