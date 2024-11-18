---
author: 南宫乘风
categories:
- 项目实战
date: 2024-07-29 17:11:26
description: 目前公司使用PowerDNS进行DNS管理，但由于采用的是单节点架构，存在不可用的风险。为提升系统的稳定性和可靠性，我们计划对现有架构进行重构。通过引入高可用性设计，我们将优化系统架构，使其能够在故障情况下依然保持服务的连续性和高效性，从而提升整体的业务稳定性。系统：Cnetos7软件：（相关信息已经脱敏）名称ip组件matsernginx，mysql，PowerDNS
  Authoritative ，PowerDNS Recursor   （主）slave。
image: ../../title_pic/52.jpg
slug: '202407291711'
tags:
- 架构
title: PowerDNS架构解析与安装部署指南
---
<!--more-->
## 1、背景介绍
目前公司使用PowerDNS进行DNS管理，但由于采用的是单节点架构，存在不可用的风险。为提升系统的稳定性和可靠性，我们计划对现有架构进行重构。通过引入高可用性设计，我们将优化系统架构，使其能够在故障情况下依然保持服务的连续性和高效性，从而提升整体的业务稳定性。
## 2、环境介绍
系统：Cnetos7
软件：
pdns-4.1.8-1.el7.MIND.x86_64
pdns-recursor-4.1.11-1.el7.MIND.x86_64
（相关信息已经脱敏）


| 名称   | ip           | 组件                                                         |
| ------ | ------------ | ------------------------------------------------------------ |
| matser | 172.17.20.20 | nginx，mysql，PowerDNS Authoritative ，PowerDNS Recursor   （主） |
| slave  | 172.17.20.21 | nginx，mysql，PowerDNS Authoritative ，PowerDNS Recursor      (备) |

nginx（53）：作为upstream 代理 53 端口

mysql（3306）：作为PowerDNS的后端存储

PowerDNS Authoritative（5300）：用于管理企业私有域名

PowerDNS Recursor（5301）： 用于DNS解析转发、缓存



![在这里插入图片描述](../../image/7ac48b5ce4034594a614e1fa76266ac6.png)
## 3、组件介绍
 PowerDNS全家桶中包含PowerDNS Authoritative、Recursor、DNSList（暂不使用）三个组件。 

- PowerDNS Authoritative：DNS权威服务器，用于提供企业私有域名的管理和解析；
- PowerDNS Recursor：DNS递归服务器，用于接受客户端DNS查询请求，并根据目标域转发配置转发到不同的上游DNS服务器进行解析，并对DNS解析记录进行缓存；
- PowerDNS-Admin：DNS权威服务器的Web管理页面；
- PowerDNS-Monitor：使用Grafana提供权威服务器和递归服务器的监控页面


 PowerDNS权威服务器支持多种复制模式，本架构采用MySQL作为后端存储，并通过MySQL复制实现主备数据同步。



PowerDNS（PDNS）成立于20世纪90年代末，是开源DNS软件、服务和支持的主要供应商，它们提供的**权威认证DNS服务器**和**递归认证DNS服务器**都是100%开源的软件，同时也和红帽等开源方案提供商一样提供了付费的技术支持版本。同时官方表示为了避免和软件使用者出现竞争，他们只提供服务支持而不提供DNS托管服务。



熟悉DNS工作原理的同学可以大致地将DNS记录的查询分为两种：**查询本地缓存**和**向上递归查询**。和其他的如BIND、dnsmasq等将这些功能集成到一起的DNS软件不同，PowerDNS将其一分为二，分为了`PowerDNS Authoritative Server`和`PowerDNS Recursor`，分别对应这两种主要的需求，而我们常说的`pdns`指的就是`PowerDNS Authoritative Server (后面简称PDNS Auth)`，主要用途就是作为**权威域名服务器**，当然也可以作为普通的DNS服务器提供DNS查询功能。 

对于PowerDNS-Recursor，PowerDNS官网介绍其是一个**内置脚本能力**的高性能的**DNS递归查询**服务器，并且已经为一亿五千万个互联网连接提供支持。
![在这里插入图片描述](../../image/a37b97ccff3e4f32995266159db67265.jpeg)
## 4、MySQL安装
可参照博客安装 ：  https://blog.csdn.net/heian_99/article/details/106644755
### MySQL主从同步
#### master创建账号

