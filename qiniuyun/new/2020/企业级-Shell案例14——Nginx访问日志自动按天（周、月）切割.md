---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-21 14:40:10
description: 访问日志自动按天周、月切割适用于企业级分析，可以更加准确、速度分析日志。方便使用。设置凌晨定时任务，每天可以自动切割日志。日志目录获取到上一天的时间归档日志取时间归档日志的名称相关博文：企业级案例服务。。。。。。。
image: http://image.ownit.top/4kdongman/87.jpg
tags:
- nginx
- 日志
- 切割
title: 企业级-Shell案例14——Nginx访问日志自动按天（周、月）切割
---

<!--more-->

# Nginx访问日志自动按天（周、月）切割

适用于企业级分析，可以更加准确、速度分析日志。方便使用。

设置凌晨定时任务，每天可以自动切割日志。

```bash
#!/bin/bash
#nginx日志目录
LOG_DIR=/www/server/nginx/logs
#获取到上一天的时间
YESTERDAY_TIME=$(date -d "yesterday" +%F)
#归档日志取时间
LOG_MONTH_DIR=$LOG_DIR/$(date +"%Y-%m")
#归档日志的名称
LOG_FILE_LIST="access.log"

for LOG_FILE in $LOG_FILE_LIST; do
    [ ! -d $LOG_MONTH_DIR ] && mkdir -p $LOG_MONTH_DIR
    mv $LOG_DIR/$LOG_FILE $LOG_MONTH_DIR/${LOG_FILE}_${YESTERDAY_TIME}
done

kill -USR1 $(cat $LOG_DIR/nginx.pid)
```

![](http://image.ownit.top/csdn/2020012114354386.png)

# 相关博文：

# [ 企业级-Shell案例1——服务器系统配置初始化](https://blog.csdn.net/heian_99/article/details/104027379)

# [企业级-Shell案例2——发送告警邮件](https://blog.csdn.net/heian_99/article/details/104028229)

# [企业级-Shell案例3——批量创建多个用户并设置密码](https://blog.csdn.net/heian_99/article/details/104028407)

# [企业级-Shell案例4——一键查看服务器利用率](https://blog.csdn.net/heian_99/article/details/104028739)

# [企业级-Shell案例5——找出占用CPU 内存过高的进程](https://blog.csdn.net/heian_99/article/details/104030019)

# [企业级-Shell案例6——查看网卡的实时流量](https://blog.csdn.net/heian_99/article/details/104030173)

# [企业级-Shell案例7——监控多台服务器磁盘利用率脚本](https://blog.csdn.net/heian_99/article/details/104031458)

# [企业级-Shell案例8——批量检测网站是否异常并邮件通知](https://blog.csdn.net/heian_99/article/details/104032121)

# [企业级-Shell案例9——批量主机远程执行命令脚本](https://blog.csdn.net/heian_99/article/details/104039706)

# [企业级-Shell案例10——一键部署LNMP网站平台脚本](https://blog.csdn.net/heian_99/article/details/104039886)

# [企业级-Shell案例11——监控MySQL主从同步状态是否异常脚本](https://blog.csdn.net/heian_99/article/details/104040379)

# [企业级-Shell案例12——MySql数据库备份脚本](https://blog.csdn.net/heian_99/article/details/104061077)

# [企业级-Shell案例13——Nginx访问日志分析](https://blog.csdn.net/heian_99/article/details/104061361)

# [企业级-Shell案例14——Nginx访问日志自动按天（周、月）切割](https://blog.csdn.net/heian_99/article/details/104061818)

# [企业级-Shell案例15——自动发布Java项目（Tomcat）](https://blog.csdn.net/heian_99/article/details/104062470)

# [企业级-Shell案例16——自动发布PHP项目](https://blog.csdn.net/heian_99/article/details/104062967)

# [企业级-Shell案例17——DOS攻击防范（自动屏蔽攻击IP）](https://blog.csdn.net/heian_99/article/details/104063402)

# [企业级-Shell案例18——目录入侵检测与告警](https://blog.csdn.net/heian_99/article/details/104063746)