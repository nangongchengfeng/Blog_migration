+++
author = "南宫乘风"
title = "mysql-unknown-option-in-kubernetes错误"
date = "2021-04-07 15:28:32"
tags=[]
categories=['Kubernetes', '错误问题解决']
image = "post/4kdongman/53.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/115486589](https://blog.csdn.net/heian_99/article/details/115486589)

## **错误问题**

**原因：把MySQL的用户密码配置成secrets，然后挂载mysql，mysql会一直报错，无法完成初始**

```
Version: '5.7.33'  socket: '/var/run/mysqld/mysqld.sock'  port: 0  MySQL Community Server (GPL)
2021-04-07 15:06:32+08:00 [Note] [Entrypoint]: Temporary server started.
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
2021-04-07T07:06:58.526144Z 0 [Note] InnoDB: page_cleaner: 1000ms intended loop took 24159ms. The settings might not be optimal. (flushed=200 and evicted=0, during the time.)
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
2021-04-07 15:06:58+08:00 [Note] [Entrypoint]: Creating database wordpress
mysql: [ERROR] unknown option '--"'
```

![20210407151922867.png](https://img-blog.csdnimg.cn/20210407151922867.png)

## 解决问题

问题是我使用该`echo 'secret' | base64`命令创建了我的机密，而echo命令自动插入了结尾的换行符。

使用`echo -n 'secret' | base64`代替。✔️

因此我没有注意到日志输出中有换行符。希望这可以帮助一些也使用echo命令对base64进行编码的人。

![20210407152321646.png](https://img-blog.csdnimg.cn/20210407152321646.png)

![20210407152651461.png](https://img-blog.csdnimg.cn/20210407152651461.png)

 

参考文章： [https://stackoverflow.com/questions/62985541/mysql-unknown-option-in-kubernetes#](https://stackoverflow.com/questions/62985541/mysql-unknown-option-in-kubernetes#)

 