```bash
grant replication slave  on *.* to repl@'172.17.20.%' identified by '123';
flush privileges;
show master status; #查询master的状态 ，进行同步
```
![在这里插入图片描述](../../image/247cf37487994935b17a9621e53e621c.png)
#### slave库同步

注意：主从库的server_id 不能设置一样，auto.cnf 设置也不能一样，不满会出现mysql主从同步失败的

```bash
mysql> change master to master_host='172.17.20.20′,master_user='repl',master_password='123',master_log_file='mysql-bin.000006′,master_log_pos=407;

CHANGE MASTER TO
MASTER_HOST='172.17.20.20',
MASTER_PORT=3306,
MASTER_USER='repl',
MASTER_PASSWORD='123',
MASTER_LOG_FILE='mysql-bin.000006',
MASTER_LOG_POS=407;


mysql> start slave;

mysql> show slave status\G
```
![在这里插入图片描述](../../image/7b0271af28654650a2350f4b872a9390.png)
#### 创建**powerdns**数据库
需要在主从配置完成后创建

在主库执行以下命令

```bash
mysql -uroot -p
CREATE DATABASE powerdns;
GRANT ALL ON powerdns.* TO 'powerdns'@'localhost' IDENTIFIED BY 'VMware1!';
FLUSH PRIVILEGES;
```
![在这里插入图片描述](../../image/05d49e35b8ad43379338ac995ecbeb85.png)
导入PowerDNS 的数据库

```sql
CREATE TABLE domains (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255) NOT NULL,
  master                VARCHAR(128) DEFAULT NULL,
  last_check            INT DEFAULT NULL,
  type                  VARCHAR(6) NOT NULL,
  notified_serial       INT DEFAULT NULL,
  account               VARCHAR(40) CHARACTER SET 'utf8' DEFAULT NULL,
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET 'latin1';

CREATE UNIQUE INDEX name_index ON domains(name);


CREATE TABLE records (
  id                    BIGINT AUTO_INCREMENT,
  domain_id             INT DEFAULT NULL,
  name                  VARCHAR(255) DEFAULT NULL,
  type                  VARCHAR(10) DEFAULT NULL,
  content               VARCHAR(64000) DEFAULT NULL,
  ttl                   INT DEFAULT NULL,
  prio                  INT DEFAULT NULL,
  change_date           INT DEFAULT NULL,
  disabled              TINYINT(1) DEFAULT 0,
  ordername             VARCHAR(255) BINARY DEFAULT NULL,
  auth                  TINYINT(1) DEFAULT 1,
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET 'latin1';

CREATE INDEX nametype_index ON records(name,type);
CREATE INDEX domain_id ON records(domain_id);
CREATE INDEX ordername ON records (ordername);


CREATE TABLE supermasters (
  ip                    VARCHAR(64) NOT NULL,
  nameserver            VARCHAR(255) NOT NULL,
  account               VARCHAR(40) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (ip, nameserver)
) Engine=InnoDB CHARACTER SET 'latin1';


CREATE TABLE comments (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  name                  VARCHAR(255) NOT NULL,
  type                  VARCHAR(10) NOT NULL,
  modified_at           INT NOT NULL,
  account               VARCHAR(40) CHARACTER SET 'utf8' DEFAULT NULL,
  comment               TEXT CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET 'latin1';

CREATE INDEX comments_name_type_idx ON comments (name, type);
CREATE INDEX comments_order_idx ON comments (domain_id, modified_at);


CREATE TABLE domainmetadata (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  kind                  VARCHAR(32),
  content               TEXT,
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET 'latin1';

CREATE INDEX domainmetadata_idx ON domainmetadata (domain_id, kind);


CREATE TABLE cryptokeys (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  flags                 INT NOT NULL,
  active                BOOL,
  content               TEXT,
  PRIMARY KEY(id)
) Engine=InnoDB CHARACTER SET 'latin1';

CREATE INDEX domainidindex ON cryptokeys(domain_id);


CREATE TABLE tsigkeys (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255),
  algorithm             VARCHAR(50),
  secret                VARCHAR(255),
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET 'latin1';

CREATE UNIQUE INDEX namealgoindex ON tsigkeys(name, algorithm);

```
创建文件导入数据库

```bash
touch /opt/schema.mysql.sql
把mysql的内容写到这个文件里面
mysql> use powerdns
Database changed
mysql> source /opt/schema.mysql.sql
Query OK, 0 rows affected (0.01 sec)
```
![在这里插入图片描述](../../image/67cd31b12c634c51a38566efcecf0cbc.png)
## 5、PowerDNS Authoritative Server安装

