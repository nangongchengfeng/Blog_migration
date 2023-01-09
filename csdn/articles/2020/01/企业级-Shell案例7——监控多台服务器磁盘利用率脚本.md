+++
author = "南宫乘风"
title = "企业级-Shell案例7——监控多台服务器磁盘利用率脚本"
date = "2020-01-18 17:16:17"
tags=['ssh', '监控', '磁盘']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/58.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104031458](https://blog.csdn.net/heian_99/article/details/104031458)

# 监控多台服务器磁盘利用率脚本

 

## SSH

```
ssh root@192.168.1.99 "df -h"

```

![20200118162917664.png](https://img-blog.csdnimg.cn/20200118162917664.png)

但每次要使用密码，不推荐使用。

可以使用秘钥登录。

## 创建秘钥【一直回车就行】

```
ssh-keygen
```

![20200118163246786.png](https://img-blog.csdnimg.cn/20200118163246786.png)

## 把公钥复制到需要被控的服务器

```
ssh-copy-id root@192.168.1.99

```

![2020011816355378.png](https://img-blog.csdnimg.cn/2020011816355378.png)

在被传公钥的服务器的root的.ssh下

```
ls .ssh/

```

![20200118163740302.png](https://img-blog.csdnimg.cn/20200118163740302.png)

## 私钥登录公钥服务器

```
ssh -i .ssh/id_rsa root@192.168.1.99
```

![20200118163846994.png](https://img-blog.csdnimg.cn/20200118163846994.png)

## 脚本编写

```
#!/bin/bash
HOST_INFO=host.info
for IP in $(awk '/^[^#]/{print $1}' $HOST_INFO); do
	#取出用户名和端口
    USER=$(awk -v ip=$IP 'ip==$1{print $2}' $HOST_INFO)
    PORT=$(awk -v ip=$IP 'ip==$1{print $3}' $HOST_INFO)
	#创建临时文件，保存信息
    TMP_FILE=/tmp/disk.tmp
	#通过公钥登录获取主机磁盘信息
    ssh -p $PORT $USER@$IP 'df -h' &gt; $TMP_FILE
	#分析磁盘占用空间
    USE_RATE_LIST=$(awk 'BEGIN{OFS="="}/^\/dev/{print $NF,int($5)}' $TMP_FILE)
	#循环磁盘列表，进行判断
    for USE_RATE in $USE_RATE_LIST; do
		#取出等号（=）右边的值 挂载点名称
        PART_NAME=${USE_RATE%=*}  
		#取出等号（=）左边的值  磁盘利用率
        USE_RATE=${USE_RATE#*=}
		#进行判断
        if [ $USE_RATE -ge 80 ]; then
            echo "Warning: $PART_NAME Partition usage $USE_RATE%!"
			 echo "服务器$IP的磁盘空间占用过高，请及时处理" | mail -s "空间不足警告" 你的qq@qq.com
		else
			echo "服务器$IP的$PART_NAME目录空间良好"
        fi
    done
done
```

 

![20200118171504700.png](https://img-blog.csdnimg.cn/20200118171504700.png)

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
