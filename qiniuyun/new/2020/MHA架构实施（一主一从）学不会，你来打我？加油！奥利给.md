---
author: 南宫乘风
categories:
- MySQL
date: 2020-06-24 11:43:46
description: 目录、环境要求、环境要求、架构工作原理、架构工作原理架构介绍架构介绍软件构成软件构成软件构成、环境搭建、环境搭建环境准备主从都需要下面步骤环境准备主从都需要下面步骤用户的创建处理原始环境用户的创建处理。。。。。。。
image: http://image.ownit.top/4kdongman/65.jpg
tags:
- mysql
- 负载均衡器
- MHA
- 主从复制
- 集群
title: MHA架构实施（一主一从）学不会，你来打我？加油！奥利给
---

<!--more-->

**目录**

 

[1、环境要求](#1%E3%80%81%E7%8E%AF%E5%A2%83%E8%A6%81%E6%B1%82 "1、环境要求")

[2、架构工作原理](#2%E3%80%81%E6%9E%B6%E6%9E%84%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86 "2、架构工作原理")

[2.1架构介绍:](#2.1%E6%9E%B6%E6%9E%84%E4%BB%8B%E7%BB%8D%3A "2.1架构介绍:")

[2.2 MHA软件构成](<#2.2 MHA软件构成> "2.2 MHA软件构成")

[3、Mysql环境搭建](#3%E3%80%81Mysql%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA "3、Mysql环境搭建")

[3.1环境准备（主从都需要下面步骤）](#3.1%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87%EF%BC%88%E4%B8%BB%E4%BB%8E%E9%83%BD%E9%9C%80%E8%A6%81%E4%B8%8B%E9%9D%A2%E6%AD%A5%E9%AA%A4%EF%BC%89 "3.1环境准备（主从都需要下面步骤）")

[3.2用户的创建处理原始环境](#3.2%E7%94%A8%E6%88%B7%E7%9A%84%E5%88%9B%E5%BB%BA%E5%A4%84%E7%90%86%E5%8E%9F%E5%A7%8B%E7%8E%AF%E5%A2%83 "3.2用户的创建处理原始环境")

[3.3解压文件，更改文件目录](#3.3%E8%A7%A3%E5%8E%8B%E6%96%87%E4%BB%B6%EF%BC%8C%E6%9B%B4%E6%94%B9%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95 "3.3解压文件，更改文件目录")

[3.4设置环境变量](#3.4%E8%AE%BE%E7%BD%AE%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F "3.4设置环境变量")

[3.5环境目录规划](#3.5%E7%8E%AF%E5%A2%83%E7%9B%AE%E5%BD%95%E8%A7%84%E5%88%92 "3.5环境目录规划")

[3.6my.cnf配置文件](#3.6my.cnf%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6 "3.6my.cnf配置文件")

[3.7mysql数据库初始化](#3.7mysql%E6%95%B0%E6%8D%AE%E5%BA%93%E5%88%9D%E5%A7%8B%E5%8C%96 "3.7mysql数据库初始化")

[3.8启动数据库2种方式](#3.8%E5%90%AF%E5%8A%A8%E6%95%B0%E6%8D%AE%E5%BA%932%E7%A7%8D%E6%96%B9%E5%BC%8F "3.8启动数据库2种方式")

[1\. sys-v](<#1. sys-v> "1. sys-v")

[2\. systemd](<#2. systemd> "2. systemd")

[3.9修改数据库的密码](#3.9%E4%BF%AE%E6%94%B9%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9A%84%E5%AF%86%E7%A0%81 "3.9修改数据库的密码")

[4、mysql主从配置](#4%E3%80%81mysql%E4%B8%BB%E4%BB%8E%E9%85%8D%E7%BD%AE "4、mysql主从配置")

[1、主库创建用户（db01）](#1%E3%80%81%E4%B8%BB%E5%BA%93%E5%88%9B%E5%BB%BA%E7%94%A8%E6%88%B7%EF%BC%88db01%EF%BC%89 "1、主库创建用户（db01）")

[2、从库开启连接（db02）](#2%E3%80%81%E4%BB%8E%E5%BA%93%E5%BC%80%E5%90%AF%E8%BF%9E%E6%8E%A5%EF%BC%88db02%EF%BC%89 "2、从库开启连接（db02）")

[5、MHA环境搭建](#5%E3%80%81MHA%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA "5、MHA环境搭建")

[5.1配置关键程序软连接](#5.1%E9%85%8D%E7%BD%AE%E5%85%B3%E9%94%AE%E7%A8%8B%E5%BA%8F%E8%BD%AF%E8%BF%9E%E6%8E%A5 "5.1配置关键程序软连接")

[5.2配置各个节点互信](#5.2%E9%85%8D%E7%BD%AE%E5%90%84%E4%B8%AA%E8%8A%82%E7%82%B9%E4%BA%92%E4%BF%A1 "5.2配置各个节点互信")

[5.3安装MHA软件](#5.3%E5%AE%89%E8%A3%85MHA%E8%BD%AF%E4%BB%B6 "5.3安装MHA软件")

[1、所有节点安装Node软件依赖包](#1%E3%80%81%E6%89%80%E6%9C%89%E8%8A%82%E7%82%B9%E5%AE%89%E8%A3%85Node%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96%E5%8C%85 "1、所有节点安装Node软件依赖包")

[2、在db01主库中创建mha需要的用户](#2%E3%80%81%E5%9C%A8db01%E4%B8%BB%E5%BA%93%E4%B8%AD%E5%88%9B%E5%BB%BAmha%E9%9C%80%E8%A6%81%E7%9A%84%E7%94%A8%E6%88%B7 "2、在db01主库中创建mha需要的用户")

[3、Manager软件安装（db02）](#3%E3%80%81Manager%E8%BD%AF%E4%BB%B6%E5%AE%89%E8%A3%85%EF%BC%88db02%EF%BC%89 "3、Manager软件安装（db02）")

[5.4配置文件准备（db02）](#5.4%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E5%87%86%E5%A4%87%EF%BC%88db02%EF%BC%89 "5.4配置文件准备（db02）")

[5.5状态检查](#5.5%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5 "5.5状态检查")

[互信检查](#%E4%BA%92%E4%BF%A1%E6%A3%80%E6%9F%A5 "互信检查")

[主从状态检查](#%E4%B8%BB%E4%BB%8E%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5 "主从状态检查")

[5.6开启HMA（db02）](#5.6%E5%BC%80%E5%90%AFHMA%EF%BC%88db02%EF%BC%89 "5.6开启HMA（db02）")

[开启](#%E5%BC%80%E5%90%AF "开启")

[检测MHA状态](#%E6%A3%80%E6%B5%8BMHA%E7%8A%B6%E6%80%81 "检测MHA状态")

[6、MHA 的vip功能](<#6、MHA 的vip功能> "6、MHA 的vip功能")

[参数](#%E5%8F%82%E6%95%B0 "参数")

[修改脚本内容](#%E4%BF%AE%E6%94%B9%E8%84%9A%E6%9C%AC%E5%86%85%E5%AE%B9 "修改脚本内容")

[更改manager配置文件：](#%E6%9B%B4%E6%94%B9manager%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9A "更改manager配置文件：")

[主库上，手工生成第一个vip地址](#%E4%B8%BB%E5%BA%93%E4%B8%8A%EF%BC%8C%E6%89%8B%E5%B7%A5%E7%94%9F%E6%88%90%E7%AC%AC%E4%B8%80%E4%B8%AAvip%E5%9C%B0%E5%9D%80 "主库上，手工生成第一个vip地址")

[重启mha](#%E9%87%8D%E5%90%AFmha "重启mha")

[7、 binlog server（db02）](<#7、 binlog server（db02）> "7、 binlog server（db02）")

[参数：](#%E5%8F%82%E6%95%B0%EF%BC%9A "参数：")

[创建必要目录](#%E5%88%9B%E5%BB%BA%E5%BF%85%E8%A6%81%E7%9B%AE%E5%BD%95 "创建必要目录")

[拉取主库binlog日志](#%E6%8B%89%E5%8F%96%E4%B8%BB%E5%BA%93binlog%E6%97%A5%E5%BF%97 "拉取主库binlog日志")

[重启MHA](#%E9%87%8D%E5%90%AFMHA "重启MHA")

[8、邮件提醒](#8%E3%80%81%E9%82%AE%E4%BB%B6%E6%8F%90%E9%86%92 "8、邮件提醒")

[1\. 参数](<#1. 参数> "1. 参数")

[2\. 准备邮件脚本](<#2. 准备邮件脚本> "2. 准备邮件脚本")

[3\. 修改manager配置文件，调用邮件脚本](<#3. 修改manager配置文件，调用邮件脚本> "3. 修改manager配置文件，调用邮件脚本")

[重启MHA](#%E9%87%8D%E5%90%AFMHA "重启MHA")

[9、测试MHA](#9%E3%80%81%E6%B5%8B%E8%AF%95MHA "9、测试MHA")

[关闭主库,看警告邮件  ](<#关闭主库,看警告邮件  > "关闭主库,看警告邮件  ")

---

# ******1、环境要求******

MHA实施文档： [MHA实施文档.pdf-群集服务文档类资源-CSDN下载](https://download.csdn.net/download/heian_99/12548469 "MHA实施文档.pdf-群集服务文档类资源-CSDN下载")

![](http://image.ownit.top/csdn/20200624114048584.png)

MHA实施软件集合： [MHA实施文档.zip-群集服务文档类资源-CSDN下载](https://download.csdn.net/download/heian_99/12548494 "MHA实施文档.zip-群集服务文档类资源-CSDN下载")（包含所用到的软件）

![](http://image.ownit.top/csdn/2020062411421623.png)

![](http://image.ownit.top/csdn/20200624114140888.png)

****系统：********CentOS Linux release 7.4.1708 \(Core\)****

****Myssql：5********.7.20****

****MHA：********mha4mysql-manager-0.56-0.el6.noarch****

****           mha4mysql-node-0.56-0.el6.noarch****

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>主机</strong></strong></p></td><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>IP</strong></strong></p></td><td style="vertical-align:top;width:138.3pt;"><p style="margin-left:0pt;"><strong><strong>端口</strong></strong></p></td></tr><tr><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>主库（db</strong></strong><strong><strong>01</strong></strong><strong><strong>）</strong></strong></p></td><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>172.17.1.145</strong></strong></p></td><td style="vertical-align:top;width:138.3pt;"><p style="margin-left:0pt;"><strong><strong>3</strong></strong><strong><strong>306</strong></strong></p></td></tr><tr><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>从库（db</strong></strong><strong><strong>02</strong></strong><strong><strong>）</strong></strong></p></td><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>172.17.1.146</strong></strong></p></td><td style="vertical-align:top;width:138.3pt;"><p style="margin-left:0pt;"><strong><strong>3</strong></strong><strong><strong>306</strong></strong></p></td></tr><tr><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>虚拟ip（vrrp漂移）</strong></strong></p></td><td style="vertical-align:top;width:138.25pt;"><p style="margin-left:0pt;"><strong><strong>172.17.1.100</strong></strong></p></td><td style="vertical-align:top;width:138.3pt;"><p style="margin-left:0pt;"></p></td></tr></tbody></table>

![](http://image.ownit.top/csdn/2020062411072764.png)

# ******2、架构工作原理******

**主库宕机处理过程**

**1\. 监控节点 \(通过配置文件获取所有节点信息\)**

>    系统,网络,SSH连接性
> 
>    主从状态,重点是主库

**2\. 选主**

\(1\) 如果判断从库\(position或者GTID\),数据有差异,最接近于Master的slave,成为备选主

\(2\) 如果判断从库\(position或者GTID\),数据一致,按照配置文件顺序,选主.

\(3\) 如果设定有权重\(candidate\_master=1\),按照权重强制指定备选主.

>     1. 默认情况下如果一个slave落后master 100M的relay logs的话，即使有权重,也会失效.
> 
>     2. 如果check\_repl\_delay=0的化,即使落后很多日志,也强制选择其为备选主

**3\. 数据补偿**

> \(1\) 当SSH能连接,从库对比主库GTID 或者position号,立即将二进制日志保存至各个从节点并且应用\(save\_binary\_logs \)
> 
> \(2\) 当SSH不能连接, 对比从库之间的relaylog的差异\(apply\_diff\_relay\_logs\)

**4\. Failover**

将备选主进行身份切换,对外提供服务

其余从库和新主库确认新的主从关系

**5\. 应用透明\(VIP\)**

**6\. 故障切换通知\(send\_reprt\)**

**7\. 二次数据补偿\(binlog\_server\)**

## ******2********.********1********架构介绍:******

> 1主1从，master：db01   slave：db02 ）：
> 
> MHA 高可用方案软件构成
> 
> Manager软件：选择一个从节点安装
> 
> Node软件：所有节点都要安装

## ******2********.2 MHA软件构成******

**anager工具包主要包括以下几个工具：**

> masterha\_manger             启动MHA
> 
> masterha\_check\_ssh      检查MHA的SSH配置状况
> 
> masterha\_check\_repl         检查MySQL复制状况
> 
> masterha\_master\_monitor     检测master是否宕机
> 
> masterha\_check\_status       检测当前MHA运行状态
> 
> masterha\_master\_switch  控制故障转移（自动或者手动）
> 
> masterha\_conf\_host      添加或删除配置的server信息

**Node工具包主要包括以下几个工具：**

**这些工具通常由MHA Manager的脚本触发，无需人为操作**

> save\_binary\_logs            保存和复制master的二进制日志
> 
> apply\_diff\_relay\_logs       识别差异的中继日志事件并将其差异的事件应用于其他的
> 
> purge\_relay\_logs            清除中继日志（不会阻塞SQL线程）

# ******3、********Mysql********环境搭建******

## ******3********.********1环境准备（主从都需要下面步骤）******

创建目录，上传所需要的文件（主从都需要上传）

```bash
[root@db01 ~]# mkdir -p /tools/mysql
[root@db01 ~]# cd  /tools/mysql
[root@db01 mysql]# scp * root@172.17.1.146:/tools/mysql/
```

![](http://image.ownit.top/csdn/20200624111039951.png)

## ******3********.2用户的创建处理原始环境******

```bash
[root@db01 ~]# rpm -qa |grep mariadb
[root@db01 ~]# yum remove mariadb-libs-5.5.56-2.el7.x86_64 -y
添加mysql用户
 [root@db01 ~]# useradd -s /sbin/nologin mysql
```

## ******3.3********解压文件，更改文件目录******

```bash
存放mysql程序目录
[root@db01 mysql]# mkdir -p /app
解压
[root@db01 mysql]# tar xf mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz 
移动
[root@db01 mysql]# mv mysql-5.7.20-linux-glibc2.12-x86_64 /app/mysql
```

### ******3********.4设置环境变量******

```bash

vim /etc/profile

export PATH=/app/mysql/bin:$PATH

[root@db01 ~]# source /etc/profile

[root@db01 ~]# mysql -V

mysql  Ver 14.14 Distrib 5.7.20, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```

![](http://image.ownit.top/csdn/20200624111140925.png)

## ******3********.5********环境目录规划******

![](http://image.ownit.top/csdn/20200624111147115.png)

创建文件，并授权

```bash
[root@db01 mysql]# 
[root@db01 mysql]# mkdir -p /data/{mysql,binlog}
[root@db01 mysql]# mkdir -p /data/mysql/data
[root@db01 mysql]# chown -R mysql.mysql /app/mysql/*
[root@db01 mysql]# chown -R mysql.mysql /data/*
```

错误日志存放

```bash
[root@db01 ~]# touch /var/log/mysql.log
[root@db01 ~]# chown mysql.mysql /var/log/mysql.log
[root@db01 ~]# ll /var/log/mysql.log
-rw-r--r-- 1 mysql mysql 0 6月  21 20:38 /var/log/mysql.log
```

Sock环境配置

```bash
[root@db01 data]# touch /tmp/mysql.sock
[root@db01 data]# chown mysql.mysql /tmp/mysql.sock
```

慢日志（有需要可以加下面参数）

```bash
开关:
slow_query_log=1 
文件位置及名字 
slow_query_log_file=/data/mysql/slow.log
设定慢查询时间:
long_query_time=0.1
没走索引的语句也记录:
log_queries_not_using_indexes
```

## ******3********.6********my.********cnf********配置文件******

主库server\_id=145

从库server\_id=146

```bash
[mysqld]
basedir=/data/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
#错误日志
log_error=/var/log/mysql.log
log_timestamps=system
#server_id
server_id=145
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
#GTID
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
# 允许最大连接数
max_connections=200
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
[mysql]
socket=/tmp/mysql.sock
prompt=db01 [\d]>
```

## ******3********.7********mysql数据库初始化******

```bash
[root@db01 ~]# mysqld --initialize-insecure --user=mysql --basedir=/app/mysql --datadir=/data/mysql/data
```

## ******3.8********启动数据库2种方式******

### ******1\. sys-v******

```bash
[root@db01 data]# cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld 
[root@db01 data]# vim /etc/init.d/mysqld 
[root@db01 data]# grep -Ev "^(#|$)" /etc/init.d/mysqld
 
basedir=/app/mysql
datadir=/data/mysql/data
………………………………………..
```

```bash
[root@db02 mysql]# service mysqld restart
[root@db02 mysql]# service mysqld stop
[root@db02 mysql]# service mysqld start
```

```bash
[root@db02 mysql]# /etc/init.d/mysqld restart
[root@db02 mysql]# /etc/init.d/mysqld stop
[root@db02 mysql]# /etc/init.d/mysqld start
```

### ******2\. systemd******

注意： sysv方式启动过的话，需要先提前关闭，才能以下方式登录

```bash
cat >/etc/systemd/system/mysqld.service <<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/app/mysql/bin/mysqld --defaults-file=/etc/my.cnf
LimitNOFILE = 5000
EOF
```

```bash
[root@db02 mysql]# systemctl restart mysqld
[root@db02 mysql]# systemctl stop mysqld
[root@db02 mysql]# systemctl start mysqld
```

![](http://image.ownit.top/csdn/20200624111355255.png)

## ******3********.9********修改数据库的密码******

****注意：****5.8以上数据库，需要先创用户，授权

      5.7的数据库，你授权时，就行给你创建用户

（坑：在更改密码时，要注意空格，防止密码里有空格，而自己没注意

```bash
use mysql;
本地连接密码
grant all on *.* to root@'localhost' identified by 'xdzh@2020';
同一网段可连接的root权限
grant all on *.* to root@'172.17.1.%' identified by 'xdzh@2020';
刷新权限表
flush privileges;
```

![](http://image.ownit.top/csdn/20200624111429928.png)

本地登录测试

![](http://image.ownit.top/csdn/20200624111436287.png)

# ******4、mysql主从配置******

## **1、主库创建用户（db01****）******

****账号密码可以自己定义****

```bash
grant replication slave  on *.* to repl@'172.17.1.%' identified by '123';
flush privileges;
```

![](http://image.ownit.top/csdn/20200624111504279.png)

## ******2、从库开启连接（db********02********）******

执行语句，连接主库，同步数据

```bash
change master to 
master_host='172.17.1.145',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;
```

开启从库

```bash
start slave;
```

![](http://image.ownit.top/csdn/20200624111547326.png)

查看用户

![](http://image.ownit.top/csdn/20200624111554968.png)

# ******5、********MHA环境搭建******

规划

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:207.4pt;"><p style="margin-left:0pt;">主机</p></td><td style="vertical-align:top;width:207.4pt;"><p style="margin-left:0pt;">MHA软件</p></td></tr><tr><td style="vertical-align:top;width:207.4pt;"><p style="margin-left:0pt;">主库（db01）</p></td><td style="vertical-align:top;width:207.4pt;"><p style="margin-left:0pt;">Node</p></td></tr><tr><td style="vertical-align:top;width:207.4pt;"><p style="margin-left:0pt;">从库（db02）</p></td><td style="vertical-align:top;width:207.4pt;"><p style="margin-left:0pt;">Node，Master</p></td></tr></tbody></table>

## ******5********.1********配置关键程序软连接******

注意：一定要配置，不然后面数据库切换会出现问题（主从都配置）

```bash
ln -s /app/mysql/bin/mysqlbinlog    /usr/bin/mysqlbinlog
ln -s /app/mysql/bin/mysql          /usr/bin/mysql
```

![](http://image.ownit.top/csdn/20200624111621692.png)

## ******5********.2********配置各个节点互信******

配置SSH

```bash
db01：
rm -rf /root/.ssh 
ssh-keygen
cd /root/.ssh 
mv id_rsa.pub authorized_keys
scp  -r  /root/.ssh  172.17.1.146:/root
```

各节点验证：

```bash
db01:
ssh 172.17.1.145 date
ssh 172.17.1.146 date

db02:
ssh 172.17.1.145 date
ssh 172.17.1.146 date
```

主库

![](http://image.ownit.top/csdn/20200624111711489.png)

从库

![](http://image.ownit.top/csdn/20200624111716381.png)

## ******5********.3********安装MHA软件******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">mha官网：https://code.google.com/archive/p/mysql-master-ha/</p><p style="margin-left:0pt;">github下载地址：https://github.com/yoshinorim/mha4mysql-manager/wiki/Downloads</p></td></tr></tbody></table>

### ******1、********所有节点安装Node软件依赖包******

```bash
yum install perl-DBD-MySQL -y
rpm -ivh mha4mysql-node-0.56-0.el6.noarch.rpm
```

![](http://image.ownit.top/csdn/20200624111748709.png)

### ******2、********在db01主库中创建mha需要的用户******

账号密码可以自己定义

```bash
grant all privileges on *.* to mha@'172.17.1.%' identified by 'mha';
```

![](http://image.ownit.top/csdn/20200624111806606.png)

### ******3、Manager软件安装（db02）******

注意：这边如果yum安装缺少依赖，换成阿里云的源和epel

```bash
yum install -y perl-Config-Tiny epel-release perl-Log-Dispatch perl-Parallel-ForkManager perl-Time-HiRes
rpm -ivh mha4mysql-manager-0.56-0.el6.noarch.rpm
```

![](http://image.ownit.top/csdn/20200624111836755.png)

## ******5********.4********配置文件准备（db********02********）******

```bash
创建配置文件目录
 mkdir -p /etc/mha
创建日志目录
 mkdir -p /var/log/mha/app1
```

编辑mha配置文件

```bash
vim /etc/mha/app1.cnf

[server default]
manager_log=/var/log/mha/app1/manager        
manager_workdir=/var/log/mha/app1            
master_binlog_dir=/data/binlog       
user=mha                                   
password=mha                               
ping_interval=2
repl_password=123
repl_user=repl
ssh_user=root                               
[server1]                                   
hostname=172.17.1.145
port=3306                                  
[server2]            
hostname=172.17.1.146
port=3306
```

![](http://image.ownit.top/csdn/20200624111906941.png)

## ******5********.5状态检查******

```bash
检测repl状态
masterha_check_repl  --conf=/etc/mha/app1.cnf 
检测ssh状态
masterha_check_ssh  --conf=/etc/mha/app1.cnf

检测运行状态
 masterha_check_status --conf=/etc/mha/app1.cnf
```

### ******互信检查******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">masterha_check_ssh &nbsp;--conf=/etc/mha/app1.cnf</p></td></tr></tbody></table>

![](http://image.ownit.top/csdn/20200624111932247.png)

### ******主从状态检查******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">masterha_check_repl &nbsp;--conf=/etc/mha/app1.cnf</p></td></tr></tbody></table>

![](http://image.ownit.top/csdn/20200624111948633.png)

## ******5********.6********开启HMA（db********02********）******

### ******开启******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &nbsp;&lt; /dev/null&gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;</p></td></tr></tbody></table>

### ******检测MHA状态******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">masterha_check_status --conf=/etc/mha/app1.cnf</p><p style="margin-left:0pt;"></p><p style="margin-left:0pt;">[root@db02 mysql]# masterha_check_status --conf=/etc/mha/app1.cnf</p><p style="margin-left:0pt;">app1 (pid:17248) is running(0:PING_OK), master:172.17.1.145</p><p style="margin-left:0pt;">[root@db02 mysql]# mysql -umha -pmha -h172.17.1.145 -e "show variables like 'server_id'"</p><p style="margin-left:0pt;">mysql: [Warning] Using a password on the command line interface can be insecure.</p><p style="margin-left:0pt;">+---------------+-------+</p><p style="margin-left:0pt;">| Variable_name | Value |</p><p style="margin-left:0pt;">+---------------+-------+</p><p style="margin-left:0pt;">| server_id &nbsp;&nbsp;&nbsp;&nbsp;| 145 &nbsp;&nbsp;|</p><p style="margin-left:0pt;">+---------------+-------+</p><p style="margin-left:0pt;">[root@db02 mysql]# mysql -umha -pmha -h172.17.1.146 -e "show variables like 'server_id'"</p><p style="margin-left:0pt;">mysql: [Warning] Using a password on the command line interface can be insecure.</p><p style="margin-left:0pt;">+---------------+-------+</p><p style="margin-left:0pt;">| Variable_name | Value |</p><p style="margin-left:0pt;">+---------------+-------+</p><p style="margin-left:0pt;">| server_id &nbsp;&nbsp;&nbsp;&nbsp;| 146 &nbsp;&nbsp;|</p><p style="margin-left:0pt;">+---------------+-------+</p></td></tr></tbody></table>

![](http://image.ownit.top/csdn/20200624112112881.png)

![](http://image.ownit.top/csdn/20200624112119304.png)

# ******6********、********MHA 的vip功能******

## ******参数******

注意：/usr/local/bin/master\_ip\_failover，必须事先准备好

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">master_ip_failover_script=/usr/local/bin/master_ip_failover</p></td></tr></tbody></table>

## ******修改脚本内容******

```bash
vi  /usr/local/bin/master_ip_failover
my $vip = '172.17.1.100/24';
my $key = '1';
my $ssh_start_vip = "/sbin/ifconfig eth0:$key $vip";
my $ssh_stop_vip = "/sbin/ifconfig eth0:$key down";
```

## ******更改manager配置文件：******

```bash
vi /etc/mha/app1.cnf
添加：
master_ip_failover_script=/usr/local/bin/master_ip_failover
注意：
[root@db03 ~]# dos2unix /usr/local/bin/master_ip_failover 
dos2unix: converting file /usr/local/bin/master_ip_failover to Unix format ...
[root@db03 ~]# chmod +x /usr/local/bin/master_ip_failover
```

## ******主库上，手工生成第一个vip地址******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">手工在主库上绑定vip，注意一定要和配置文件中的ethN一致，我的是eth0:1(1是key指定的值)</p><p style="margin-left:0pt;">ifconfig ens33:1 172.17.1.100/24</p></td></tr></tbody></table>

![](http://image.ownit.top/csdn/20200624112235903.png)

## ******重启mha******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">masterha_stop --conf=/etc/mha/app1.cnf</p><p style="margin-left:0pt;">nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;</p></td></tr></tbody></table>

# ******7、******** binlog server（db02）******

## ******参数：******

binlogserver配置：

找一台额外的机器，必须要有5.6以上的版本，支持gtid并开启，我们直接用slave（db02）

vim /etc/mha/app1.cnf

```bash
[binlog1]
no_master=1
hostname= 172.17.1.146
master_binlog_dir=/data/mysql/binlog
```

![](http://image.ownit.top/csdn/20200624112324531.png)

## ******创建必要目录******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">mkdir -p /data/mysql/binlog</p><p style="margin-left:0pt;">chown -R mysql.mysql /data/*</p><p style="margin-left:0pt;">修改完成后，将主库binlog拉过来（从000001开始拉，之后的binlog会自动按顺序过来）</p></td></tr></tbody></table>

## ******拉取主库binlog日志******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">cd /data/mysql/binlog &nbsp;&nbsp;&nbsp;&nbsp;-----》必须进入到自己创建好的目录</p><p style="margin-left:0pt;">mysqlbinlog &nbsp;-R --host=172.17.1.145 --user=mha --password=mha --raw &nbsp;--stop-never mysql-bin.000001 &amp;</p><p style="margin-left:0pt;">注意：</p><p style="margin-left:0pt;">拉取日志的起点,需要按照目前从库的已经获取到的二进制日志点为起点</p></td></tr></tbody></table>

![](http://image.ownit.top/csdn/20200624112351686.png)

## ******重启MHA******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">masterha_stop --conf=/etc/mha/app1.cnf</p><p style="margin-left:0pt;">nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;</p></td></tr></tbody></table>

# ******8、邮件提醒******

## ******1\. 参数******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">report_script=/usr/local/bin/send</p></td></tr></tbody></table>

## ******2\. 准备邮件脚本******

****send\_report****

> \(1\)准备发邮件的脚本\(上传 email\_2019-最新.zip中的脚本，到/usr/local/bin/中\)
> 
> \(2\)将准备好的脚本添加到mha配置文件中,让其调用

![](http://image.ownit.top/csdn/20200624112448507.png)

## ******3\. 修改manager配置文件，调用邮件脚本******

```bash
vi /etc/mha/app1.cnf
report_script=/usr/local/bin/send
```

## ******重启MHA******

<table border="1" cellspacing="0"><tbody><tr><td style="vertical-align:top;width:414.8pt;"><p style="margin-left:0pt;">masterha_stop --conf=/etc/mha/app1.cnf</p><p style="margin-left:0pt;">nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;</p></td></tr></tbody></table>

# ******9********、测试MHA******

## ******关闭主库********,看警告邮件  ******

![](http://image.ownit.top/csdn/2020062411255410.png)

切换完后，HMA会退出，还有binlogserver

![](http://image.ownit.top/csdn/20200624112607581.png)

![](http://image.ownit.top/csdn/20200624112627559.png)

** 145数据库挂掉后，MHA自动切换IP到146上，无需人为修改。**

![](http://image.ownit.top/csdn/2020062411264552.png)