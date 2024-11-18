---
author: 南宫乘风
categories:
- MySQL
date: 2019-04-21 22:24:57
description: 使用快照实现物理备份优点：几乎是热备创建快照前把表上锁，创建完后立即释放支持所有存储引擎备份速度快无需使用昂贵的商业软件它是操作系统级别的缺点：可能需要跨部门协调使用操作系统级别的命令，一般没权限无法。。。。。。。
image: ../../title_pic/60.jpg
slug: '201904212224'
tags:
- 技术记录
title: MySQL数据物理备份之lvm快照
---

<!--more-->

# 使用lvm快照实现物理备份

  
  
优点：  
几乎是热备\(创建快照前把表上锁，创建完后立即释放\)  
支持所有存储引擎  
备份速度快  
无需使用昂贵的商业软件\(它是操作系统级别的\)  
缺点：  
可能需要跨部门协调\(使用操作系统级别的命令，DBA一般没权限\)  
无法预计服务停止时间  
数据如果分布在多个卷上比较麻烦\(针对存储级别而言\)  
  
  
操作流程：  
1、flush table with read locak;  
2、create snapshot  
3、show master status;　show slave status;  
4、unlock tables;  
5、copy data from cow to backup  
6、remove snapshot  
 

# 正常安装MySQL：

  
1\. 安装系统  
2\. 准备LVM，例如 /dev/vg\_localhost/lv-mysql，mount /usr/local/mysql  
3\. 源码安装MySQL到 /usr/local/mysql  
  
可选操作：　将现在的数据迁移到LVM  
1\. 准备lvm及文件系统

```
[root@localhost ~]# lvcreate -L 2G -n lv-mysql vg_localhost
[root@localhost ~]# mkfs.ext4 /dev/vg_localhost/lv-mysql
```

  
2\. 将数据迁移到LVM

```
[root@localhost ~]# service mysqld stop
[root@localhost ~]# mount /dev/vg_localhost/lv-mysql /mnt/ //临时挂载点
[root@localhost ~]# rsync -va /usr/local/mysql/ /mnt/ //将MySQL原数据镜像到临时挂载点
```

  
 

```
[root@localhost ~]# umount /mnt/
[root@localhost ~]# mount /dev/vg_localhost/lv-mysql /usr/local/mysql //加入fstab开机挂载
[root@localhost ~]# df -Th
/dev/mapper/vg_localhost-lv--mysql ext4 2.0G 274M 1.7G 15% /usr/local/mysql
[root@localhost ~]# service mysqld start
```

  
 

# 手动基于LVM快照实现备份：

  
1\. 加锁

```
mysql> flush table with read lock;
```

  
2.创建快照

```
# lvcreate -L 500M -s -n lv-mysql-snap /dev/vg_localhost/lv-mysql

# mysql -uroot -p123 -e 'show master status' > /backup/`date +%F`_position.txt

mysql> show master status;
+-------------------+----------+--------------+------------------+-------------------+
| File | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------------+----------+--------------+------------------+-------------------+
| mysqld-bin.000016 | 542 | | | |
+-------------------+----------+--------------+------------------+-------------------+
```

  
  
3\. 释放锁

```
mysql> unlock tables;
```

  
4\. 从快照中备份

```
[root@localhost ~]# mount -o ro /dev/vg_localhost/lv-mysql-snap /mnt/
[root@localhost ~]# mkdir /backup/`date +%F`
[root@localhost ~]# rsync -a /mnt/ /backup/2014-09-02/
```

  
  
5\. 移除快照

```
[root@localhost ~]# umount /mnt/
[root@localhost ~]# lvremove -f /dev/vg_localhost/lv-mysql-snap
```

  
 

## 脚本 + Cron

 

```
#!/bin/bash
#LVM backmysql...
back_dir=/backup/`date +%F`

[ -d $back_dir ] || mkdir -p $back_dir

mysql -uroot -p678 -e 'flush table with read lock'
lvcreate -L 500M -s -n lv-mysql-snap /dev/vg_localhost/lv-mysql
mysql -uroot -p678 -e 'show master status' |grep mysql > $back_dir/position.txt
mysql -uroot -p678 -e 'flush logs'
mysql -uroot -p678 -e 'unlock tables'

mount -o ro /dev/vg_localhost/lv-mysql-snap /mnt/

rsync -a /mnt/ $back_dir

if [ $? -eq 0 ];then
umount /mnt/
lvremove -f /dev/vg_localhost/lv-mysql-snap
fi
```

  
  
  
 

# mylvmbackup

  
功能：利用LVM快照实现物理备份，即LVM快照备份的自动版  
  
安装perl模块  
1\. 在线安装

```
http://www.lenzg.net/mylvmbackup
```

  
它依赖于perl 模块，可用以下命令安装

```
perl -MCPAN -e 'install Config::IniFiles'
```

  
2\. 离线安装

```
# yum -y install atrpms-77-1.noarch.rpm perl-Config-IniFiles-2.72-3.em.el6.noarch.rpm perl-File-Copy-Recursive-0.38-1.el6.rfx.noarch.rpm perl-IO-stringy-2.110-8.el6.noarch.rpm
```

  
安装mylvmbackup软件包

```
# yum -y install mylvmbackup-0.15-0.noarch.rpm
```

  
  
备份方法一：

```
# mylvmbackup --user=root --password=111 --host=localhost --mycnf=/etc/my.cnf --vgname=vg_localhost --lvname=lv-mysql --backuptype=tar --lvsize=100M --backupdir=/
backup
```

  
 

```
[root@localhost backup]# tar xf backup-20140903_000236_mysql.tar.gz
[root@localhost backup]# ls
backup backup-cnf-20140903_000236_mysql
backup-20140903_000236_mysql.tar.gz backup-pos
```

  
  
备份方法二：

```
[root@server ~]# vim /etc/mylvmbackup.conf
[mysql] #连接数据库配置
user=root
password=123456
host=localhost
port=3306
socket=/tmp/mysql.sock
mycnf=/etc/my.cnf
[lvm] #LVM逻辑卷的配置
vgname=vg_server #卷组名称
lvname=lv_mysql #逻辑卷名称
backuplv=mysql_snap #快照卷名称
lvsize=500M
[fs] #文件系统配置
xfs=0
mountdir=/var/tmp/mylvmbackup/mnt/ #挂载目录
backupdir=/backup #备份目录，也可以备份到行程主机
[misc] #定义备份选项
backuptype=tar #定义备份的类型
backupretention=0
prefix=backup #定义备份文件名前缀
suffix=_mysql #定义备份文件名后缀
tararg=cvf #定义tar参数，默认为cvf
tarfilesuffix=.tar.gz #定义备份文件后缀名格式
datefmt=%Y%m%d_%H%M%S #定义备份文件名时间戳格式
keep_snapshot=0 #是否保留snaphot
keep_mount=0 #是否卸载snaphot
quiet=0 #定义记录日志类型
注释：其他配置保持输入即可
```

  
  
然后直接执行mylvmbackup即可