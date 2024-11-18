---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-29 17:10:43
description: 关于进程查看，前面讲解了命令，下面拉介绍另一个命令：静态查看：动态查看动态查看进程的状态用户进程占用的系统进程占用的调整过优先级的进程占用的空闲等待磁盘的进程所占用的显示所有的平均比，按可现实每个的使。。。。。。。
image: ../../title_pic/29.jpg
slug: '201901291710'
tags:
- linux
title: Linux进程管理之top
---

<!--more-->

 

关于Linux进程查看，前面讲解了ps命令，下面拉介绍另一个命令top

 

ps：静态查看

top：动态查看

  
动态查看进程的状态 

\# top

  
![](../../image/2019012917095356.png)

```
[root@wei ~]# top
top - 18:38:46 up 15 min,  2 users,  load average: 0.09, 0.07, 0.06
Tasks:  98 total,   1 running,  97 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.0 us,  1.3 sy,  0.0 ni, 97.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :   997956 total,   613748 free,   215484 used,   168724 buff/cache
KiB Swap:  2097148 total,  2097148 free,        0 used.   605556 avail Mem 
 
```

  
         7.6\%us  用户进程占用的CPU  
         1.6\%sy  系统进程占用的CPU  
         0.0\%ni  调整过优先级的进程占用的CPU  
         90.6\%id  CPU空闲  
         0.0\%wa   等待磁盘IO的进程所占用的CPU  
           
Cpu\(s\) :显示所有的CPU平均比，按1可现实每个CPU的使用情况

top交互式指令：  
            
        M：按内存使用排序  
        P：按CPU使用排序          
        T：按运行时间排序  
          
        l: 是否显示TOP第1行信息  
        m: 是否显示内存使用信息  
        t: 是否显示CPU及任务信息  
          
        c：是否显示完整的命令行  
        q：退出TOP  
        

  
显示当前时刻CPU的使用情况

```
[root@wei ~]# uptime
 19:03:27 up 39 min,  2 users,  load average: 0.00, 0.01, 0.05
```

top选项：  
        
      \-d 1 ：指定top信息刷新的频率  
      \-b  ：以批模式显示进程信息  
      \-n 2：共显示两批信息  
        
\# top \-d 1 \-b \-n 2

  
查看服务器性能 ：  
          
        1.ps ，top  
        2.df  \-hT  
        3.free \-m  查看磁盘  
          
          
使用这三个命令需要安装sysstat

```
[root@wei csdn]# yum install sysstat
```

    # mpstat   查看CPU

    # vmstat   查看内存  
    # iostat   查看磁盘  
    # sar      查看网卡  
 

四个基本用法一样，参数设置一样。

```
[root@wei csdn]# mpstat 1     一秒显示一次
[root@wei csdn]# mpstat 1 5     一秒显示一次，显示5次
```