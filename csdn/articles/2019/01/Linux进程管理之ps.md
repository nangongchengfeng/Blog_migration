+++
author = "南宫乘风"
title = "Linux进程管理之ps"
date = "2019-01-29 16:45:00"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/56.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86691863](https://blog.csdn.net/heian_99/article/details/86691863)

 

**[Linux](http://lib.csdn.net/base/linux) 是一种动态系统，能够适应不断变化的计算需求。****下面介绍一些 Linux 所提供的工具来进行进程的查看与控制，掌握这些让我们能在某些进程出现异常的时候及时查看相关的指标，从而解决问题。**

 

<br>**进程管理**

**进程   process<br>        <br>        某应用程序打开的进程<br>        PID         Process ID<br>        <br>        类型：<br>             用户空间进程<br>             内核空间进程**

<br>**用户空间进程：通过执行用户程序、应用程序或内核之外的系统程序而产生的进程，此类进程可以在用户的控制下运行或关闭。**

**内核空间进程：可以执行内存资源分配和进程切换等管理工作；而且，该进程的运行不受用户的干预，即使是root用户也不能干预系统进程的运行**。

 

静态查看进程状态

```
# ps
 
[root@wei csdn]# ps                &gt;&gt;&gt;&gt;查看本终端的进程
   PID TTY          TIME CMD
  1806 pts/1    00:00:00 bash
  2805 pts/1    00:00:00 ps

```

选项的使用方式：

        BSD风格：选项没有横线-        ps aux<br>         SysV风格：选项需要带有横线-   ps -elf<br>         <br>         <br> BSD风格：<br>        <br>        a ：显示与终端相关的进程<br>        u : 显示启动进程的用户<br>        x ：显示与终端无关的程序<br>        

```
# ps a

# ps u

# ps x
```

```

[root@wei csdn]# ps u
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root       1343  0.0  0.2 115436  2032 pts/0    Ss+  19:59   0:00 -bash
root       1674  0.0  0.2 115432  2032 tty1     Ss+  20:01   0:00 -bash
```

 
|USER|运行进程的用户
|%CPU|进程所占欧诺个的CPU百分比
| %MEM |进程所占用的MEM百分比
|VSZ |虚拟内存集，进程独有的内存+共享存在
|PSS|进程独有的内存

 

STAT    进程的状态

      D: 不可中断的睡眠（等待磁盘IO完成）<br>       S：可中断的睡眠（不需要等待磁盘IO完成）<br>       R：运行或就绪<br>       T: 停止<br>       Z：僵死  Zombie

      &lt; :高优先级进程<br>           会被CPU优先执行<br>           会获取更多的CPU执行时间          <br>     <br>       N:低优先级进程<br>       +：前台进程组中的进程<br>       l:多线程进程（Thread）<br>       s：会话进程首进程，某一个连接的父进程

```
[root@wei csdn]# ps aux |less
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.1  0.6 127940  6580 ?        Ss   19:58   0:03 /usr/lib/systemd/systemd --switched-root --system --deserialize 22
root          2  0.0  0.0      0     0 ?        S    19:58   0:00 [kthreadd]
root          3  0.0  0.0      0     0 ?        S    19:58   0:00 [ksoftirqd/0]
root          5  0.0  0.0      0     0 ?        S&lt;   19:58   0:00 [kworker/0:0H]
```

** 带有方括号为系统进程（Linux内核启动）<br>    无方括号的（用户进程）**

<br> SysV风格选项：<br>          <br>           -e  显示所有进程<br>           -l  详细信息<br>           -f  以长格式显示（更多字段类容）

```
[root@wei csdn]# ps -elf | less
F S UID         PID   PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
4 S root          1      0  0  80   0 - 31985 ep_pol 19:58 ?        00:00:04 /usr/lib/systemd/systemd --switched-root --system --deserialize 22
1 S root          2      0  0  80   0 -     0 kthrea 19:58 ?        00:00:00 [kthreadd]
1 S root          3      2  0  80   0 -     0 smpboo 19:58 ?        00:00:01 [ksoftirqd/0]
	
```

进程优先级：<br>       0---139<br>       <br>       数据越小，越先级越高<br>       <br> 高优先级进程：<br>     会获取CPU更多的执行时间<br>     会被CPU优先执行<br>     <br> nice值：<br>     新优先级=旧优先级——nice值<br>     <br>     -20----19<br>     <br>     普通用户仅能够调大nice值，既降低进程优先级<br>     root用户可以随意调整nice值<br>     <br> 显示进程树

```
[root@wei csdn]# yum install psmisc  #  安装显示pstree的命令包

[root@wei csdn]# pstree
systemd─┬─NetworkManager───2*[{NetworkManager}]
        ├─VGAuthService
        ├─auditd───{auditd}
        ├─crond
        ├─dbus-daemon───{dbus-daemon}
        ├─login───bash
        ├─lvmetad
        ├─master─┬─pickup
        │        └─qmgr
        ├─mysqld_safe───mysqld───21*[{mysqld}]
        ├─polkitd───5*[{polkitd}]
        ├─rsyslogd───2*[{rsyslogd}]
        ├─sshd─┬─2*[sshd───bash]
        │      └─sshd───bash───pstree
        ├─systemd-journal
        ├─systemd-logind
        ├─systemd-udevd
        ├─tuned───4*[{tuned}]
        └─vmtoolsd───{vmtoolsd}

```

 

```
[root@wei csdn]# ps aux | grep vim
root       2917  0.2  0.5 151600  5136 pts/2    S+   21:39   0:00 vim list
root       2925  0.0  0.0 112720   984 pts/1    R+   21:43   0:00 grep --color=auto vim
[root@wei csdn]# pidof vim
2917
[root@wei csdn]# pidof bash
1828 1806 1674 1343
```

 

 

 

 

 

 

 

 
