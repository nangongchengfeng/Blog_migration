---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-18 15:50:52
description: 查看网卡的实时流量监控流量脚本编写流量进入流量传出相关博文：企业级案例服务器系统配置初始化企业级案例发送告警邮件企业级案例批量创建多个用户并设置密码企业级案例一键查看服务器利用率企业级案例找出占用内存。。。。。。。
image: ../../title_pic/69.jpg
slug: '202001181550'
tags:
- 网络
- 流量
- 监控
- shell
title: 企业级-Shell案例6——查看网卡的实时流量
---

<!--more-->

# 查看网卡的实时流量

监控流量

## 脚本编写

```bash
#!/bin/bash
eth0=$1
echo  -e    "流量进入--流量传出    "
while true; do
	old_in=$(cat /proc/net/dev |grep $eth0 |awk '{print $2}')
	old_out=$(cat /proc/net/dev |grep $eth0 |awk '{print $10}')
	sleep 1
	new_in=$(cat /proc/net/dev |grep $eth0 |awk '{print $2}')
	new_out=$(cat /proc/net/dev |grep $eth0 |awk '{print $10}')
	in=$(printf "%.1f%s" "$((($new_in-$old_in)/1024))" "KB/s")
	out=$(printf "%.1f%s" "$((($new_out-$old_out)/1024))" "KB/s")
	echo "$in $out"
done
```

![](../../image/20200118154838985.png)

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