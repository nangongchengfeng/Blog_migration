+++
author = "南宫乘风"
title = "Linux进程管理之top"
date = "2019-01-29 17:10:43"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/41.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86692562](https://blog.csdn.net/heian_99/article/details/86692562)

 

关于Linux进程查看，前面讲解了ps命令，下面拉介绍另一个命令top

 

ps：静态查看

top：动态查看

<br> 动态查看进程的状态 

# top

<br>![2019012917095356.png](https://img-blog.csdnimg.cn/2019012917095356.png)

```
[root@wei ~]# top
top - 18:38:46 up 15 min,  2 users,  load average: 0.09, 0.07, 0.06
Tasks:  98 total,   1 running,  97 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.0 us,  1.3 sy,  0.0 ni, 97.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :   997956 total,   613748 free,   215484 used,   168724 buff/cache
KiB Swap:  2097148 total,  2097148 free,        0 used.   605556 avail Mem 
 
```

<br>          7.6%us  用户进程占用的CPU<br>          1.6%sy  系统进程占用的CPU<br>          0.0%ni  调整过优先级的进程占用的CPU<br>          90.6%id  CPU空闲<br>          0.0%wa   等待磁盘IO的进程所占用的CPU<br>          <br> Cpu(s) :显示所有的CPU平均比，按1可现实每个CPU的使用情况

top交互式指令：<br>           <br>         M：按内存使用排序<br>         P：按CPU使用排序        <br>         T：按运行时间排序<br>         <br>         l: 是否显示TOP第1行信息<br>         m: 是否显示内存使用信息<br>         t: 是否显示CPU及任务信息<br>         <br>         c：是否显示完整的命令行<br>         q：退出TOP<br>         

<br> 显示当前时刻CPU的使用情况

```
[root@wei ~]# uptime
 19:03:27 up 39 min,  2 users,  load average: 0.00, 0.01, 0.05
```

top选项：<br>       <br>       -d 1 ：指定top信息刷新的频率<br>       -b  ：以批模式显示进程信息<br>       -n 2：共显示两批信息<br>       <br> # top -d 1 -b -n 2

<br> 查看服务器性能 ：<br>         <br>         1.ps ，top<br>         2.df  -hT<br>         3.free -m  查看磁盘<br>         <br>         <br> 使用这三个命令需要安装sysstat

```
[root@wei csdn]# yum install sysstat
```

    # mpstat   查看CPU

    # vmstat   查看内存<br>     # iostat   查看磁盘<br>     # sar      查看网卡<br>  

四个基本用法一样，参数设置一样。

```
[root@wei csdn]# mpstat 1     一秒显示一次
[root@wei csdn]# mpstat 1 5     一秒显示一次，显示5次
```

 

 

 

 

 
