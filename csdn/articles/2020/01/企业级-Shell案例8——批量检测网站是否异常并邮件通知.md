+++
author = "南宫乘风"
title = "企业级-Shell案例8——批量检测网站是否异常并邮件通知"
date = "2020-01-18 18:14:53"
tags=['linux', 'shelll', '脚本']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/22.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104032121](https://blog.csdn.net/heian_99/article/details/104032121)

# 批量检测网站是否异常脚本

**检测网站运行是否正常，如果不能正常访问，发送邮件通知管理员**

```
curl -o /de/dev/null -s -w "%{http_code}" www.baidu.com

```

![20200118172939936.png](https://img-blog.csdnimg.cn/20200118172939936.png)

访问失败，也又可能和网络等等原因有关。

所以我们要进行次数判断，超出一定的次数。那就发送邮件。

# 脚本编写

```
#!/bin/bash  
URL_LIST="www.baidu.com www.ctnrs.com www.der-matech.net.cn www.der-matech.com.cn www.der-matech.cn www.der-matech.top www.der-matech.org"
for URL in $URL_LIST; do
    FAIL_COUNT=0
    for ((i=1;i&lt;=3;i++)); do
        HTTP_CODE=$(curl -o /dev/null --connect-timeout 3 -s -w "%{http_code}" $URL)
        if [ $HTTP_CODE -eq 200 ]; then
            echo "$URL OK"
            break
        else
            echo "$URL retry $FAIL_COUNT"
            let FAIL_COUNT++
        fi
    done
    if [ $FAIL_COUNT -eq 3 ]; then
        echo "Warning: $URL Access failure!"
		echo "网站$URL坏掉，请及时处理" | mail -s "$URL网站高危" 1794748404@qq.com
    fi
done
```

# 测试效果图

![20200118180558806.png](https://img-blog.csdnimg.cn/20200118180558806.png)

在设置个定时任务，10分钟一次。

然后就可以了。

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
