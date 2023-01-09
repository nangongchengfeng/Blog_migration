+++
author = "南宫乘风"
title = "企业级-Shell案例3——批量创建多个用户并设置密码"
date = "2020-01-18 11:45:08"
tags=['shell', '用户', '批量']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/26.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104028407](https://blog.csdn.net/heian_99/article/details/104028407)

# 批量创建多少个用户并设置密码

### 背景：多名新人入职

 

### 单个用户创建

**添加**

```
 useradd zhang

```

**改密码**

```
 passwd zhang

```

![20200118111945342.png](https://img-blog.csdnimg.cn/20200118111945342.png)

# 脚本编写

```
#!/bin/bash
USER_LIST=$@
USER_FILE=./user.info
for USER in $USER_LIST;do
	if ! id $USER &amp;&gt;/dev/null; then
		PASS=$(echo $RANDOM |md5sum |cut -c 1-8)
		useradd $USER
		echo $PASS | passwd --stdin $USER &amp;&gt;/dev/null
		echo "$USER   $PASS" &gt;&gt; $USER_FILE
		echo "$USER User create successful."
	else
		echo "$USER User already exists!"
	fi
done
```

```
./user.sh li zhang wei wu yi

```

![2020011811442955.png](https://img-blog.csdnimg.cn/2020011811442955.png)

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
