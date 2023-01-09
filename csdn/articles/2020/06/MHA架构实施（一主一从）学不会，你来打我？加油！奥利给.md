+++
author = "南宫乘风"
title = "MHA架构实施（一主一从）学不会，你来打我？加油！奥利给"
date = "2020-06-24 11:43:46"
tags=['mysql', '负载均衡器', 'MHA', '主从复制', '集群']
categories=['MySQL']
image = "post/4kdongman/55.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/106939828](https://blog.csdn.net/heian_99/article/details/106939828)

**目录**



 

[1、环境要求](#1%E3%80%81%E7%8E%AF%E5%A2%83%E8%A6%81%E6%B1%82)

[2、架构工作原理](#2%E3%80%81%E6%9E%B6%E6%9E%84%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86)

[2.1架构介绍:](#2.1%E6%9E%B6%E6%9E%84%E4%BB%8B%E7%BB%8D%3A)

[2.2 MHA软件构成](#2.2%20MHA%E8%BD%AF%E4%BB%B6%E6%9E%84%E6%88%90)

[3、Mysql环境搭建](#3%E3%80%81Mysql%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA)

[3.1环境准备（主从都需要下面步骤）](#3.1%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87%EF%BC%88%E4%B8%BB%E4%BB%8E%E9%83%BD%E9%9C%80%E8%A6%81%E4%B8%8B%E9%9D%A2%E6%AD%A5%E9%AA%A4%EF%BC%89)

[3.2用户的创建处理原始环境](#3.2%E7%94%A8%E6%88%B7%E7%9A%84%E5%88%9B%E5%BB%BA%E5%A4%84%E7%90%86%E5%8E%9F%E5%A7%8B%E7%8E%AF%E5%A2%83)

[3.3解压文件，更改文件目录](#3.3%E8%A7%A3%E5%8E%8B%E6%96%87%E4%BB%B6%EF%BC%8C%E6%9B%B4%E6%94%B9%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95)

[3.4设置环境变量](#3.4%E8%AE%BE%E7%BD%AE%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)

[3.5环境目录规划](#3.5%E7%8E%AF%E5%A2%83%E7%9B%AE%E5%BD%95%E8%A7%84%E5%88%92)

[3.6my.cnf配置文件](#3.6my.cnf%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)

[3.7mysql数据库初始化](#3.7mysql%E6%95%B0%E6%8D%AE%E5%BA%93%E5%88%9D%E5%A7%8B%E5%8C%96)

[3.8启动数据库2种方式](#3.8%E5%90%AF%E5%8A%A8%E6%95%B0%E6%8D%AE%E5%BA%932%E7%A7%8D%E6%96%B9%E5%BC%8F)

[1. sys-v](#1.%20sys-v)

[2. systemd](#2.%20systemd)

[3.9修改数据库的密码](#3.9%E4%BF%AE%E6%94%B9%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9A%84%E5%AF%86%E7%A0%81)

[4、mysql主从配置](#4%E3%80%81mysql%E4%B8%BB%E4%BB%8E%E9%85%8D%E7%BD%AE)

[1、主库创建用户（db01）](#1%E3%80%81%E4%B8%BB%E5%BA%93%E5%88%9B%E5%BB%BA%E7%94%A8%E6%88%B7%EF%BC%88db01%EF%BC%89)

[2、从库开启连接（db02）](#2%E3%80%81%E4%BB%8E%E5%BA%93%E5%BC%80%E5%90%AF%E8%BF%9E%E6%8E%A5%EF%BC%88db02%EF%BC%89)

[5、MHA环境搭建](#5%E3%80%81MHA%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA)

[5.1配置关键程序软连接](#5.1%E9%85%8D%E7%BD%AE%E5%85%B3%E9%94%AE%E7%A8%8B%E5%BA%8F%E8%BD%AF%E8%BF%9E%E6%8E%A5)

[5.2配置各个节点互信](#5.2%E9%85%8D%E7%BD%AE%E5%90%84%E4%B8%AA%E8%8A%82%E7%82%B9%E4%BA%92%E4%BF%A1)

[5.3安装MHA软件](#5.3%E5%AE%89%E8%A3%85MHA%E8%BD%AF%E4%BB%B6)

[1、所有节点安装Node软件依赖包](#1%E3%80%81%E6%89%80%E6%9C%89%E8%8A%82%E7%82%B9%E5%AE%89%E8%A3%85Node%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96%E5%8C%85)

[2、在db01主库中创建mha需要的用户](#2%E3%80%81%E5%9C%A8db01%E4%B8%BB%E5%BA%93%E4%B8%AD%E5%88%9B%E5%BB%BAmha%E9%9C%80%E8%A6%81%E7%9A%84%E7%94%A8%E6%88%B7)

[3、Manager软件安装（db02）](#3%E3%80%81Manager%E8%BD%AF%E4%BB%B6%E5%AE%89%E8%A3%85%EF%BC%88db02%EF%BC%89)

[5.4配置文件准备（db02）](#5.4%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E5%87%86%E5%A4%87%EF%BC%88db02%EF%BC%89)

[5.5状态检查](#5.5%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5)

[互信检查](#%E4%BA%92%E4%BF%A1%E6%A3%80%E6%9F%A5)

[主从状态检查](#%E4%B8%BB%E4%BB%8E%E7%8A%B6%E6%80%81%E6%A3%80%E6%9F%A5)

[5.6开启HMA（db02）](#5.6%E5%BC%80%E5%90%AFHMA%EF%BC%88db02%EF%BC%89)

[开启](#%E5%BC%80%E5%90%AF)

[检测MHA状态](#%E6%A3%80%E6%B5%8BMHA%E7%8A%B6%E6%80%81)

[6、MHA 的vip功能](#6%E3%80%81MHA%20%E7%9A%84vip%E5%8A%9F%E8%83%BD)

[参数](#%E5%8F%82%E6%95%B0)

[修改脚本内容](#%E4%BF%AE%E6%94%B9%E8%84%9A%E6%9C%AC%E5%86%85%E5%AE%B9)

[更改manager配置文件：](#%E6%9B%B4%E6%94%B9manager%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9A)

[主库上，手工生成第一个vip地址](#%E4%B8%BB%E5%BA%93%E4%B8%8A%EF%BC%8C%E6%89%8B%E5%B7%A5%E7%94%9F%E6%88%90%E7%AC%AC%E4%B8%80%E4%B8%AAvip%E5%9C%B0%E5%9D%80)

[重启mha](#%E9%87%8D%E5%90%AFmha)

[7、 binlog server（db02）](#7%E3%80%81%C2%A0binlog%20server%EF%BC%88db02%EF%BC%89)

[参数：](#%E5%8F%82%E6%95%B0%EF%BC%9A)

[创建必要目录](#%E5%88%9B%E5%BB%BA%E5%BF%85%E8%A6%81%E7%9B%AE%E5%BD%95)

[拉取主库binlog日志](#%E6%8B%89%E5%8F%96%E4%B8%BB%E5%BA%93binlog%E6%97%A5%E5%BF%97)

[重启MHA](#%E9%87%8D%E5%90%AFMHA)

[8、邮件提醒](#8%E3%80%81%E9%82%AE%E4%BB%B6%E6%8F%90%E9%86%92)

[1. 参数](#1.%20%E5%8F%82%E6%95%B0)

[2. 准备邮件脚本](#2.%20%E5%87%86%E5%A4%87%E9%82%AE%E4%BB%B6%E8%84%9A%E6%9C%AC)

[3. 修改manager配置文件，调用邮件脚本](#3.%20%E4%BF%AE%E6%94%B9manager%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%8C%E8%B0%83%E7%94%A8%E9%82%AE%E4%BB%B6%E8%84%9A%E6%9C%AC)

[重启MHA](#%E9%87%8D%E5%90%AFMHA)

[9、测试MHA](#9%E3%80%81%E6%B5%8B%E8%AF%95MHA)

[关闭主库,看警告邮件  ](#%E5%85%B3%E9%97%AD%E4%B8%BB%E5%BA%93%2C%E7%9C%8B%E8%AD%A6%E5%91%8A%E9%82%AE%E4%BB%B6%20%C2%A0)

# **<strong><strong>1、环境要求**</strong></strong>



MHA实施文档： [MHA实施文档.pdf-群集服务文档类资源-CSDN下载](https://download.csdn.net/download/heian_99/12548469)

![20200624114048584.png](https://img-blog.csdnimg.cn/20200624114048584.png)

MHA实施软件集合： [MHA实施文档.zip-群集服务文档类资源-CSDN下载](https://download.csdn.net/download/heian_99/12548494)（包含所用到的软件）

![2020062411421623.png](https://img-blog.csdnimg.cn/2020062411421623.png)

![20200624114140888.png](https://img-blog.csdnimg.cn/20200624114140888.png)

**<strong>系统：**</strong>**<strong>CentOS Linux release 7.4.1708 (Core)**</strong>

**<strong>Myssql：5**</strong>**<strong>.7.20**</strong>

**<strong>MHA：**</strong>**<strong>mha4mysql-manager-0.56-0.el6.noarch**</strong>

**<strong>           mha4mysql-node-0.56-0.el6.noarch**</strong>


<td style="vertical-align:top;width:138.25pt;"> **<strong>主机**</strong> </td><td style="vertical-align:top;width:138.25pt;"> **<strong>IP**</strong> </td><td style="vertical-align:top;width:138.3pt;"> **<strong>端口**</strong> </td>

**<strong>IP**</strong>
<td style="vertical-align:top;width:138.25pt;"> **<strong>主库（db**</strong>**<strong>01**</strong>**<strong>）**</strong> </td><td style="vertical-align:top;width:138.25pt;"> **<strong>172.17.1.145**</strong> </td><td style="vertical-align:top;width:138.3pt;"> **<strong>3**</strong>**<strong>306**</strong> </td>

**<strong>172.17.1.145**</strong>
<td style="vertical-align:top;width:138.25pt;"> **<strong>从库（db**</strong>**<strong>02**</strong>**<strong>）**</strong> </td><td style="vertical-align:top;width:138.25pt;"> **<strong>172.17.1.146**</strong> </td><td style="vertical-align:top;width:138.3pt;"> **<strong>3**</strong>**<strong>306**</strong> </td>

**<strong>172.17.1.146**</strong>
<td style="vertical-align:top;width:138.25pt;"> **<strong>虚拟ip（vrrp漂移）**</strong> </td><td style="vertical-align:top;width:138.25pt;"> **<strong>172.17.1.100**</strong> </td><td style="vertical-align:top;width:138.3pt;">  </td>

**<strong>172.17.1.100**</strong>

![2020062411072764.png](https://img-blog.csdnimg.cn/2020062411072764.png)

# **<strong><strong>2、架构工作原理**</strong></strong>

**主库宕机处理过程**

**1. 监控节点 (通过配置文件获取所有节点信息)**

>  
    系统,网络,SSH连接性 
    主从状态,重点是主库 




**2. 选主**

(1) 如果判断从库(position或者GTID),数据有差异,最接近于Master的slave,成为备选主

(2) 如果判断从库(position或者GTID),数据一致,按照配置文件顺序,选主.

(3) 如果设定有权重(candidate_master=1),按照权重强制指定备选主.

>  
     1. 默认情况下如果一个slave落后master 100M的relay logs的话，即使有权重,也会失效. 
     2. 如果check_repl_delay=0的化,即使落后很多日志,也强制选择其为备选主 


**3. 数据补偿**

>  
 (1) 当SSH能连接,从库对比主库GTID 或者position号,立即将二进制日志保存至各个从节点并且应用(save_binary_logs ) 
 (2) 当SSH不能连接, 对比从库之间的relaylog的差异(apply_diff_relay_logs) 


**4. Failover**

将备选主进行身份切换,对外提供服务

其余从库和新主库确认新的主从关系

**5. 应用透明(VIP)**

**6. 故障切换通知(send_reprt)**

**7. 二次数据补偿(binlog_server)**

## **<strong><strong>2**</strong>**<strong>.**</strong>**<strong>1**</strong>**<strong>架构介绍:**</strong></strong>

>  
 1主1从，master：db01   slave：db02 ）： 
 MHA 高可用方案软件构成 
 Manager软件：选择一个从节点安装 
 Node软件：所有节点都要安装 


## **<strong><strong>2**</strong>**<strong>.2 MHA软件构成**</strong></strong>

**anager工具包主要包括以下几个工具：**

>  
 masterha_manger             启动MHA 
 masterha_check_ssh      检查MHA的SSH配置状况 
 masterha_check_repl         检查MySQL复制状况 
 masterha_master_monitor     检测master是否宕机 
 masterha_check_status       检测当前MHA运行状态 
 masterha_master_switch  控制故障转移（自动或者手动） 
 masterha_conf_host      添加或删除配置的server信息 




**Node工具包主要包括以下几个工具：**

**这些工具通常由MHA Manager的脚本触发，无需人为操作**

>  
 save_binary_logs            保存和复制master的二进制日志 
 apply_diff_relay_logs       识别差异的中继日志事件并将其差异的事件应用于其他的 
 purge_relay_logs            清除中继日志（不会阻塞SQL线程） 


# **<strong><strong>3、**</strong>**<strong>Mysql**</strong>**<strong>环境搭建**</strong></strong>



## **<strong><strong>3**</strong>**<strong>.**</strong>**<strong>1环境准备（主从都需要下面步骤）**</strong></strong>

创建目录，上传所需要的文件（主从都需要上传）

```
[root@db01 ~]# mkdir -p /tools/mysql
[root@db01 ~]# cd  /tools/mysql
[root@db01 mysql]# scp * root@172.17.1.146:/tools/mysql/
```

![20200624111039951.png](https://img-blog.csdnimg.cn/20200624111039951.png)

## **<strong><strong>3**</strong>**<strong>.2用户的创建处理原始环境**</strong></strong>

```
[root@db01 ~]# rpm -qa |grep mariadb
[root@db01 ~]# yum remove mariadb-libs-5.5.56-2.el7.x86_64 -y
添加mysql用户
 [root@db01 ~]# useradd -s /sbin/nologin mysql
```

## **<strong><strong>3.3**</strong>**<strong>解压文件，更改文件目录**</strong></strong>

```
存放mysql程序目录
[root@db01 mysql]# mkdir -p /app
解压
[root@db01 mysql]# tar xf mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz 
移动
[root@db01 mysql]# mv mysql-5.7.20-linux-glibc2.12-x86_64 /app/mysql
```

### **<strong><strong>3**</strong>**<strong>.4设置环境变量**</strong></strong>

```

vim /etc/profile

export PATH=/app/mysql/bin:$PATH

[root@db01 ~]# source /etc/profile

[root@db01 ~]# mysql -V

mysql  Ver 14.14 Distrib 5.7.20, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```

![20200624111140925.png](https://img-blog.csdnimg.cn/20200624111140925.png)

## **<strong><strong>3**</strong>**<strong>.5**</strong>**<strong>环境目录规划**</strong></strong>

![20200624111147115.png](https://img-blog.csdnimg.cn/20200624111147115.png)

创建文件，并授权

```
[root@db01 mysql]# 
[root@db01 mysql]# mkdir -p /data/{mysql,binlog}
[root@db01 mysql]# mkdir -p /data/mysql/data
[root@db01 mysql]# chown -R mysql.mysql /app/mysql/*
[root@db01 mysql]# chown -R mysql.mysql /data/*
```

错误日志存放

```
[root@db01 ~]# touch /var/log/mysql.log
[root@db01 ~]# chown mysql.mysql /var/log/mysql.log
[root@db01 ~]# ll /var/log/mysql.log
-rw-r--r-- 1 mysql mysql 0 6月  21 20:38 /var/log/mysql.log
```

Sock环境配置

```
[root@db01 data]# touch /tmp/mysql.sock
[root@db01 data]# chown mysql.mysql /tmp/mysql.sock
```

慢日志（有需要可以加下面参数）

```
开关:
slow_query_log=1 
文件位置及名字 
slow_query_log_file=/data/mysql/slow.log
设定慢查询时间:
long_query_time=0.1
没走索引的语句也记录:
log_queries_not_using_indexes
```

## **<strong><strong>3**</strong>**<strong>.6**</strong>**<strong>my.**</strong>**<strong>cnf**</strong>**<strong>配置文件**</strong></strong>

主库server_id=145

从库server_id=146

```
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
prompt=db01 [\d]&gt;
```

## **<strong><strong>3**</strong>**<strong>.7**</strong>**<strong>mysql数据库初始化**</strong></strong>

```
[root@db01 ~]# mysqld --initialize-insecure --user=mysql --basedir=/app/mysql --datadir=/data/mysql/data
```

## **<strong><strong>3.8**</strong>**<strong>启动数据库2种方式**</strong></strong>

### **<strong><strong>1. sys-v **</strong></strong>

```
[root@db01 data]# cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld 
[root@db01 data]# vim /etc/init.d/mysqld 
[root@db01 data]# grep -Ev "^(#|$)" /etc/init.d/mysqld
 
basedir=/app/mysql
datadir=/data/mysql/data
………………………………………..
```

```
[root@db02 mysql]# service mysqld restart
[root@db02 mysql]# service mysqld stop
[root@db02 mysql]# service mysqld start
```

```
[root@db02 mysql]# /etc/init.d/mysqld restart
[root@db02 mysql]# /etc/init.d/mysqld stop
[root@db02 mysql]# /etc/init.d/mysqld start
```

### **<strong><strong>2. systemd **</strong></strong>

注意： sysv方式启动过的话，需要先提前关闭，才能以下方式登录

```
cat &gt;/etc/systemd/system/mysqld.service &lt;&lt;EOF
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

```
[root@db02 mysql]# systemctl restart mysqld
[root@db02 mysql]# systemctl stop mysqld
[root@db02 mysql]# systemctl start mysqld
```

![20200624111355255.png](https://img-blog.csdnimg.cn/20200624111355255.png)

## **<strong><strong>3**</strong>**<strong>.9**</strong>**<strong>修改数据库的密码**</strong></strong>

**<strong>注意：**</strong>5.8以上数据库，需要先创用户，授权

      5.7的数据库，你授权时，就行给你创建用户

（坑：在更改密码时，要注意空格，防止密码里有空格，而自己没注意

```
use mysql;
本地连接密码
grant all on *.* to root@'localhost' identified by 'xdzh@2020';
同一网段可连接的root权限
grant all on *.* to root@'172.17.1.%' identified by 'xdzh@2020';
刷新权限表
flush privileges;
```

![20200624111429928.png](https://img-blog.csdnimg.cn/20200624111429928.png)

本地登录测试

![20200624111436287.png](https://img-blog.csdnimg.cn/20200624111436287.png)

# **<strong><strong>4、mysql主从配置**</strong></strong>

## **1、主库创建用户（db01<strong><strong>）**</strong></strong>

**<strong>账号密码可以自己定义**</strong>

```
grant replication slave  on *.* to repl@'172.17.1.%' identified by '123';
flush privileges;
```

![20200624111504279.png](https://img-blog.csdnimg.cn/20200624111504279.png)

## **<strong><strong>2、从库开启连接（db**</strong>**<strong>02**</strong>**<strong>）**</strong></strong>

执行语句，连接主库，同步数据

```
change master to 
master_host='172.17.1.145',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;
```

开启从库

```
start slave;
```

![20200624111547326.png](https://img-blog.csdnimg.cn/20200624111547326.png)

查看用户

![20200624111554968.png](https://img-blog.csdnimg.cn/20200624111554968.png)

# **<strong><strong>5、**</strong>**<strong>MHA环境搭建**</strong></strong>

规划
<td style="vertical-align:top;width:207.4pt;"> 主机 </td><td style="vertical-align:top;width:207.4pt;"> MHA软件 </td>

MHA软件
<td style="vertical-align:top;width:207.4pt;"> 主库（db01） </td><td style="vertical-align:top;width:207.4pt;"> Node </td>

Node
<td style="vertical-align:top;width:207.4pt;"> 从库（db02） </td><td style="vertical-align:top;width:207.4pt;"> Node，Master </td>

Node，Master

## **<strong><strong>5**</strong>**<strong>.1**</strong>**<strong>配置关键程序软连接**</strong></strong>

注意：一定要配置，不然后面数据库切换会出现问题（主从都配置）

```
ln -s /app/mysql/bin/mysqlbinlog    /usr/bin/mysqlbinlog
ln -s /app/mysql/bin/mysql          /usr/bin/mysql
```

![20200624111621692.png](https://img-blog.csdnimg.cn/20200624111621692.png)

## **<strong><strong>5**</strong>**<strong>.2**</strong>**<strong>配置各个节点互信**</strong></strong>

配置SSH

```
db01：
rm -rf /root/.ssh 
ssh-keygen
cd /root/.ssh 
mv id_rsa.pub authorized_keys
scp  -r  /root/.ssh  172.17.1.146:/root
```

各节点验证：

```
db01:
ssh 172.17.1.145 date
ssh 172.17.1.146 date

db02:
ssh 172.17.1.145 date
ssh 172.17.1.146 date
```

主库



![20200624111711489.png](https://img-blog.csdnimg.cn/20200624111711489.png)

从库

![20200624111716381.png](https://img-blog.csdnimg.cn/20200624111716381.png)

## **<strong><strong>5**</strong>**<strong>.3**</strong>**<strong>安装MHA软件**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> mha官网：https://code.google.com/archive/p/mysql-master-ha/ github下载地址：https://github.com/yoshinorim/mha4mysql-manager/wiki/Downloads </td>

github下载地址：https://github.com/yoshinorim/mha4mysql-manager/wiki/Downloads

### **<strong><strong>1、**</strong>**<strong>所有节点安装Node软件依赖包**</strong></strong>

```
yum install perl-DBD-MySQL -y
rpm -ivh mha4mysql-node-0.56-0.el6.noarch.rpm
```

![20200624111748709.png](https://img-blog.csdnimg.cn/20200624111748709.png)

### **<strong><strong>2、**</strong>**<strong>在db01主库中创建mha需要的用户**</strong></strong>

账号密码可以自己定义

```
grant all privileges on *.* to mha@'172.17.1.%' identified by 'mha';
```

![20200624111806606.png](https://img-blog.csdnimg.cn/20200624111806606.png)

### **<strong><strong>3、Manager软件安装（db02）**</strong></strong>

注意：这边如果yum安装缺少依赖，换成阿里云的源和epel

```
yum install -y perl-Config-Tiny epel-release perl-Log-Dispatch perl-Parallel-ForkManager perl-Time-HiRes
rpm -ivh mha4mysql-manager-0.56-0.el6.noarch.rpm
```

![20200624111836755.png](https://img-blog.csdnimg.cn/20200624111836755.png)

## **<strong><strong>5**</strong>**<strong>.4**</strong>**<strong>配置文件准备（db**</strong>**<strong>02**</strong>**<strong>）**</strong></strong>

```
创建配置文件目录
 mkdir -p /etc/mha
创建日志目录
 mkdir -p /var/log/mha/app1
```

编辑mha配置文件

```
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



![20200624111906941.png](https://img-blog.csdnimg.cn/20200624111906941.png)

## **<strong><strong>5**</strong>**<strong>.5状态检查**</strong></strong>

```
检测repl状态
masterha_check_repl  --conf=/etc/mha/app1.cnf 
检测ssh状态
masterha_check_ssh  --conf=/etc/mha/app1.cnf

检测运行状态
 masterha_check_status --conf=/etc/mha/app1.cnf
```

### **<strong><strong>互信检查**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> masterha_check_ssh  --conf=/etc/mha/app1.cnf </td>

![20200624111932247.png](https://img-blog.csdnimg.cn/20200624111932247.png)

### **<strong><strong>主从状态检查**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> masterha_check_repl  --conf=/etc/mha/app1.cnf </td>

![20200624111948633.png](https://img-blog.csdnimg.cn/20200624111948633.png)

## **<strong><strong>5**</strong>**<strong>.6**</strong>**<strong>开启HMA（db**</strong>**<strong>02**</strong>**<strong>）**</strong></strong>

### **<strong><strong>开启**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover  &lt; /dev/null&gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp; </td>

### **<strong><strong>检测MHA状态**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> masterha_check_status --conf=/etc/mha/app1.cnf  [root@db02 mysql]# masterha_check_status --conf=/etc/mha/app1.cnf app1 (pid:17248) is running(0:PING_OK), master:172.17.1.145 [root@db02 mysql]# mysql -umha -pmha -h172.17.1.145 -e "show variables like 'server_id'" mysql: [Warning] Using a password on the command line interface can be insecure. +---------------+-------+ | Variable_name | Value | +---------------+-------+ | server_id     | 145   | +---------------+-------+ [root@db02 mysql]# mysql -umha -pmha -h172.17.1.146 -e "show variables like 'server_id'" mysql: [Warning] Using a password on the command line interface can be insecure. +---------------+-------+ | Variable_name | Value | +---------------+-------+ | server_id     | 146   | +---------------+-------+ </td>



app1 (pid:17248) is running(0:PING_OK), master:172.17.1.145

mysql: [Warning] Using a password on the command line interface can be insecure.

| Variable_name | Value |

| server_id     | 145   |

[root@db02 mysql]# mysql -umha -pmha -h172.17.1.146 -e "show variables like 'server_id'"

+---------------+-------+

+---------------+-------+

+---------------+-------+

![20200624112112881.png](https://img-blog.csdnimg.cn/20200624112112881.png)

![20200624112119304.png](https://img-blog.csdnimg.cn/20200624112119304.png)

# **<strong><strong>6**</strong>**<strong>、**</strong>**<strong>MHA 的vip功能**</strong></strong>

## **<strong><strong>参数**</strong></strong>

注意：/usr/local/bin/master_ip_failover，必须事先准备好
<td style="vertical-align:top;width:414.8pt;"> master_ip_failover_script=/usr/local/bin/master_ip_failover </td>

## **<strong><strong>修改脚本内容**</strong></strong>

```
vi  /usr/local/bin/master_ip_failover
my $vip = '172.17.1.100/24';
my $key = '1';
my $ssh_start_vip = "/sbin/ifconfig eth0:$key $vip";
my $ssh_stop_vip = "/sbin/ifconfig eth0:$key down";
```

## **<strong><strong>更改manager配置文件：**</strong></strong>

```
vi /etc/mha/app1.cnf
添加：
master_ip_failover_script=/usr/local/bin/master_ip_failover
注意：
[root@db03 ~]# dos2unix /usr/local/bin/master_ip_failover 
dos2unix: converting file /usr/local/bin/master_ip_failover to Unix format ...
[root@db03 ~]# chmod +x /usr/local/bin/master_ip_failover
```

## **<strong><strong>主库上，手工生成第一个vip地址**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> 手工在主库上绑定vip，注意一定要和配置文件中的ethN一致，我的是eth0:1(1是key指定的值) ifconfig ens33:1 172.17.1.100/24 </td>

ifconfig ens33:1 172.17.1.100/24

![20200624112235903.png](https://img-blog.csdnimg.cn/20200624112235903.png)

## **<strong><strong>重启mha**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> masterha_stop --conf=/etc/mha/app1.cnf nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp; </td>

nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;

# **<strong><strong>7、**</strong>**<strong> binlog server（db02）**</strong></strong>

## **<strong><strong>参数：**</strong></strong>

binlogserver配置：

找一台额外的机器，必须要有5.6以上的版本，支持gtid并开启，我们直接用slave（db02）

vim /etc/mha/app1.cnf

```
[binlog1]
no_master=1
hostname= 172.17.1.146
master_binlog_dir=/data/mysql/binlog
```

![20200624112324531.png](https://img-blog.csdnimg.cn/20200624112324531.png)



## **<strong><strong>创建必要目录**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> mkdir -p /data/mysql/binlog chown -R mysql.mysql /data/* 修改完成后，将主库binlog拉过来（从000001开始拉，之后的binlog会自动按顺序过来） </td>

chown -R mysql.mysql /data/*

## **<strong><strong>拉取主库binlog日志**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> cd /data/mysql/binlog     -----》必须进入到自己创建好的目录 mysqlbinlog  -R --host=172.17.1.145 --user=mha --password=mha --raw  --stop-never mysql-bin.000001 &amp; 注意： 拉取日志的起点,需要按照目前从库的已经获取到的二进制日志点为起点 </td>

mysqlbinlog  -R --host=172.17.1.145 --user=mha --password=mha --raw  --stop-never mysql-bin.000001 &amp;

拉取日志的起点,需要按照目前从库的已经获取到的二进制日志点为起点

![20200624112351686.png](https://img-blog.csdnimg.cn/20200624112351686.png)



## **<strong><strong>重启MHA**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> masterha_stop --conf=/etc/mha/app1.cnf nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp; </td>

nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;

# **<strong><strong>8、邮件提醒**</strong></strong>

## **<strong><strong>1. 参数**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> report_script=/usr/local/bin/send </td>

## **<strong><strong>2. 准备邮件脚本**</strong></strong>

**<strong>send_report**</strong>

>  
 (1)准备发邮件的脚本(上传 email_2019-最新.zip中的脚本，到/usr/local/bin/中) 
 (2)将准备好的脚本添加到mha配置文件中,让其调用 


![20200624112448507.png](https://img-blog.csdnimg.cn/20200624112448507.png)

## **<strong><strong>3. 修改manager配置文件，调用邮件脚本**</strong></strong>

```
vi /etc/mha/app1.cnf
report_script=/usr/local/bin/send
```

## **<strong><strong>重启MHA**</strong></strong>
<td style="vertical-align:top;width:414.8pt;"> masterha_stop --conf=/etc/mha/app1.cnf nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp; </td>

nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover &lt; /dev/null &gt; /var/log/mha/app1/manager.log 2&gt;&amp;1 &amp;

# **<strong><strong>9**</strong>**<strong>、测试MHA**</strong></strong>

## **<strong><strong>关闭主库**</strong>**<strong>,看警告邮件  **</strong></strong>



![2020062411255410.png](https://img-blog.csdnimg.cn/2020062411255410.png)

切换完后，HMA会退出，还有binlogserver

![20200624112607581.png](https://img-blog.csdnimg.cn/20200624112607581.png)

![20200624112627559.png](https://img-blog.csdnimg.cn/20200624112627559.png)

** 145数据库挂掉后，MHA自动切换IP到146上，无需人为修改。**

![2020062411264552.png](https://img-blog.csdnimg.cn/2020062411264552.png)










