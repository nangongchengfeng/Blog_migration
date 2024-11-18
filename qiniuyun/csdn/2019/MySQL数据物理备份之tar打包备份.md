---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-21 22:28:12
description: 复制数据文件方式，可以使用或、停止服务、备份数据文件、将备份文件拷贝到目标服务器、目标服务器停止服务、解压文件至目标服务器数据文件夹修改权限、目标服务器启动服务测试。。。。。。。
image: ../../title_pic/06.jpg
slug: '201904212228'
tags:
- 技术记录
title: MySQL数据物理备份之tar打包备份
---

<!--more-->

复制数据文件方式，可以使用cp或tar  
  
1、停止服务

```
[root@localhost mysql]# systemctl stop mysqld
[root@localhost mysql]# netstat -lnupt | grep 3306
```

  
2、备份数据文件

```
cd /var/lib/mysql
[root@localhost mysql]# mkdir -p /server/backup
[root@localhost mysql]#tar czf /server/backup/all.`date +%F`.tar.gz *
```

  
  
3、将备份文件拷贝到目标服务器

```
scp /server/backup/all.`date +%F`.tar.gz 192.168.95.12:/tmp
```

  
  
4、目标服务器停止服务

```
# systemctl stop mysqld
```

  
  
5、解压文件至目标服务器数据文件夹

```
# tar xf /tmp/all.tar.gz -C /usr/local/mysql/data
```

  
修改权限

```
# chown -R mysql.mysql /usr/local/mysql/data
```

  
6、目标服务器启动服务测试

```
# systemctl start mysqld
```