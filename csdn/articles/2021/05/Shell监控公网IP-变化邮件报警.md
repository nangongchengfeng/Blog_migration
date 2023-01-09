+++
author = "南宫乘风"
title = "Shell监控公网IP-变化邮件报警"
date = "2021-05-01 13:58:35"
tags=['shell', 'linux', 'bash']
categories=[' 企业级-Shell脚本案例', 'Linux Shell']
image = "post/4kdongman/98.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/116329525](https://blog.csdn.net/heian_99/article/details/116329525)

**Shell监控公网IP-变化邮件报警**

**公司用的网线IP，但是有时IP会改变，导致部分业务有问题，我们又不能及时发现，会造成一定的影响。**

**现在使用shell监控公网的IP，如发生变化，立即邮件报警。**

 

### [企业级-Shell案例2——发送告警邮件](https://blog.csdn.net/heian_99/article/details/104028229)

centos邮件报警可以参考这个，默认是mailx

 

### 脚本

```
#!/bin/bash
dirfile='/home/ip_change'
new_ip=`curl icanhazip.com`    #获取新公网ip
mail_user=1794@qq.com    #接收收邮件邮箱
mail_subject="IP已经发生变化，及时处理"    #邮件主题
log="/var/log/tool.log"
datetime=`date '+%Y-%m-%d %H:%M:%S'`
#判断文件是否存在
if [ ! -f "$dirfile" ]; then
  touch "$file"
  echo "1.1.1.1" &gt; $dirfile
fi
#判断new_ip是否获取

if [ ! -n "$new_ip" ]; then
    echo "$datetime 公网IP获取失败，检查'curl icanhazip.com' " &gt;&gt; $log
    exit 1
fi
old_ip=`cat $dirfile`     #查看旧ip

# 判断两个IP是否相等 发邮件
if [ "$new_ip" = "$old_ip" ]; then
  echo "$datetime IP正常 - true " &gt;&gt; $log
else
  echo  $new_ip &gt; $dirfile
  echo "IP已经发生变化, 新IP: $new_ip   旧IP： $old_ip  !!! " | mail -s "$mail_subject" "$mail_user"
  echo "$datetime IP已经发生变化 - error 新IP ：$new_ip   旧IP： $old_ip" &gt;&gt; $log
fi
```

![20210501135739773.png](https://img-blog.csdnimg.cn/20210501135739773.png)

![2021050113570613.png](https://img-blog.csdnimg.cn/2021050113570613.png)
