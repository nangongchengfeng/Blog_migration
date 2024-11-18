---
author: 南宫乘风
categories:
- 技术记录
date: 2019-10-26 17:38:01
description: 目录安装教程安装教程介绍的应用场景安装安装安装完毕后，使用下面的命令启动服务进入服务修改默认端口和密码查看进程重启服务器登录服务器登录服务器语法语法安装教程介绍是用语言开发的一个开源的高性能键值对数据。。。。。。。
image: ../../title_pic/63.jpg
slug: '201910261738'
tags:
- 技术记录
title: Redis安装教程
---

<!--more-->

     

**目录**

[                                               ](<#                                               >)

 

[                                            Redis安装教程](<#                                            Redis安装教程>)

[redis介绍](#redis%E4%BB%8B%E7%BB%8D)

[redis的应用场景 ](#redis%E7%9A%84%E5%BA%94%E7%94%A8%E5%9C%BA%E6%99%AF%E2%80%83)

[yum安装redis](#yum%E5%AE%89%E8%A3%85redis)

[安装](#%E5%AE%89%E8%A3%85)

[安装完毕后，使用下面的命令启动redis服务](#%E5%AE%89%E8%A3%85%E5%AE%8C%E6%AF%95%E5%90%8E%EF%BC%8C%E4%BD%BF%E7%94%A8%E4%B8%8B%E9%9D%A2%E7%9A%84%E5%91%BD%E4%BB%A4%E5%90%AF%E5%8A%A8redis%E6%9C%8D%E5%8A%A1)

[进入redis服务](#%E8%BF%9B%E5%85%A5redis%E6%9C%8D%E5%8A%A1)

[修改redis默认端口和密码](#%E4%BF%AE%E6%94%B9redis%E9%BB%98%E8%AE%A4%E7%AB%AF%E5%8F%A3%E5%92%8C%E5%AF%86%E7%A0%81)

[查看Redis进程](#%E6%9F%A5%E7%9C%8BRedis%E8%BF%9B%E7%A8%8B)

[重启redis服务器](#%E9%87%8D%E5%90%AFredis%E6%9C%8D%E5%8A%A1%E5%99%A8)

[                                                          登录Redis服务器](<#                                                          登录Redis服务器>)

[语法](#%E8%AF%AD%E6%B3%95)

[语法](#%E8%AF%AD%E6%B3%95)

---
                                         

 

#                                             Redis安装教程

## redis介绍

**redis是用C语言开发的一个开源的高性能键值对（key-value）数据库。它通过提供多种键值数据类型来适应不同场景下的存储需求，目前为止redis支持的键值数据类型如下字符串、列表（lists）、集合（sets）、有序集合（sorts sets）、哈希表（hashs）**

## redis的应用场景 

- 缓存（数据查询、短连接、新闻内容、商品内容等等）。（最多使用）
- 分布式集群架构中的session分离。
- 聊天室的在线好友列表。
- 任务队列。（秒杀、抢购、12306等等） 
- 应用排行榜。 
- 网站访问统计。 
- 数据过期处理（可以精确到毫秒）

## yum安装redis

### 安装

```
#检查是否有redis yum 源
yum install redis
#下载fedora的epel仓库
yum install epel-release
#安装redis数据库
yum install redis
```

### 安装完毕后，使用下面的命令启动redis服务

```bash
# 启动redis
service redis start
# 停止redis
service redis stop
# 查看redis运行状态
service redis status
# 查看redis进程
ps -ef | grep redis
```

### 进入redis服务

```
# 进入本机redis
redis-cli
# 列出所有key
keys *
```

### 修改redis默认端口和密码

1、打开配置文件

```bash
vi /etc/redis.conf
```

2、修改默认端口，查找 port 6379 修改为相应端口即可

3、修改默认密码，查找 requirepass foobared 将 foobared 修改为你的密码

4、使用配置文件启动 redis

 

```
# 查找Redis配置（注意不是安装目录下的redis.conf）
# 打开第五步设计的Redis配置，默认为：/etc/redis/6379.conf
# 修改配置文件如下几项，其它保持不变
daemonize yes
#bind 127.0.0.1 （注释，不限制IP）
protected-mode no
将 requirepass foobared前的“#”去掉，密码改为你想要设置的密码（我设置为123456）

# 重启服务
[root@172 redis-3.2.11]# service redis_6379 restart
Stopping ...
Redis stopped
Starting Redis server...

# 开放6379端口
firewall-cmd --zone=public --add-port=6379/tcp --permanent
# 重启防火墙，否则开放端口不起作用
firewall-cmd --reload
```

### 查看Redis进程

```
ps -ef|grep redis
```

### 重启redis服务器

```
systemctl restart redis
```

 

##                                                           登录Redis服务器

**Redis 命令用于在 redis 服务上执行操作。**

**要在 redis 服务上执行命令需要一个 redis 客户端。Redis 客户端在我们之前下载的的 redis 的安装包中。**

### 语法

Redis 客户端的基本语法为：

```
$ redis-cli
```

**本地登录**

```
redis-cli
```

![](../../image/20191026172949550.png)

 

如果需要在远程 redis 服务上执行命令，同样我们使用的也是 redis-cli 命令。

### 语法

```
$ redis-cli -h host -p port -a password
```

**远程登录**

```
redis-cli -h 192.168.116.129 -p 6379
192.168.116.129:6379> keys *
1) "hello"
```

![](../../image/20191026173208728.png)