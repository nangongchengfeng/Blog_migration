---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-18 14:21:08
description: 一键查看服务器利用率背景：访问过慢，服务器内存搞内存利用率硬盘利用率连接状态脚本编写使用率：等待磁盘相应使用率：内存总大小使用剩余硬盘挂载点总大小使用使用率连接状态相关博文：企业级案例服务器系统配置初。。。。。。。
image: ../../title_pic/37.jpg
slug: '202001181421'
tags:
- 监控
- 利用率
title: 企业级-Shell案例4——一键查看服务器利用率
---

<!--more-->

# 一键查看服务器利用率

### 背景：web访问过慢，服务器内存搞

- cpu      60\%
- 内存     利用率
- 硬盘     利用率
- TCP连接状态

## 脚本编写

```bash
#!/bin/bash
function cpu(){
	
	util=$(vmstat | awk '{if(NR==3)print $13+$14}')
	iowait=$(vmstat | awk '{if(NR==3)print $16}')
	echo "CPU -使用率：${util}% ,等待磁盘IO相应使用率：${iowait}:${iowait}%"

}
function memory (){

	total=`free -m |awk '{if(NR==2)printf "%.1f",$2/1024}'`
    used=`free -m |awk '{if(NR==2) printf "%.1f",($2-$NF)/1024}'`
    available=`free -m |awk '{if(NR==2) printf "%.1f",$NF/1024}'`
    echo "内存 - 总大小: ${total}G , 使用: ${used}G , 剩余: ${available}G"
}
disk(){
	
	fs=$(df -h |awk '/^\/dev/{print $1}')
    for p in $fs; do
        mounted=$(df -h |awk '$1=="'$p'"{print $NF}')
        size=$(df -h |awk '$1=="'$p'"{print $2}')
        used=$(df -h |awk '$1=="'$p'"{print $3}')
        used_percent=$(df -h |awk '$1=="'$p'"{print $5}')
        echo "硬盘 - 挂载点: $mounted , 总大小: $size , 使用: $used , 使用率: $used_percent"
    done

}
function tcp_status() {
    summary=$(ss -antp |awk '{status[$1]++}END{for(i in status) printf i":"status[i]" "}')
    echo "TCP连接状态 - $summary"
}
cpu
memory
disk
tcp_status
```

![](../../image/20200118140907708.png)

 

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