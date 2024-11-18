---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-21 16:49:43
description: 攻击防范自动屏蔽攻击拒绝服务攻击点点原理：半连接脚本编写判断一分钟访问界面的次数，如果超出一定的次数，那就屏蔽异常日志分析的访问情况相关博文：企业级案例服务器系统配置初始化企业级案例发送告警邮件企业级。。。。。。。
image: ../../title_pic/58.jpg
slug: '202001211649'
tags:
- dos攻击
- nginx
- 日志
title: 企业级-Shell案例17——DOS攻击防范（自动屏蔽攻击IP）
---

<!--more-->

# DOS攻击防范（自动屏蔽攻击IP）

DOS  拒绝服务攻击

点   \---> 点

原理：tcp半连接

# 脚本编写

**判断一分钟ip访问界面的次数，如果超出一定的次数，那就屏蔽异常ip**

```bash
#!/bin/bash
DATE=$(date +%d/%b/%Y:%H:%M)
#nginx日志
LOG_FILE=/usr/local/nginx/logs/demo2.access.log
#分析ip的访问情况
ABNORMAL_IP=$(tail -n5000 $LOG_FILE |grep $DATE |awk '{a[$1]++}END{for(i in a)if(a[i]>10)print i}')
for IP in $ABNORMAL_IP; do
    if [ $(iptables -vnL |grep -c "$IP") -eq 0 ]; then
        iptables -I INPUT -s $IP -j DROP
        echo "$(date +'%F_%T') $IP" >> /tmp/drop_ip.log
    fi
done
```

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