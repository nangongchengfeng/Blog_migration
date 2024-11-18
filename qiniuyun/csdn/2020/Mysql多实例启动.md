---
author: 南宫乘风
categories:
- MySQL
date: 2020-05-19 17:56:00
description: 目录多实例的应用、准备多个目录、准备配置文件、初始化三套数据、管理多实例、授权、启动、验证多实例下载版本：安装方式：二进制多实例的应用、准备多个目录、准备配置文件安装路径数据存放目录的、初始化三套数据。。。。。。。
image: ../../title_pic/77.jpg
slug: '202005191756'
tags:
- mysql
- linux
- 运维
- 服务器
title: Mysql多实例启动
---

<!--more-->

**目录**

[多实例的应用](#%E5%A4%9A%E5%AE%9E%E4%BE%8B%E7%9A%84%E5%BA%94%E7%94%A8)

[1、准备多个目录](#1%E3%80%81%E5%87%86%E5%A4%87%E5%A4%9A%E4%B8%AA%E7%9B%AE%E5%BD%95)

[2、准备配置文件](#2%E3%80%81%E5%87%86%E5%A4%87%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)

[3、初始化三套数据](#3%E3%80%81%E5%88%9D%E5%A7%8B%E5%8C%96%E4%B8%89%E5%A5%97%E6%95%B0%E6%8D%AE)

[4、systemd管理多实例](#4%E3%80%81systemd%E7%AE%A1%E7%90%86%E5%A4%9A%E5%AE%9E%E4%BE%8B)

[5、授权](#5%E3%80%81%E6%8E%88%E6%9D%83)

[6、启动](#6%E3%80%81%E5%90%AF%E5%8A%A8)

[7、验证多实例](#7%E3%80%81%E9%AA%8C%E8%AF%81%E5%A4%9A%E5%AE%9E%E4%BE%8B)

---

Mysql下载

<https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz>

 

Mysql版本：5.7.26

Mysql安装方式：二进制

 

## 多实例的应用

### 1、准备多个目录

```
mkdir -p /mysql/330{7,8,9}/data
```

 

### 2、准备配置文件

```bash
cat > /mysql/3307/my.cnf <<EOF
[mysqld]
basedir=/application/mysql   #mysql安装路径
datadir=/mysql/3307/data     #mysql数据存放目录
socket=/mysql/3307/mysql.sock  #mysql的socket
log_error=/mysql/3307/mysql.log
port=3307
server_id=7
log_bin=/mysql/3307/mysql-bin
EOF

cat > /mysql/3308/my.cnf <<EOF
[mysqld]
basedir=/application/mysql
datadir=/mysql/3308/data
socket=/mysql/3308/mysql.sock
log_error=/mysql/3308/mysql.log
port=3308
server_id=8
log_bin=/mysql/3308/mysql-bin
EOF

cat > /mysql/3309/my.cnf <<EOF
[mysqld]
basedir=/application/mysql
datadir=/mysql/3309/data
socket=/mysql/3309/mysql.sock
log_error=/mysql/3309/mysql.log
port=3309
server_id=9
log_bin=/mysql/3309/mysql-bin
EOF
```

### 3、初始化三套数据

```bash
mysqld --initialize-insecure  --user=mysql --datadir=/mysql/3307/data --basedir=/application/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/mysql/3308/data --basedir=/application/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/mysql/3309/data --basedir=/application/mysql
```

### 4、systemd管理多实例

```bash
cd /etc/systemd/system
cp mysqld.service mysqld3307.service
cp mysqld.service mysqld3308.service
cp mysqld.service mysqld3309.service

vim mysqld3307.service
ExecStart=/app/mysql/bin/mysqld  --defaults-file=/mysql/3307/my.cnf
vim mysqld3308.service
ExecStart=/app/mysql/bin/mysqld  --defaults-file=/mysql/3308/my.cnf
vim mysqld3309.service
ExecStart=/app/mysql/bin/mysqld  --defaults-file=/mysql/3309/my.cnf
```

 

 

### 5、授权

```bash
chown -R mysql.mysql /mysql/*
```

 

### 6、启动

```bash
systemctl start mysqld3307.service
systemctl start mysqld3308.service
systemctl start mysqld3309.service
```

### 7、验证多实例

```
netstat -lnp|grep 330
mysql -S /mysql/3307/mysql.sock -e "select @@server_id"
mysql -S /mysql/3308/mysql.sock -e "select @@server_id"
mysql -S /mysql/3309/mysql.sock -e "select @@server_id"
```

![](../../image/20200520102625482.png)