- 参考官网文档：[https://doc.powerdns.com/authorit文章来源(Source)：https://www.dqzboy.comative/installation.html](https://www.dqzboy.com/go.php?url=https://doc.powerdns.com/authoritative/installation.html)
- PowerDNS已经集成到`epel`源中，所以我们首先需要安装`elel源`

```bash
[root@localhost ~]# wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
 
[root@localhost ~]# rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
 
[root@localhost ~]# yum clean all 
[root@localhost ~]# yum makecache
[root@localhost ~]# yum install -y pdns pdns-backend-mysql
```
![在这里插入图片描述](../../image/575ecca4163945cbaf4c69a7c18dcfd5.png)

### 修改配置文件
`/etc/pdns/pdns.conf `

```bash
[root@master ~]# cp /etc/pdns/pdns.conf /etc/pdns/pdns.conf_`date '+%Y_%m_%d'`
[root@master ~]# tree /etc/pdns/
/etc/pdns/
└── pdns.conf

0 directories, 1 file

[root@master ~]# cat /etc/pdns/pdns.conf |  grep -Ev "^#|^$"
launch=bind
setgid=pdns
setuid=pdns


添加配置 生产环境如下

###############

cache-ttl=60
config-dir=/etc/pdns
disable-axfr=yes
distributor-threads=3
#数据库的连接信息
gmysql-dbname=powerdns
gmysql-host=127.0.0.1
gmysql-password=VMware1!
gmysql-user=powerdns
guardian=no
launch=gmysql
## pdns config 本地地址和启动端口
local-address=127.0.0.1
local-port=5300
log-dns-details=no
disable-syslog=no
negquery-cache-ttl=60
query-cache-ttl=60
query-logging=no
receiver-threads=12
cache-ttl=0
setuid=pdns
setgid=pdns
## pdns API   激活 API 服务
api-key=3jEkItlrSHfuqJbr
api=yes
#web页面也信息
webserver-address=0.0.0.0
webserver-password=bdata.pdns
# webserver-allow-from指定允许访问webserver和API的IP白名单，多个IP可以使用英文逗号隔开
webserver-allow-from=0.0.0.0/0
webserver-port=8281
webserver=yes
loglevel=9



```
### 启动Pdns服务

```bash
[root@master pdns]# systemctl enable pdns
Created symlink from /etc/systemd/system/multi-user.target.wants/pdns.service to /usr/lib/systemd/system/pdns.service.

[root@master pdns]# systemctl start pdns.service
[root@master pdns]# systemctl status pdns.service
```
![在这里插入图片描述](../../image/a2b861cc1ef843ca9631728c1e6ed3fe.png)
## 6、PowerDNS Recursor安装

```bash
[root@master pdns]# yum install pdns-recursor -y
```
### 修改配置文件
` /etc/pdns-recursor/recursor.conf `

```bash
[root@master pdns]# tree /etc/pdns-recursor/
/etc/pdns-recursor/
└── recursor.conf

[root@master pdns]# cp /etc/pdns-recursor/recursor.conf /etc/pdns-recursor/recursor.conf_`date '+%Y_%m_%d'`

[root@master pdns]# cat /etc/pdns-recursor/recursor.conf | grep  -Ev "^#|^$"
security-poll-suffix=
setgid=pdns-recursor
setuid=pdns-recursor


添加配置 生产环境如下

###############

#允许所有用户端请求
allow-from=0.0.0.0/0,::/0
## pdns-re API   激活 API 服务
api-key=3jEkItlrSHfuqJbr

disable-packetcache=no
export-etc-hosts=yes
#用户解析的自定义配置文件   与forward-zones相同，从文件中解析
forward-zones-file=/etc/pdns-recursor/forward
#/etc/hosts 文件的路径或等效文件。该文件可用于使用export-etc-hosts权威地提供数据。
etc-hosts-file=/etc/pdns-recursor/hosts
#本地监听地址
local-address=0.0.0.0
local-port=5301
max-cache-entries=1000000
max-cache-ttl=60
max-mthreads=1024
max-packetcache-entries=500000
packetcache-servfail-ttl=0
packetcache-ttl=0
quiet=yes
setgid=pdns-recursor
setuid=pdns-recursor
threads=6
#web页面也信息
webserver-address=0.0.0.0
webserver-password=bdata.pdns
webserver-port=8282
webserver-allow-from=172.17.0.0/16
webserver=yes
loglevel=9

```
### 创建forward 和hosts 文件
#### 1. Forward 配置

`forward` 配置用于指定 PowerDNS 在无法解析某个 DNS 请求时，将请求转发给其他上游 DNS 服务器进行解析。这在多种情况下都很有用，比如公司内部网络中的 DNS 服务器需要解析外部互联网域名时。

 主要用途：

- **外部解析**：如果本地 DNS 服务器没有相应的记录，可以通过 forward 配置将请求转发给公共 DNS 服务器，如 Google DNS（8.8.8.8）。
- **负载均衡和冗余**：可以配置多个上游 DNS 服务器，提高解析请求的成功率和响应速度。

 配置示例：

```plaintext
forward-zones=.=8.8.8.8;8.8.4.4
```

上面的示例表示将所有（`.` 代表所有域名）未解析的请求转发给 Google 的 DNS 服务器。

#### 2. Hosts 文件

`hosts` 文件是一个静态的 DNS 记录文件，用于手动定义特定域名的 IP 地址。这类似于传统的 `/etc/hosts` 文件，用于快速、本地化地解析一些常用或特定的域名，而无需通过外部 DNS 服务器。

 主要用途：

- **本地解析**：快速解析常用域名，避免每次都去查询外部 DNS。
- **自定义解析**：为本地网络设备或特定服务自定义域名解析记录。
- **简化开发和测试**：开发和测试环境中，直接在 hosts 文件中添加记录，方便快捷。

 配置示例：

假设 `hosts` 文件内容如下：

```plaintext
192.168.1.1   server1.local
192.168.1.2   server2.local
```

这表示将 `server1.local` 解析为 `192.168.1.1`，将 `server2.local` 解析为 `192.168.1.2`。

#### 总结

- **Forward 配置**：用于指定 PowerDNS 在无法解析请求时，将请求转发给其他上游 DNS 服务器，确保解析的成功率和速度。
- **Hosts 文件**：用于手动定义特定域名的 IP 地址，实现本地化、静态的 DNS 解析。

通过合理配置和使用 `forward` 和 `hosts` 文件，可以大大提升 PowerDNS 系统的灵活性和解析效率，满足各种不同的网络需求。


```bash
touch {forward,hosts}
```
![在这里插入图片描述](../../image/51758a743ea4400ba452377dec6453b9.png)
借鉴配置

```bash
[root@prometheus-server pdns-recursor]# cat forward 
+fjf.com=127.0.0.1:5300
+sit.com=127.0.0.1:5300
+fjf=127.0.0.1:5300
+cloudcs.fjf=172.31.0.10
+168.192.in-addr.arpa=127.0.0.1:5300
+30.172.in-addr.arpa=172.31.0.10
+31.172.in-addr.arpa=172.31.0.10
+.=223.5.5.5,223.6.6.6,119.29.29.29
```

```bash
[root@prometheus-server pdns-recursor]# cat hosts 
192.168.82.22   mvn.test.com
192.168.84.47   gitlab.test.com
192.168.81.11   mirrors.test.cn
192.168.82.22   img.test.cn 
192.168.82.22  test.xxx.com
```

### 启动Pdns-recursor

```bash
[root@master pdns-recursor]# systemctl enable pdns-recursor.service
Created symlink from /etc/systemd/system/multi-user.target.wants/pdns-recursor.service to /usr/lib/systemd/system/pdns-recursor.service.

[root@master pdns-recursor]# systemctl start  pdns-recursor
[root@master pdns-recursor]# systemctl status pdns-recursor.service 
```
![在这里插入图片描述](../../image/caa8830216094784befb1bc79c596cb3.png)

## 7、PowerAdmin安装

```bash
wget https://nchc.dl.sourceforge.net/project/poweradmin/poweradmin-2.1.7.tgz
yum -y install php56u php56u-fpm php56u-fpm  tengine php56u-mcrypt php56u-pdo  php56u-soap  php56u-mysqlnd 
https://linux.cn/article-5623-2.html        #跟随此连接安装即可
```
安装步骤

```bash
打开浏览器 ，打开页面
http://172.17.20.20:90/install/
```
![在这里插入图片描述](../../image/c4cbecd71c0844a1882c08479cfbf2e0.png)
![在这里插入图片描述](../../image/67eb9fcef6bc464686cc0a02771ed51e.png)
![在这里插入图片描述](../../image/ad3d702cfe00420bbc44a63e1227db8c.png)
![在这里插入图片描述](../../image/a23a3a4ad55743128d3c2cc2b77121ea.png)
![在这里插入图片描述](../../image/39500702c36b4774a2e431f8c47627df.png)
![在这里插入图片描述](../../image/5269f94d449e4fd98572277bec1e7007.png)
![在这里插入图片描述](../../image/b4f2a90f989c4ee1afdef0273169e777.png)
![在这里插入图片描述](../../image/a5a2266891f34cabac099bfc55dcbfe7.png)
![在这里插入图片描述](../../image/13b5bd7349b74b98b707470826c6d81f.png)
**需要移除从PowerAdmin的根目录中移除“install”文件夹，这一点很重要。使用以下命令：**
![在这里插入图片描述](../../image/ef56178ab9d6448aa7e5b93b15cec064.png)
![在这里插入图片描述](../../image/70cbd806172f4a5f83deb9a663741b74.png)
### 添加主域名![在这里插入图片描述](../../image/105b3d51c441434cb0d5fe60d46548e7.png)
###  添加子域名
![在这里插入图片描述](../../image/1ec2f3e6f3d04448b3ecfb6170cf305d.png)
## 8、成功测试

```bash
[root@master pdns-recursor]# cat /etc/resolv.conf 
# Generated by NetworkManager
nameserver 172.17.20.20
[root@master pdns-recursor]# nslookup www.fjf.com
Server:		172.17.20.20
Address:	172.17.20.20#53

Non-authoritative answer:
Name:	www.fjf.com
Address: 172.17.20.21

[root@master pdns-recursor]# nslookup test.fjf.com
Server:		172.17.20.20
Address:	172.17.20.20#53

Non-authoritative answer:
Name:	test.fjf.com
Address: 172.17.20.21

[root@master pdns-recursor]# nslookup 112.efoxconn.com
Server:		172.17.20.20
Address:	172.17.20.20#53

Non-authoritative answer:
Name:	112.efoxconn.com
Address: 10.134.192.116
```
## 9、备服务器同上步骤
备份服务器 按照上面配置，可以进行安装 和配置文件scp

```bash
yum install -y pdns pdns-backend-mysql
 yum install pdns-recursor -y
 
 
 
[root@master pdns-recursor]# scp -r /etc/pdns/*  172.17.20.21:/etc/pdns/
[root@master pdns-recursor]# scp -r /etc/pdns-recursor/* 172.17.20.21:/etc/pdns-recursor/

[root@slave pdns]# systemctl start pdns &&systemctl status pdns
[root@slave pdns]# systemctl start pdns-recursor && systemctl status pdns-recursor.service 

[root@slave pdns]# systemctl enable pdns && systemctl enable pdns-recursor
```

## 10、nginx负载均衡
安装nginx

```bash
yum install -y nginx
```

把这个配置加入 nginx.conf 后面

```bash

stream {
    # 添加socket转发的代理
	upstream dns {
    server 172.17.20.21:5301 max_fails=3 fail_timeout=3s;
    server 172.17.20.21:5301 max_fails=3 fail_timeout=3s;
	}

    # 提供转发的服务，即访问localhost:30001，会跳转至代理bss_num_socket指定的转发地址
	server {
    listen 53 udp;
    proxy_pass dns;
    proxy_timeout 3s;
    proxy_connect_timeout 3s;
	}
}



```
![在这里插入图片描述](../../image/077a6d2f9ce34468944e06e5a7204671.png)

```bash
[root@master ~]# netstat -ltunp |grep 53
tcp        0      0 127.0.0.1:5300          0.0.0.0:*               LISTEN      39851/pdns_server   
tcp        0      0 0.0.0.0:53              0.0.0.0:*               LISTEN      41809/nginx: master 
tcp        0      0 0.0.0.0:5301            0.0.0.0:*               LISTEN      40930/pdns_recursor 
tcp6       0      0 :::5300                 :::*                    LISTEN      39851/pdns_server   
udp        0      0 127.0.0.1:5300          0.0.0.0:*                           39851/pdns_server   
udp        0      0 0.0.0.0:5301            0.0.0.0:*                           40930/pdns_recursor 
udp        0      0 0.0.0.0:53              0.0.0.0:*                           41809/nginx: master 
udp6       0      0 :::5300                 :::*                                39851/pdns_server   
```
备份服务器的nginx也如上配置即可
