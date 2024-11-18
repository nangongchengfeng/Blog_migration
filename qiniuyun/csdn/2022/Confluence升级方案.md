---
author: 南宫乘风
categories:
- 软件
date: 2022-07-04 10:39:47
description: 目前版本的授权信息版权声明；股份有限公司最新版本地址：升级版本选择原地址下载：新地址下载：数据备份生产环境：程序目录：数据目录：数据库：数据备份目标机器数据还原注意：数据库必须使用才行，不然会报数据库。。。。。。。
image: ../../title_pic/50.jpg
slug: '202207041039'
tags:
- java
- 开发语言
title: Confluence升级方案
---

<!--more-->

## Confluence目前版本

Confluence的授权信息  
Confluence 6.9.3  
版权声明； 2003 \- 2018 Atlassian 股份有限公司

![](../../image/a77130ec53334b82a6a1c1daa7b39e90.png)

##  Confluence最新版本

Confluence 7.13.7  
地址：https://www.atlassian.com/zh/software/confluence/download-archives

![](../../image/68dfe15137984fb6919eb252ada6a638.png)

## 升级版本选择

原  Confluence 6.9.3 地址下载：https://product-downloads.atlassian.com/software/confluence/do  
wnloads/atlassian-confluence-6.9.3-x64.bin

新  Confluence 7.13.7 地址下载：https://product-downloads.atlassian.com/software/confluence/d  
ownloads/atlassian-confluence-7.13.7-x64.bin

## 数据备份

生产环境：127.0.0.1  
程序目录：/opt/atlassian  
数据目录：/var/atlassian  
数据库：mysql 5.6

![](../../image/c3e593a2fa1844dba095cafa16c1fb9e.png)

##  mysql数据备份

```bash
cd /opt/mysql_backup
mysqldump -uroot -hlocalhost -p confluence > confluence-20220616.sql
scp confluence-20220616.sql 目标机器
```

## 数据还原

注意：数据库必须使用root 才行，不然会报 数据库触发器失败的错误（错误如下图）

## ![](../../image/3a382943611e4e21926f0c177656203d.png)

```bash
[root@localhost ~]# mysql -u root -p
mysql> CREATE DATABASE IF NOT EXISTS confluence DEFAULT CHARSET utf8 COLLATE 
utf8_general_ci;
mysql> use confluence;
mysql> source /root/confluence-20220616.sql;    #注意，这里需要写入confluence.sql的
绝对路径
```

 修改Confluence配置文件中数据库连接为新数据库

```bash
vi /var/atlassian/application-data/confluence/confluence.cfg.xml
```

## ![](../../image/c40d4c67d99b4292af43791a18047cfb.png)

##  启动Conflucence

```bash
授权
chown -R confluence:confluence /opt/atlassian
chown -R confluence:confluence /var/atlassian
切换用户启动
su confluence
/opt/atlassian/confluence/bin/startup.sh
```

## ![](../../image/9ad51aae5d104ef7ad5689ea73b5df0b.png)

##  版本更新（ 7.13.7）

```bash
开始升级
[root@prometheus-server confluence]# ls
atlassian-confluence-6.9.3-x64.bin  atlassian-confluence-7.13.7-x64.bin
[root@prometheus-server confluence]# ./atlassian-confluence-7.13.7-x64.bin 
```

## ![](../../image/a7046acedd7e4231980bd3a3820c7816.png)

 ![](../../image/76b402923ebe4d7eab63bf4105c3c460.png)

##  访问页面（key失效）

## ![](../../image/1d9b2a8d8dd24fd9b67b25da6e53d7ee.png)

## 进行破解恢复 

 注意：数据库必须使用root 才行，不然会报 数据库触发器失败的错误

```bash
vim confluence.cfg.xml
查询新的server.id
    <property name="confluence.setup.server.id">BJ5V-W7UB-4PO5-2J39</property>
```

![](../../image/0b3fa80d06d74f099a3790f6dacfa550.png)

##  备份jar包破解

```bash
sz /opt/atlassian/confluence/confluence/WEB-INF/lib/atlassian-extras-decoder-v2-
3.4.1.jar
```

![](../../image/da890dcdc2144adba0b8b047ea247c15.png)

 ![](../../image/1474799696ed4e75946f2c27de0cf13d.png)

破解完成的包 上传到其相应目录  进行重启 

![](../../image/b53d045039404c778387807ee26c313e.png)

```bash
[root@prometheus-server ~]# mv atlassian-extras-decoder-v2-3.4.1.jar  
/opt/atlassian/confluence/confluence/WEB-INF/lib/
mv: overwrite ‘/opt/atlassian/confluence/confluence/WEB-INF/lib/atlassian-extras-decoder-v2-3.4.1.jar’? y
```

 ![](../../image/d984601444fa41b2829c9a693eefc894.png)

##  成功测试

新版测试地址（http://127.0.0.1:8090/） 账号和密码 原有的即可登陆

![](../../image/a5ffbafb766f43b8a2b1d83af24ef043.png)