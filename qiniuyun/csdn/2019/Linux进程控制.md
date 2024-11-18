---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-30 20:51:51
description: 上进程有种状态，这中状态可以与一般操作系统的状态对应起来：运行：正在运行或在运行队列中等待。中断：休眠中，受阻，在等待某个条件的形成或接受到信号。不可中断：收到信号不唤醒和不可运行，进程必须等待直到有。。。。。。。
image: ../../title_pic/50.jpg
slug: '201901302051'
tags:
- linux
title: Linux进程控制
---

<!--more-->

**Linux上进程有5种状态，这5中状态可以与一般操作系统的状态对应起来：**

- **运行：正在运行或在运行队列中等待。**
- **中断：休眠中， 受阻， 在等待某个条件的形成或接受到信号。**
- **不可中断：收到信号不唤醒和不可运行， 进程必须等待直到有中断发生。**
- **僵死：进程已终止， 但进程描述符存在， 直到父进程调用wait4\(\)系统调用后释放。**
- **停止：进程收到SIGSTOP， SIGSTP， SIGTIN， SIGTOU信号后停止运行运行。**

  
**进程控制**

**    信号：Signal  
      
查看所有的信号**

```
[root@wei csdn]# kill -l
 1) SIGHUP     2) SIGINT     3) SIGQUIT     4) SIGILL     5) SIGTRAP
 6) SIGABRT     7) SIGBUS     8) SIGFPE     9) SIGKILL    10) SIGUSR1
11) SIGSEGV    12) SIGUSR2    13) SIGPIPE    14) SIGALRM    15) SIGTERM
16) SIGSTKFLT    17) SIGCHLD    18) SIGCONT    19) SIGSTOP    20) SIGTSTP
21) SIGTTIN    22) SIGTTOU    23) SIGURG    24) SIGXCPU    25) SIGXFSZ
26) SIGVTALRM    27) SIGPROF    28) SIGWINCH    29) SIGIO    30) SIGPWR
31) SIGSYS    34) SIGRTMIN    35) SIGRTMIN+1    36) SIGRTMIN+2    37) SIGRTMIN+3
38) SIGRTMIN+4    39) SIGRTMIN+5    40) SIGRTMIN+6    41) SIGRTMIN+7    42) SIGRTMIN+8
43) SIGRTMIN+9    44) SIGRTMIN+10    45) SIGRTMIN+11    46) SIGRTMIN+12    47) SIGRTMIN+13
48) SIGRTMIN+14    49) SIGRTMIN+15    50) SIGRTMAX-14    51) SIGRTMAX-13    52) SIGRTMAX-12
53) SIGRTMAX-11    54) SIGRTMAX-10    55) SIGRTMAX-9    56) SIGRTMAX-8    57) SIGRTMAX-7
58) SIGRTMAX-6    59) SIGRTMAX-5    60) SIGRTMAX-4    61) SIGRTMAX-3    62) SIGRTMAX-2
63) SIGRTMAX-1    64) SIGRTMAX    
```

 

 

**常用的信号：**

**    1\) SIGHUP     让一个进程不用重启，就可以重读其配置文件，并让新配置生效  
    2\) SIGINT     硬件中断信号。 Ctrl+c  
    9\) SIGKILL    杀死一个进程  
    15\) SIGTERM   终止一个进程  
        
如何调用一个信号：  
      
     信号号码： kill \-9 \<PID> （杀死程序后，要删除交互文件，才能正常恢复）  
     信号名称： kil \-SIGKILL \<PID>  
     信号名称简写：kill \-KILL \<PID>**

**\# kill \<PID>**

**\# killall \<PROCESS\_NAME>    **

```
[root@wei csdn]# killall httpd
```

  
**控制进程的运行方式（前台/后台）  
   
     前台：占用命令提示符**

**（1）控制命令在后台运行**

 

```
[root@wei csdn]# firefox &
```

  
**（2）查看后台的应用程序**

```
[root@wei csdn]# jobs -l

```

**       
（3）将正在运行的指令放入后台，并暂停运行**

  
**             Ctrl+z**

  
**（4）将后台的程序调回前台继续运行**

**\# fg \<后台任务编号>**