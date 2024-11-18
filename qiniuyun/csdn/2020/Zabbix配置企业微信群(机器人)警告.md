---
author: 南宫乘风
categories:
- Zabbix监控
date: 2020-10-30 18:22:15
description: 企业微信机器人告警企业微信群聊里面增加机器人，机器人会提供发送信息的脚本进行实现的、创建企业微信机器人没有企业微信的可以自己在企业微信官网申请注册个企业，创建企业微信群至少个人以上这个后面需要使用到、。。。。。。。
image: ../../title_pic/18.jpg
slug: '202010301822'
tags:
- zabbix
- 监控
- 警告
- 企业微信
- 机器人
title: Zabbix配置企业微信群(机器人)警告
---

<!--more-->

## 企业微信机器人告警

企业微信群聊里面增加机器人，机器人会提供发送信息的URL

 python 脚本进行实现的

### 1、创建企业微信机器人

![](../../image/20201030181237742.png)

没有企业微信的可以自己在企业微信官网申请注册个企业，创建企业微信群至少 3 个人以上

![](../../image/20201030181333913.png)

**这个 webhook 后面需要使用到**

### 2、配置 zabbix server

2.1：配置脚本执行目录

定义脚本目录，我这里就选择了默认的目录

```bash
[root@zabbix-master ~]#  grep -Ev '^$|#' /etc/zabbix/zabbix_server.conf | grep ^A
AlertScriptsPath=/usr/lib/zabbix/alertscripts
```

![](../../image/20201030181408876.png)

2.2：创建脚本

进入该定义的脚本存放路径下创建用来推送告警消息的脚本

```bash
[root@zabbix-master ~]# 
[root@zabbix-master ~]# cd /usr/lib/zabbix/alertscripts

[root@zabbix-master alertscripts]# vim wechat.py 

#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import sys
import os

headers = {'Content-Type': 'application/json;charset=utf-8'}
api_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=36d51b45-162f6c9d13909" #这就是先前的webhook地址
def msg(text):
    json_text= {
     "msgtype": "text",
        "text": {
            "content": text
        },
    }
    print requests.post(api_url,json.dumps(json_text),headers=headers).content

if __name__ == '__main__':
    text = sys.argv[1]
    msg(text)
~            
```

2.3：赋予脚本执行权限

```bash
[root@zabbix-master alertscripts]# chmod +x wechat.py
[root@zabbix-master alertscripts]# python wechat.py 你好
{"errcode":0,"errmsg":"ok"}
[root@zabbix-master alertscripts]# 
```

![](../../image/20201030181751655.png)

### 3、zabbix Web 页面配置

3.1：创建报警媒介

管理--> 报警媒介类型--> 创建媒介类型  
新建一个企业微信的报警，脚本名称就是我们脚本名 wechat.py

![](../../image/20201030181818737.png)

![](../../image/20201030181827294.png)

![](../../image/20201030181834972.png)

3.2：创建动作

![](../../image/20201030181905798.png)

![](../../image/2020103018191314.png)

![](../../image/2020103018192468.png)

**默认标题：**

```bash
故障{TRIGGER.STATUS},服务器:{HOSTNAME1}发生: {TRIGGER.NAME}故障!

故障{TRIGGER.STATUS},服务器:{HOSTNAME1}发生: {TRIGGER.NAME}故障!
告警主机:{HOSTNAME1}
告警地址：{HOST.IP}
告警时间:{EVENT.DATE} {EVENT.TIME}
告警等级:{TRIGGER.SEVERITY}
告警信息: {TRIGGER.NAME}
告警项目:{TRIGGER.KEY1}
问题详情:{ITEM.NAME}:{ITEM.VALUE}
当前状态:{TRIGGER.STATUS}:{ITEM.VALUE1}
事件ID:{EVENT.ID}
```

**恢复操作**

```
恢复{TRIGGER.STATUS}, 服务器:{HOSTNAME1}: {TRIGGER.NAME}已恢复!


恢复{TRIGGER.STATUS}, 服务器:{HOSTNAME1}: {TRIGGER.NAME}已恢复!
告警主机:{HOSTNAME1}
告警地址：{HOST.IP}
告警时间:{EVENT.DATE} {EVENT.TIME}
告警等级:{TRIGGER.SEVERITY}
告警信息: {TRIGGER.NAME}
告警项目:{TRIGGER.KEY1}
问题详情:{ITEM.NAME}:{ITEM.VALUE}
当前状态:{TRIGGER.STATUS}:{ITEM.VALUE1}
事件ID:{EVENT.ID}
```

### 4、测试发送告警

![](../../image/2020103018211323.png)

 

![](../../image/20201030182132120.png)