---
author: 南宫乘风
categories:
- Linux实战操作
date: 2021-11-19 23:13:08
description: 目前集群机器比较多，因为下载业务比较多，网络状态不好监控，涉及的状态比较多。有几次出问题，对方的锅，还要扔给我们。有必要做一下监控。防止背锅目前业务方式是把日志写入本地，到时间那台有问题，再去分析那一。。。。。。。
image: ../../title_pic/15.jpg
slug: '202111192313'
tags:
- linux
- docker
- k8s
title: Rsyslog同步集群服务器的网络连接状态
---

<!--more-->

目前集群机器比较多，因为下载业务比较多，网络状态不好监控，涉及的状态比较多。有几次出问题，对方的锅，还要扔给我们。有必要做一下监控。防止背锅

目前业务方式是把日志写入本地，到时间那台有问题，再去分析那一台。

我一看，这还的行吗。如果出问题业务量大，分析半天能累死人，太累了，不太建议。

看来的拿出来看家本领，好歹也是管理过上K台机器的菜鸡，还是有点方法的。

（1）使用脚本分析本地网络的问题

（2）写入rsyslog

（3）使用rsyslog的同步，把日志接入一台机器

（4）然后把数据接入elk，使用可视化界面操作（逼格是否一下上来了）

# 1、分析网络的脚本

```bash
[heian@game ~]$ netstat -n | awk '/^tcp/ {print $0}'  | awk '{print $(NF-1),$NF}' |  awk -F ':| ' '{print $1,$NF}' |awk  '{a[$1" "$2]++}END{for(i in a)print i,a[i]}' |sort -nk 3
10.10.10.3 ESTABLISHED 1
127.0.0.1 ESTABLISHED 6
172.18.0.2 ESTABLISHED 1
192.168.1.100 ESTABLISHED 6
192.168.1.15 ESTABLISHED 6
192.168.1.210 ESTABLISHED 1
```

脚本实现，把数据写入rsyslog

```bash
[root@game heian]# cat tcp_listen.sh 
#!/bin/bash
date_time=`date +"%Y%m%d%H%M"`
today=`date +"%Y-%m-%d"`
date_hour=`date +"%Y-%m-%d_%H"`
log_dir="/app/bighead/scripts/monitorNetstat_log"
log_path=$log_dir/$today/${date_hour}.log

#检查文件夹是否存在，不存在则创建
[ ! -d $log_dir/$today ] && mkdir -p $log_dir/$today
#获取数据
netstat -n | awk '/^tcp/ {print $0}'  | awk '{print $(NF-1),$NF}' |  awk -F ':| ' '{print $1,$NF}' |awk -v date_time=$date_time '{a[$1" "$2]++}END{for(i in a)print date_time,i,a[i]}' |sort -nk 4 >> $log_path
tcp_listen2=$(netstat -n | awk '/^tcp/ {print $0}'  | awk '{print $(NF-1),$NF}' |  awk -F ':| ' '{print $1,$NF}' |awk  '{a[$1" "$2]++}END{for(i in a)print i,a[i]}' |sort -nk 3)
#写入本地文件 
while read tcp
do 
  echo "$tcp"
  logger -p local5.info  "$tcp"
done <<< "$tcp_listen2"

#删除5天前的文件夹
[ -d $log_dir ] && find $log_dir -type d -mtime +5 | xargs rm -rf
```

此脚本会把数据在本地保存一份，也会把数据写入rsyslog

为什么要这么做，防止rsyslog服务器宕机，数据丢失喽（别说，考虑全面点）

# 2、分发脚本，执行定时任务

把这个脚本分发到集群机器上，设置定时任务，10分钟执行一次，会同步一次网络状态。

至于分发，和执行命令创建，ansible喽，自己写了命令，一个copy 一个cron 两个命令搞定

```bash

#大致这格式
ansible p3 -m copy -a "src=/root/node_monitor dest=/root"
ansible p3 -m shell -a "chmod a+x /root/node_monitor/*" -f 10
ansible p3 -m cron -a "minute=* hour=* day=* month=* weekday=* name='chia' job='/usr/bin/python3 /root/node_monitor/node_monitor.py' user='root' state='present'"
```

# 3、同步集群网络状态到rsyslog

