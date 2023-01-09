+++
author = "南宫乘风"
title = "Linux计划任务管理"
date = "2019-01-31 21:08:21"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/75.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86726181](https://blog.csdn.net/heian_99/article/details/86726181)

# <br>**计划任务**

### **类型：<br>     一次性计划任务<br>     周期性计划任务**

# <br>**    <br> 一次性计划任务**

**前提：  atd服务必须运行**

```
[root@wei init.d]# yum -y install at        #安装atd服务

[root@wei init.d]# systemctl start atd      #开启atd服务

[root@wei init.d]# systemctl status atd     #查看atd开启状态
```

<br>**![20190131205405517.png](https://img-blog.csdnimg.cn/20190131205405517.png)**

**18:00关机（以系统时间为准）：**

```
[root@wei init.d]# at 18:00
at&gt; poweroff
at&gt; &lt;EOT&gt;  # Ctrl+d 提交任务
job 1 at Fri Feb  1 18:00:00 2019
```

<br>**1分钟后执行的任务：<br>     **

```
[root@wei init.d]# at now + 1 minute
at&gt; mkdir /root/nangong
at&gt; &lt;EOT&gt;
job 4 at Thu Jan 31 18:49:00 2019
```

# **周期性计划任务**

**前提：crond服务必须运行**

```
[root@wei ~]# yum install crontabs      #安装crond服务

[root@wei init.d]# systemctl start crond      #开启crond服务

[root@wei ~]# systemctl status crond       #查看crond开启状态
```

**![20190131205612649.png](https://img-blog.csdnimg.cn/20190131205612649.png)<br><br> 制作周期性计划任务**

**# crontab -e **

**      时间        COMMAND**

**时间：<br>     分  时  日   月   周<br>     <br>     分钟： 0----59<br>     时：   0----23<br>     日期： 1----31<br>     月：   1---12<br>     周：   0----6<br>      *  表示每周（日   月   周）<br>      -  连续的时间<br>      ， 不连续的时间<br> 示例：**

**每天晚上11:30     30 23 * * *<br> 每天零点          0 0 * * *    <br> 每天早上8:10 9:10 10:10   10 8-10 * * *  <br> 每隔5分钟          */5 * * * *<br> 每隔3小时          * */3 * * *      **

**COMMAND命令： <br>          1.建议写命令的完整路径 /bin/mkdir/abc<br>          2.只能写一条命令（shell）<br>          **<br>  

### **注意：<br>        在写命令时%在周期性计划任务中是结束的意思，因此在使用%时，需要加\右斜杠转义<br>        &amp;&gt; /dev/null  不给用户发邮件<br>        **

**创建计划任务**

**示例：<br> （1）每分钟在tmp目录下创建文件**

**[root@wei ~]# crontab -e         **

***/1 * * * *   /usr/bin/touch /tmp/wei/$(date +\%F-\%T).txt**

**![20190131205939941.png](https://img-blog.csdnimg.cn/20190131205939941.png)**

**（2）每分钟分别显示磁盘使用，cpu状态，内存状态的信息**

**分析：一行只能写一条命令，但要显示三个命令，则需要借助shell脚本。然后在周期性任务中调用shell脚本。**

**（1）创建shell脚本**

```
[root@wei ~]# vim hei.sh
#!/bin/bash
echo
echo "CPU负载"
uptime
echo
echo "磁盘容量："
df -hT
echo
echo "内存容量"
free -h
```

**我在次调用演示。**

**![20190131210452568.png](https://img-blog.csdnimg.cn/20190131210452568.png)**

**（2）创建周期性任务**<br>  

```
[root@wei ~]# crontab -e     

*/1 * * * *  /usr/bin/bash /root/hei.sh 
```

**注意：这个会给root用户发邮件显示shell脚本运行的信息**

 

```
*/1 * * * *  /usr/bin/bash /root/hei.sh &amp;&gt; /dev/null
```

**  &amp;&gt; /dev/null  不给用户发邮件**

<br>**查看计划任务**

```
[root@wei ~]# crontab -l
*/1 * * * *   /usr/bin/touch /tmp/wei/$(date +\%F-\%T).txt
*/1 * * * *  /usr/bin/bash /root/hei.sh &amp;&gt; /dev/null
```

**删除计划任务（全部删除）**

```
[root@wei ~]# crontab -r
```

 
