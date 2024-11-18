---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2020-01-21 13:42:41
description: 数据库备份脚本备份数据库，使用企业级，可以防止数据库出错。分库备份备份失败分表备份备份失败相关博文：企业级案例服务器系统配置初始化企业级案例发送告警邮件企业级案例批量创建多个用户并设置密码企业级案例一。。。。。。。
image: http://image.ownit.top/4kdongman/24.jpg
tags:
- mysql
- mysqldump
- 数据库
title: 企业级-Shell案例12——MySql数据库备份脚本
---

<!--more-->

# MySql数据库备份脚本

**mysql备份数据库，使用企业级，可以防止数据库出错。**

**分库备份**

```bash
mysqldump -uroot -pxxx -B A > A.sql
```

```bash
#!/bin/bash
DATE=$(date +%F_%H-%M-%S)
HOST=localhost
USER=backup
PASS=123.com
BACKUP_DIR=/data/db_backup
DB_LIST=$(mysql -h$HOST -u$USER -p$PASS -s -e "show databases;" 2>/dev/null |egrep -v "Database|information_schema|mysql|performance_schema|sys")

for DB in $DB_LIST; do
    BACKUP_NAME=$BACKUP_DIR/${DB}_${DATE}.sql
    if ! mysqldump -h$HOST -u$USER -p$PASS -B $DB > $BACKUP_NAME 2>/dev/null; then
        echo "$BACKUP_NAME 备份失败!"
    fi
done
```

**分表备份**

```
mysqldump -uroot -pxxx -A t > t.sql
```

```bash
#!/bin/bash
DATE=$(date +%F_%H-%M-%S)
HOST=localhost
USER=backup
PASS=123.com
BACKUP_DIR=/data/db_backup
DB_LIST=$(mysql -h$HOST -u$USER -p$PASS -s -e "show databases;" 2>/dev/null |egrep -v "Database|information_schema|mysql|performance_schema|sys")

for DB in $DB_LIST; do
    BACKUP_DB_DIR=$BACKUP_DIR/${DB}_${DATE}
    [ ! -d $BACKUP_DB_DIR ] && mkdir -p $BACKUP_DB_DIR &>/dev/null
    TABLE_LIST=$(mysql -h$HOST -u$USER -p$PASS -s -e "use $DB;show tables;" 2>/dev/null)
    for TABLE in $TABLE_LIST; do
        BACKUP_NAME=$BACKUP_DB_DIR/${TABLE}.sql 
        if ! mysqldump -h$HOST -u$USER -p$PASS $DB $TABLE > $BACKUP_NAME 2>/dev/null; then
            echo "$BACKUP_NAME 备份失败!"
        fi
    done
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