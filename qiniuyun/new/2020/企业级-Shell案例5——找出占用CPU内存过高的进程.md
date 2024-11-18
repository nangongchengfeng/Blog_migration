---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-18 14:40:38
description: 找出占用内存过高的进程脚本背景：服务器占用高，找出最高的分析，看是否进程正确，是否是垃圾进程分析占用最高的应用分析占用内存最高的应用整合脚本占用前排序内存占用前排序相关博文：企业级案例服务器系统配置初。。。。。。。
image: http://image.ownit.top/4kdongman/87.jpg
tags:
- cpu
- 内存
- shell
- 监控
title: 企业级-Shell案例5——找出占用CPU 内存过高的进程
---

<!--more-->

# 找出占用CPU 内存过高的进程脚本

**背景：服务器CPU占用高，找出最高的分析，看是否进程正确，是否是垃圾进程**

# **分析占用CPU最高的应用**

```
ps -eo user,pid,pcpu,pmem,args --sort=-pcpu  |head -n 10
```

![](http://image.ownit.top/csdn/20200118143602987.png)

# **分析占用内存最高的应用**

```
ps -eo user,pid,pcpu,pmem,args --sort=-pmem  |head -n 10
```

![](http://image.ownit.top/csdn/20200118143704617.png)

# 整合脚本

```bash
#!/bin/bash
echo "-------------------CUP占用前10排序--------------------------------"
ps -eo user,pid,pcpu,pmem,args --sort=-pcpu  |head -n 10
echo "-------------------内存占用前10排序--------------------------------"
ps -eo user,pid,pcpu,pmem,args --sort=-pmem  |head -n 10
```

![](http://image.ownit.top/csdn/20200118143955877.png)

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