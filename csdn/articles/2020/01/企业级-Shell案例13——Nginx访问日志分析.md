+++
author = "南宫乘风"
title = "企业级-Shell案例13——Nginx访问日志分析"
date = "2020-01-21 14:14:12"
tags=['nginx', '分析']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/97.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104061361](https://blog.csdn.net/heian_99/article/details/104061361)

# Nginx访问日志分析

**分析客户访问是否正常**
1. 访问最多的IP1. 访问最多的页面1. 访问页面状态码的数量1. 根据时间段来访问最多的IP
UV：用户访问次数 （天）

PV：总页面访问次数（天）

**访问最多的IP**

```
 awk '{a[$1]++}END{print "UV:",length(a);for(v in a)print v,a[v]}' access.log |sort -k2 -nr |head -10

```

![20200121140247369.png](https://img-blog.csdnimg.cn/20200121140247369.png)

**统计时间段访问最多的IP**

```
awk '$4&gt;="[01/Dec/2018:13:20:25" &amp;&amp; $4&lt;="[27/Nov/2018:16:20:49"{a[$1]++}END{for(v in a)print v,a[v]}' $LOG_FILE |sort -k2 -nr|head -10
```

**访问最多的10个页面**

```
awk '{a[$7]++}END{print "PV:",length(a);for(v in a){if(a[v]&gt;5)print v,a[v]}}' access.log |sort -k2 -nr
```

**统计访问页面状态码数量**

```
awk '{a[$7" "$9]++}END{for(v in a){if(a[v]&gt;5)print v,a[v]}}' $LOG_FILE |sort -k3 -nr
```

# 脚本编写

```
#!/bin/bash
# 日志格式: $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"
LOG_FILE=$1
echo "统计访问最多的10个IP"
awk '{a[$1]++}END{print "UV:",length(a);for(v in a)print v,a[v]}' $LOG_FILE |sort -k2 -nr |head -10
echo "----------------------"

echo "统计时间段访问最多的IP"
awk '$4&gt;="[01/Dec/2018:13:20:25" &amp;&amp; $4&lt;="[27/Nov/2018:16:20:49"{a[$1]++}END{for(v in a)print v,a[v]}' $LOG_FILE |sort -k2 -nr|head -10
echo "----------------------"

echo "统计访问最多的10个页面"
awk '{a[$7]++}END{print "PV:",length(a);for(v in a){if(a[v]&gt;10)print v,a[v]}}' $LOG_FILE |sort -k2 -nr
echo "----------------------"

echo "统计访问页面状态码数量"
awk '{a[$7" "$9]++}END{for(v in a){if(a[v]&gt;5)print v,a[v]}}' $LOG_FILE |sort -k3 -nr
```

![20200121141350865.png](https://img-blog.csdnimg.cn/20200121141350865.png)

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
