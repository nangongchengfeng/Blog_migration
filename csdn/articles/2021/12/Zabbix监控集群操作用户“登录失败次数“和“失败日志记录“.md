+++
author = "南宫乘风"
title = "Zabbix监控集群操作用户“登录失败次数“和“失败日志记录“"
date = "2021-12-29 15:28:13"
tags=['安全', 'zabbix', '监控']
categories=['Zabbix监控']
image = "post/4kdongman/79.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/122216521](https://blog.csdn.net/heian_99/article/details/122216521)

近期，快要邻近春节，安全方面更加重要。

首先要对操作系统的用户做安全监控，防止操作系统账号被爆破泄露，我们也要监控起来。

（1）Zabbix记录每分钟日志登录失败的次数

（2）Zabbix记录登录失败用户的信息，方便查看



首先，我们**整个集群日志，通过rsyslog服务，把上千台的日志同步到一台上**，所以我们只需要**监控**这个**rsyslog的服务端**就可以了。 

**看效果图（这样一来，十分方便查看记录）**

![6a7d4549874b4a959571845d3f2fa003.png](https://img-blog.csdnimg.cn/6a7d4549874b4a959571845d3f2fa003.png)



![564c1453257f493cb99fce1b459db4ca.png](https://img-blog.csdnimg.cn/564c1453257f493cb99fce1b459db4ca.png)

![3e0e111a599747cda1a046503b0acace.png](https://img-blog.csdnimg.cn/3e0e111a599747cda1a046503b0acace.png)

 ![24a757410f8d4203ba7bb6e240216519.png](https://img-blog.csdnimg.cn/24a757410f8d4203ba7bb6e240216519.png)

## （1） 登录失败次数

日志格式

```
2021-12-29T15:04:16.264895+08:00 127.0.0.1 [sshd] notice: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=172.17.9.200  user=deployer

```

编写代码的脚本

```
#!/bin/bash
 
LOG_PATH="/var/log/secure"
mon=$(date +%B)
h=$(date +%d)
ms=$(date +%H:%M)
#表示字符开头为0就替换为空
h=${h/#0/""}
k="T"  #我这边有T，有的是空格，根据时间环境使用
count=`grep "$h$k$ms" /var/log/secure | grep -v sudo | grep -c "authentication failure" `
echo $count

```

修改zabbix客户端配置

```
#====================检查 账号登录失败次数======================
UserParameter=check_failed,sh /usr/local/zabbix-v503/scripts/check_failed.sh
```

重启zabbix客户端





zabbix界面配置

检查配置

![6e8be05c7a5a4c9eb61b4cd7aaa3c25d.png](https://img-blog.csdnimg.cn/6e8be05c7a5a4c9eb61b4cd7aaa3c25d.png)

 触发器

![f7394203d3b941a7b844df9f1e528768.png](https://img-blog.csdnimg.cn/f7394203d3b941a7b844df9f1e528768.png)



## （2）失败日志记录

编写脚本

```
[root@logserver01 zabbix-v503]# cat scripts/check_failedlog.sh 
#!/bin/bash
 
LOG_PATH="/var/log/secure"
mon=$(date +%B)
h=$(date +%d)
#获取前一分钟的爆破日志记录的时间  时:分
ms=$(date -d "1 minute ago" +"%H:%M")
#表示字符开头为0就替换为空
h=${h/#0/""}
k="T"
grep "$h$k$ms" /var/log/secure | grep -v sudo | grep "authentication failure" &gt;&gt; /usr/local/zabbix-v503/scripts/fail.log

```

开启定时任务（每分钟检查一次）

```
#-------check_fail_user_log-----------------
* * * * * sh /usr/local/zabbix-v503/scripts/check_failedlog.sh

```



如果有登录失败的，会单独过滤出来

![93f99c7a00fb46168a72df8420e5ef25.png](https://img-blog.csdnimg.cn/93f99c7a00fb46168a72df8420e5ef25.png)

zabbix界面配置

```
log[/usr/local/zabbix-v503/scripts/fail.log,"sshd",skip,]
```

![4619ce4636234a6ab3bc0fda75c04595.png](https://img-blog.csdnimg.cn/4619ce4636234a6ab3bc0fda75c04595.png)

已经完成相关的项目类容，很容易监控。

![9494914d2d8d46b0a082618d7d20ab23.png](https://img-blog.csdnimg.cn/9494914d2d8d46b0a082618d7d20ab23.png)

 根据触发器，可以设置值，如果每分钟爆破登录失败10次，就报警，有爆破的嫌疑
