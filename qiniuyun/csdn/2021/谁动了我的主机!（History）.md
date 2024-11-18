---
author: 南宫乘风
categories:
- Linux实战操作
date: 2021-01-22 10:31:21
description: 系统下可通过命令查看用户所有的历史操作记录，在安全应急响应中起着非常重要的作用，但在未进行附加配置情况下，命令只能查看用户历史操作记录，并不能区分用户以及操作时间，不便于审计分析。当然，一些不好的操作。。。。。。。
image: ../../title_pic/19.jpg
slug: '202101221031'
tags:
- linux
- shell
- 运维
- centos
title: 谁动了我的主机?（ History）
---

<!--more-->

Linux系统下可通过history命令查看用户所有的历史操作记录，在安全应急响应中起着非常重要的作用，但在未进行附加配置情况下，history命令只能查看用户历史操作记录，并不能区分用户以及操作时间，不便于审计分析。

当然，一些不好的操作习惯也可能通过命令历史泄露敏感信息。下面我们来介绍如何让history日志记录更细化，更便于我们审计分析。

![图片](../../image/c5ee7c661ce1daa542d25862d986a755.png)

##  History

**通过设置export HISTTIMEFORMAT='\%F \%T '，让历史记录中带上命令执行时间。**

> 注意”\%T”和后面的”’”之间有空格，不然查看历史记录的时候，时间和命令之间没有分割。
> 
> 要一劳永逸，这个配置可以写在/etc/profile中，当然如果要对指定用户做配置，这个配置可以写在/home/\$USER/.bash\_profile中。
> 
> 本文将以/etc/profile为例进行演示。

```bash
 vim /etc/profile
export HISTTIMEFORMAT='%F %T  '
source /etc/profile


要使配置立即生效请执行source /etc/profile，我们再查看history记录，可以看到记录中带上了命令执行时间。
```

![](../../image/20210122093349178.png)

![](../../image/20210122093423492.png)

**如果想要实现更细化的记录，比如登陆过系统的用户、IP地址、操作命令以及操作时间一一对应，可以通过在/etc/profile里面加入以下代码实现**

```bash
USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
export HISTTIMEFORMAT="[%F %T][`whoami`][${USER_IP}] "

修改/etc/profile并加载后，history记录如下，时间、IP、用户及执行的命令都一一对应。

```

![](../../image/20210122094533272.png)

通过以上配置，我们基本上可以满足日常的审计工作了，但了解系统的朋友应该很容易看出来，这种方法只是设置了环境变量，攻击者unset掉这个环境变量，或者直接删除命令历史，对于安全应急来说，这无疑是一个灾难。

针对这样的问题，我们应该如何应对，通过修改bash源码，让history记录通过syslog发送到远程logserver中，大大增加了攻击者对history记录完整性破坏的难度。

**history高级用法**

上面是记录History的方法。我们也可以通过写入文件，更加方便的记录和审计命令

```bash
#histroy
HISTSIZE=409600
export HISTTIMEFORMAT="[%F %T]"
export HISTORY_FILE=/var/log/.audit.log
export PROMPT_COMMAND='{ thisHistID=`history 1|awk "{print \\$1}"`;lastCommand=`history 1| awk "{\\$1=\"\" ;print}"`;user=`id -un`;whoStr=(`who -u am i`);realUser=${whoStr[0]};logMonth=${whoStr[2]};logDay=${whoStr[3]};logTime=${whoStr[4]};pid=${whoStr[6]};ip=${whoStr[7]};if [ ${thisHistID}x != ${lastHistID}x ];then echo -E `date "+%Y/%m/%d %H:%M:%S"` $user\($realUser\)@$ip[PID:$pid][LOGIN:$logMonth $logDay $logTime] --- $lastCommand ;lastHistID=$thisHistID;fi; } >> $HISTORY_FILE'
```

这个命令会在生成**/var/log/.audit.log 文件  **这里面记录的是命令

这样更为直观的分析和审计

![](../../image/20210122103009686.png)