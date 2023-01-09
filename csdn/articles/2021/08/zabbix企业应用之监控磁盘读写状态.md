+++
author = "南宫乘风"
title = "zabbix企业应用之监控磁盘读写状态"
date = "2021-08-01 12:34:05"
tags=['zabbix', '监控']
categories=['Zabbix监控']
image = "post/4kdongman/98.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/119296719](https://blog.csdn.net/heian_99/article/details/119296719)

最近公司服务器的一个磁盘出现Read Only，导致数据不可写，但此服务器安装的zabbix监控并未报警，所以针对此情况，新增了监控系统磁盘读写状态的监控。<br> 下面是效果图

![20210801122955191.png](https://img-blog.csdnimg.cn/20210801122955191.png)

![2021080112311067.png](https://img-blog.csdnimg.cn/2021080112311067.png)



如果返回值0代表磁盘都是rw状态可以正常读写，返回值1的话，代表磁盘是ro状态，会报警。<br> 如何实现：

## 目标

使用zabbix监控磁盘ro指标，如果发现ro模式，及时报警

```
mount | grep -v '/sys/fs/cgroup' |awk '{print $NF}' |cut -c 2-3 |awk '{if($1~/ro/) {print 1}}'|wc -l|awk '{if($1&lt;=0) {print 0 } else {print 1}}'
```

使用这个监控所有磁盘，判断是否只读模式

## 修改zabbix_agentd.conf文件

添加

```
UserParameter=check_disk_status,/bin/mount | grep -v '/sys/fs/cgroup' |awk '{print $NF}' |cut -c 2-3 |awk '{if($1~/ro/) {print 1}}'|wc -l|awk '{if($1&lt;=0) {print 0 } else {print 1}}'
```

## 重启zabbix客户端

```
sh startup_zabbix_agentd.sh restart
```

## zabbix服务端添加监控项

![20210801123228748.png](https://img-blog.csdnimg.cn/20210801123228748.png)



## zabbix服务端添加触发器

这个触发器是最近3次检测都出现ro状态，就会报警。

![20210801123240203.png](https://img-blog.csdnimg.cn/20210801123240203.png)



## 测试

![20210801123259362.png](https://img-blog.csdnimg.cn/20210801123259362.png)



![20210801123254588.png](https://img-blog.csdnimg.cn/20210801123254588.png)



## 
