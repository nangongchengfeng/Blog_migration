---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-20 19:56:45
description: 备份类型热备份、温备份、冷备份根据服务器状态热备份：读、写不受影响；温备份：仅可以执行读操作；冷备份：离线备份；读、写操作均中止；物理备份与逻辑备份从对象来分物理备份：复制数据文件；逻辑备份：将数据导。。。。。。。
image: http://image.ownit.top/4kdongman/35.jpg
tags:
- 技术记录
title: MySQL数据备份概述
---

<!--more-->

**MySQL备份类型**  
  
热备份、温备份、冷备份 （根据服务器状态）  
热备份：读、写不受影响；  
温备份：仅可以执行读操作；  
冷备份：离线备份；读、写操作均中止；  
  
物理备份与逻辑备份 （从对象来分）  
物理备份：复制数据文件；  
逻辑备份：将数据导出至文本文件中；  
  
完全备份、增量备份、差异备份 （从数据收集来分）  
完全备份：备份全部数据；  
增量备份：仅备份上次完全备份或增量备份以后变化的数据；  
差异备份：仅备份上次完全备份以来变化的数据；  
  
**MySQL数据备份**  
  
逻辑备份： 备份的是建表、建库、插入等操作所执行SQL语句，适用于中小型数据库，效率相对较低。  
mysqldump  
mydumper  
  
逻辑备份的优点：  
在备份速度上两种备份要取决于不同的存储引擎  
物理备份的还原速度非常快。但是物理备份的最小力度只能做到表  
逻辑备份保存的结构通常都是纯ASCII的，所以我们可以使用文本处理工具来处理  
逻辑备份有非常强的兼容性，而物理备份则对版本要求非常高  
逻辑备份也对保持数据的安全性有保证  
  
逻辑备份的缺点：  
逻辑备份要对RDBMS产生额外的压力，而裸备份无压力  
逻辑备份的结果可能要比源文件更大。所以很多人都对备份的内容进行压缩  
逻辑备份可能会丢失浮点数的精度信息  
  
物理备份： 直接复制数据库文件，适用于大型数据库环境，不受存储引擎的限制，但不能恢复到异构系统中如Windows。  
xtrabackup  
inbackup  
lvm snapshot  
mysqlbackup ORACLE公司也提供了针对企业的备份软件MySQL Enterprise Backup简称  
  
MySQL备份内容  
数据文件日志文件（比如事务日志，二进制日志）  
存储过程，存储函数，触发器  
配置文件（十分重要，各个配置文件都要备份）  
用于实现数据库备份的脚本，数据库自身清理的crontab等……  
  
  
**建议：**

```
# vim /etc/my.cnf
[mysqld]
log-bin=mysql-bin
server-id=1 #5.7 必须配置server-id 启用binlog功能
binlog_format=statement #5.7 默认binlog只记录create、drop和alter，要记录insert语句必须设置格式

datadir = /usr/local/mysql/data　 #添加此行，数据存放目录
innodb_file_per_table = 1         #启用InnoDB独立表空间，默认所有数据库使用一个表空间
# service mysqld restart
```