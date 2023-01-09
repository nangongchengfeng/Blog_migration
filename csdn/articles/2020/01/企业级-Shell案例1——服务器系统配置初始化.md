+++
author = "南宫乘风"
title = "企业级-Shell案例1——服务器系统配置初始化"
date = "2020-01-18 10:48:05"
tags=['Linux', '案例', 'shell', '脚本']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/83.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104027379](https://blog.csdn.net/heian_99/article/details/104027379)

# 服务器系统配置初始化

## 背景：新购买10台服务器并已安装Linux操作系统

### 需求：
1. 安装系统新能分析工具已经其他的工具1. 设置时区并同步时间1. 禁用selinux1. 清空防火墙默认策源1. 历史命令显示操作时间1. 禁止root远程登录1. 禁止定时任务发送邮件1. 设置最大打开文件数1. 减少Swap使用1. 系统内核参数的优化
# 脚本编写

```
#/bin/bash
# 安装系统性能分析工具及其他
yum install gcc make autoconf vim sysstat net-tools iostat iftop iotp wget lrzsz lsof unzip openssh-clients net-tool vim ntpdate -y
# 设置时区并同步时间
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
if ! crontab -l |grep ntpdate &amp;&gt;/dev/null ; then
    (echo "* 1 * * * ntpdate time.windows.com &gt;/dev/null 2&gt;&amp;1";crontab -l) |crontab 
fi

# 禁用selinux
sed -i '/SELINUX/{s/permissive/disabled/}' /etc/selinux/config

# 关闭防火墙
if egrep "7.[0-9]" /etc/redhat-release &amp;&gt;/dev/null; then
    systemctl stop firewalld
    systemctl disable firewalld
elif egrep "6.[0-9]" /etc/redhat-release &amp;&gt;/dev/null; then
    service iptables stop
    chkconfig iptables off
fi

# 历史命令显示操作时间
if ! grep HISTTIMEFORMAT /etc/bashrc; then
    echo 'export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S  `whoami` "' &gt;&gt; /etc/bashrc
fi

# SSH超时时间
if ! grep "TMOUT=600" /etc/profile &amp;&gt;/dev/null; then
    echo "export TMOUT=600" &gt;&gt; /etc/profile
fi

# 禁止root远程登录 切记给系统添加普通用户，给su到root的权限
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 禁止定时任务向发送邮件
sed -i 's/^MAILTO=root/MAILTO=""/' /etc/crontab 

# 设置最大打开文件数
if ! grep "* soft nofile 65535" /etc/security/limits.conf &amp;&gt;/dev/null; then
cat &gt;&gt; /etc/security/limits.conf &lt;&lt; EOF
    * soft nofile 65535
    * hard nofile 65535
EOF
fi

# 系统内核优化
cat &gt;&gt; /etc/sysctl.conf &lt;&lt; EOF
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_tw_buckets = 20480
net.ipv4.tcp_max_syn_backlog = 20480
net.core.netdev_max_backlog = 262144
net.ipv4.tcp_fin_timeout = 20  
EOF

# 减少SWAP使用
echo "0" &gt; /proc/sys/vm/swappiness

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