## **rsyslog 服务器配置**

```bash
[root@jenkins ~]# cat /etc/rsyslog.conf 
$ModLoad imuxsock # provides support for local system logging (e.g. via logger command)
$ModLoad imklog   # provides kernel logging support (previously done by rklogd)
$ModLoad imudp
$UDPServerRun 514
$ModLoad imtcp
$InputTCPServerRun 514
$template myFormat,"%timestamp:::date-rfc3339% %fromhost-ip% %HOSTNAME%  [%programname%] %syslogseverity-text%:%msg%\n"
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
$IncludeConfig /etc/rsyslog.d/*.conf
*.info;mail.none;authpriv.none;cron.none                /var/log/messages;myFormat
authpriv.*                                              /var/log/secure;myFormat
mail.*                                                  -/var/log/maillog
cron.*                                                  /var/log/cron
*.emerg                                                 :omusrmsg:*
uucp,news.crit                                          /var/log/spooler
local7.*                                                /var/log/boot.log
local5.*                                                /var/log/history/tcp.log;myFormat
#将local类型5的日志存放到 /var/log/history/tcp.log下 使用myFormat模板
```

## **rsyslog 客户端配置**

```bash
[heian@game ~]$ cat  /etc/rsyslog.conf  | grep -Ev "^$|^#"
$ModLoad imuxsock # provides support for local system logging (e.g. via logger command)
$ModLoad imjournal # provides access to the systemd journal
$WorkDirectory /var/lib/rsyslog
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
$IncludeConfig /etc/rsyslog.d/*.conf
$OmitLocalLogging on
$IMJournalStateFile imjournal.state
*.info;mail.none;authpriv.none;cron.none                /var/log/messages
authpriv.*                                              /var/log/secure
mail.*                                                  -/var/log/maillog
cron.*                                                  /var/log/cron
*.emerg                                                 :omusrmsg:*
uucp,news.crit                                          /var/log/spooler
local7.*                                                /var/log/boot.log
*.* @@192.168.1.210
#主要是最后一行啊啊啊啊啊啊啊啊啊，注意
```

配置文件后，记得重启客户端啊

# 4、查看日志

```bash
[root@jenkins history]# pwd
/var/log/history
[root@jenkins history]# ls
tcp.log
[root@jenkins history]# cat tcp.log |wc -l
28
[root@jenkins history]# tail -f tcp.log 
2021-11-19T16:32:21+08:00 192.168.1.100 game  [heian] info: 172.18.0.2 ESTABLISHED 1
2021-11-19T16:32:21+08:00 192.168.1.100 game  [heian] info: 192.168.1.100 ESTABLISHED 6
2021-11-19T16:32:21+08:00 192.168.1.100 game  [heian] info: 192.168.1.15 ESTABLISHED 6
2021-11-19T16:32:21+08:00 192.168.1.100 game  [heian] info: 192.168.1.210 ESTABLISHED 1
2021-11-19T16:32:40+08:00 192.168.1.100 game  [heian] info: 10.10.10.3 ESTABLISHED 1
2021-11-19T16:32:40+08:00 192.168.1.100 game  [heian] info: 127.0.0.1 ESTABLISHED 6
2021-11-19T16:32:40+08:00 192.168.1.100 game  [heian] info: 172.18.0.2 ESTABLISHED 1
2021-11-19T16:32:40+08:00 192.168.1.100 game  [heian] info: 192.168.1.100 ESTABLISHED 6
2021-11-19T16:32:40+08:00 192.168.1.100 game  [heian] info: 192.168.1.15 ESTABLISHED 6
2021-11-19T16:32:40+08:00 192.168.1.100 game  [heian] info: 192.168.1.210 ESTABLISHED 1
```

集群的数据已经同步过来，后面直接接入elk就可以了。

# [Rsyslog同步集群服务器的网络连接状态](https://blog.csdn.net/heian_99/article/details/121432620)

![](../../image/07d4b6c2a5684582a567930301edfb08.png)

# [集群服务器的网络连接状态接入ELK（可视化操作）](https://blog.csdn.net/heian_99/article/details/121472415)

![](../../image/f0d382ca74a74af2b711e7e8e8a4a5cb.png)