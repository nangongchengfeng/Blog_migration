---
author: 南宫乘风
categories:
- Prometheus监控
date: 2020-01-13 16:52:18
description: 、安装普罗米修斯监控系统完整版、普罗米修斯监控数据库、普罗米修斯安装可视化图形工具、的图形显示监控数据、普罗米修斯的实现报警功能目录、安装普罗米修斯监控系统完整版、安装普罗米修斯监控系统完整版、普罗米。。。。。。。
image: http://image.ownit.top/4kdongman/11.jpg
tags:
- Grafana
- Promethus
- onealert
- 告警
- 监控
title: Promethus(普罗米修斯）的Grafana+onealert实现报警功能
---

<!--more-->

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)

 

**目录**

[1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](<#1、Centos7安装Promethus(普罗米修斯）监控系统完整版>)

[2、Promethus\(普罗米修斯）监控Mysql数据库](<#2、Promethus(普罗米修斯）监控Mysql数据库>)

[3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](<#3、Promethus(普罗米修斯）安装Grafana可视化图形工具>)

[4、Promethus的Grafana图形显示MySQL监控数据](#4%E3%80%81Promethus%E7%9A%84Grafana%E5%9B%BE%E5%BD%A2%E6%98%BE%E7%A4%BAMySQL%E7%9B%91%E6%8E%A7%E6%95%B0%E6%8D%AE)

[Grafana+onealert报警](#Grafana%2Bonealert%E6%8A%A5%E8%AD%A6)

[1、 先在onealert里添加grafana应用\(申请onealert账号\)](<#1、 先在onealert里添加grafana应用(申请onealert账号)>)

[2、在Grafana中配置Webhook URL](<#2、在Grafana中配置Webhook URL>)

[现在可以去设置一个报警来测试了\(这里以我们前面加的cpu负载监控来 做测试\)](<#现在可以去设置一个报警来测试了(这里以我们前面加的cpu负载监控来 做测试)>)

[最终的邮件报警效果：](#%E6%9C%80%E7%BB%88%E7%9A%84%E9%82%AE%E4%BB%B6%E6%8A%A5%E8%AD%A6%E6%95%88%E6%9E%9C%EF%BC%9A)

[测试mysql链接数报警](#%E6%B5%8B%E8%AF%95mysql%E9%93%BE%E6%8E%A5%E6%95%B0%E6%8A%A5%E8%AD%A6)

[总结报警不成功的可能原因](#%E6%80%BB%E7%BB%93%E6%8A%A5%E8%AD%A6%E4%B8%8D%E6%88%90%E5%8A%9F%E7%9A%84%E5%8F%AF%E8%83%BD%E5%8E%9F%E5%9B%A0)

[扩展](#%E6%89%A9%E5%B1%95)

---
 

# Grafana+onealert报警

prometheus报警需要使用alertmanager这个组件，而且报警规则需要手 动编写\(对运维来说不友好\)。所以我这里选用grafana+onealert报警。

注意: 实现报警前把所有机器时间同步再检查一遍.

```
ntpdate time.windows.com
```

## 1、 先在onealert里添加grafana应用\(申请onealert账号\)

[https://caweb.aiops.com/](https://caweb.aiops.com/#/)

![](http://image.ownit.top/csdn/20200113161638506.png)

 

![](http://image.ownit.top/csdn/20200113161840200.png)

![](http://image.ownit.top/csdn/20200113161917501.png)

## 2、在Grafana中配置Webhook URL

1、在Grafana中创建Notification channel，选择类型为Webhook；

![](http://image.ownit.top/csdn/20200113162343122.png)

2、推荐选中Send on all alerts和Include image，Cloud Alert体验更佳；

3、将第一步中生成的Webhook URL填入Webhook settings Url；

4、Http Method选择POST；

5、Send Test\&Save；

![](http://image.ownit.top/csdn/20200113162656163.png)

![](http://image.ownit.top/csdn/20200113162840747.png)

## 现在可以去设置一个报警来测试了\(这里以我们前面加的cpu负载监控来 做测试\)

![](http://image.ownit.top/csdn/20200113163106677.png)

配置

![](http://image.ownit.top/csdn/20200113163345919.png)

![](http://image.ownit.top/csdn/20200113163324830.png)

保存后就可以测试了

![](http://image.ownit.top/csdn/20200113163729952.png)

如果node1上的cpu负载还没有到0.5，你可以试试0.1,或者运行一些程序 把node1负载调大。最终能测试报警成功

![](http://image.ownit.top/csdn/20200113163902132.png)

模拟cpu负载

```
cat /dev/urandom | md5sum
```

 

## 最终的邮件报警效果：

![](http://image.ownit.top/csdn/20200113164329432.png)

![](http://image.ownit.top/csdn/20200113164457435.png)

## 测试mysql链接数报警

![](http://image.ownit.top/csdn/20200113164810425.png)

![](http://image.ownit.top/csdn/20200113164821235.png)

![](http://image.ownit.top/csdn/20200113164837652.png)

![](http://image.ownit.top/csdn/20200113164839384.png)

![](http://image.ownit.top/csdn/20200113164902506.png)

## 总结报警不成功的可能原因

- 各服务器之间时间不同步，这样时序数据会出问题，也会造成报警出问 题
- 必须写通知内容，留空内容是不会发报警的
- 修改完报警配置后，记得要点右上角的保存
- 保存配置后，需要由OK状态变为alerting状态才会报警\(也就是说，你 配置保存后，就已经是alerting状态是不会报警的\)
- grafana与onealert通信有问题

# 扩展

prometheus目前还在发展中，很多相应的监控都需要开发。但在官网的 dashboard库中,也有一些官方和社区开发人员开发的dashboard可以直接 拿来用。

![](http://image.ownit.top/csdn/20200113165033603.png)

![](http://image.ownit.top/csdn/20200113165056782.png)

![](http://image.ownit.top/csdn/20200113165113140.png)

# 相关博文

 

# [1、Centos7安装Promethus\(普罗米修斯）监控系统完整版](https://blog.csdn.net/heian_99/article/details/103952955)

# [2、Promethus\(普罗米修斯）监控Mysql数据库](https://blog.csdn.net/heian_99/article/details/103956583)

# [3、Promethus\(普罗米修斯）安装Grafana可视化图形工具](https://blog.csdn.net/heian_99/article/details/103956931)

# [4、Promethus的Grafana图形显示MySQL监控数据](https://blog.csdn.net/heian_99/article/details/103958032)

# [5、Promethus\(普罗米修斯）的Grafana+onealert实现报警功能](https://blog.csdn.net/heian_99/article/details/103959379)