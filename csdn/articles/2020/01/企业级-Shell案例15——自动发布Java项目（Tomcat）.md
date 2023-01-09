+++
author = "南宫乘风"
title = "企业级-Shell案例15——自动发布Java项目（Tomcat）"
date = "2020-01-21 16:01:02"
tags=['java', '自动部署']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/08.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104062470](https://blog.csdn.net/heian_99/article/details/104062470)

# 自动发布Java项目（Tomcat）

需求:

代码已经到版本仓库，执行shell脚本一键部署

流程步骤:

java --&gt; jar/war  --&gt; tomcat/resin       jar-jar

# 脚本编写

```
#!/bin/bash
DATE=$(date +%F_%T)

TOMCAT_NAME=$1
TOMCAT_DIR=/usr/local/$TOMCAT_NAME
ROOT=$TOMCAT_DIR/webapps/ROOT

BACKUP_DIR=/data/backup
WORK_DIR=/tmp
PROJECT_NAME=tomcat-java-demo

# 拉取代码
cd $WORK_DIR
if [ ! -d $PROJECT_NAME ]; then
   git clone https://github.com/lizhenliang/tomcat-java-demo
   cd $PROJECT_NAME
else
   cd $PROJECT_NAME
   git pull
fi

# 构建
mvn clean package -Dmaven.test.skip=true
if [ $? -ne 0 ]; then
   echo "maven build failure!"
   exit 1
fi

# 部署
TOMCAT_PID=$(ps -ef |grep "$TOMCAT_NAME" |egrep -v "grep|$$" |awk 'NR==1{print $2}')
[ -n "$TOMCAT_PID" ] &amp;&amp; kill -9 $TOMCAT_PID
[ -d $ROOT ] &amp;&amp; mv $ROOT $BACKUP_DIR/${TOMCAT_NAME}_ROOT$DATE
unzip $WORK_DIR/$PROJECT_NAME/target/*.war -d $ROOT
$TOMCAT_DIR/bin/startup.sh


```

![20200121160036496.png](https://img-blog.csdnimg.cn/20200121160036496.png)

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
