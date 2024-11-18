---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-18 11:15:22
description: 发送告警邮件安装软件配置文件进入邮箱首页，点击设置账户，然后找到下图截取的地方需要设置的，如图设置完之后呢，就要把生成的授权码作为邮箱的的啦配置文件下面的配置是假的，别用设置发件人名称设置邮件服务器填。。。。。。。
image: http://image.ownit.top/4kdongman/40.jpg
tags:
- 告警
- 邮件
- shell
title: 企业级-Shell案例2——发送告警邮件
---

<!--more-->

# 发送告警邮件

### 安装软件

```
yum install mailx -y
```

### 配置文件

进入qq邮箱首页，点击设置>账户，然后找到下图截取的地方（需要设置的，如图）

![](http://image.ownit.top/csdn/20200118110439674.png)

设置完之后呢，就要把生成的授权码作为邮箱的password的啦\~

配置/etc/mail.rc文件【**下面的配置qq是假的，别用**】

```bash
#设置发件人名称
set from=1832025651@qq.com
#设置邮件服务器
set smtp=smtp.qq.com
#填写自己邮箱地址
set smtp-auth-user=1832025651@qq.com
#输入邮箱验证码
set smtp-auth-password=pfljngafoqaxecff
#smtp的认证方式，默认是login
set smtp-auth=login
```

![](http://image.ownit.top/csdn/20200118110957449.png)

## 测试【已经完成】

```
 echo "admin ,文件内容" | mail -s "标题" 你的qq@qq.com
```

![](http://image.ownit.top/csdn/20200118111106217.png)

 

## 后续会用到这个。

 

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