+++
author = "南宫乘风"
title = "Shell帮你掌管上千台服务（多线程）"
date = "2021-06-09 20:42:08"
tags=['linux', '队列', 'shell']
categories=['Linux Shell', ' 企业级-Shell脚本案例']
image = "post/4kdongman/59.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/117753840](https://blog.csdn.net/heian_99/article/details/117753840)

## Shell帮你掌管上千台服务（多线程）

日常服务器运维时，我们都会批量管理多台服务器。

脚本，批量化，使我们工作中必不可少的。

首先我们需要一台堡垒机，负责免秘钥的登录和分发任务等等

**堡垒机到主机**

需要一套ssh-keygen来管理

![20210609203330757.png](https://img-blog.csdnimg.cn/20210609203330757.png)
1. authorized_keys： 授权密钥  1. id_rsa  ：私钥  1. id_rsa.pub  ：公钥  1. known_hosts：连接过机器记录信息，不需要属于“yes”  
这些都是前面基础环境和工作。

## 默认脚本

这个脚本是最初始化的，可以远程过去执行任务，并打印结果

```
#/bin/bash  
START_TIME=`date +%s`  
for i in `cat /opt/wei/pam_ip.txt`  #ip存放的文件
do  
    cc="ssh deployer@$i \"sudo cat /etc/ssh/sshd_config | grep -Ev '^#' | grep UsePAM\" " 
        kk=`echo $cc|bash`  
        if [ ! -n "$kk" ]; then  
          echo "IP: $i UsePAM no seting"  
          sudo echo "IP: $i UsePAM no seting" &gt;&gt; /opt/wei/pam_no.txt  
        else  
          echo "IP: $i  $kk"   
          sudo echo "IP: $i  $kk" &gt;&gt; /opt/wei/pam_yes.txt  
        fi  
done  
END_TIME=`date +%s`  
EXECUTING_TIME=`expr $END_TIME - $START_TIME`  
echo "================end====================="  
echo "程序运行时长：$EXECUTING_TIME S" 

```

## ![20210609203846700.png](https://img-blog.csdnimg.cn/20210609203846700.png)

## 脚本优化（加入线程概念）

```
#/bin/bash  
START_TIME=`date +%s`  
for i in `cat /opt/wei/pam_ip.txt`  
do  
{    cc="ssh deployer@$i \"sudo cat /etc/ssh/sshd_config | grep -Ev '^#' | grep UsePAM\" "  
        kk=`echo $cc|bash`  
        if [ ! -n "$kk" ]; then  
          echo "IP: $i UsePAM no seting"  
          sudo echo "IP: $i UsePAM no seting" &gt;&gt; /opt/wei/pam_no.txt  
        else  
          echo "IP: $i  $kk"   
          sudo echo "IP: $i  $kk" &gt;&gt; /opt/we/pam_yes.txt  
        fi  
}&amp;  
done  
wait  
END_TIME=`date +%s`  
EXECUTING_TIME=`expr $END_TIME - $START_TIME`  
echo "================end====================="  
echo "程序运行：$EXECUTING_TIME S"  

```

**使用****'&amp;'+wait ****实现****“****多进程****”****实现**

>  
 运行很快，而且很不老实（顺序都乱了,大概是因为expr运算所花时间不同） 
 解析：这一个脚本的变化是在命令后面增加了&amp;标记，意思是将进程扔到后台。在shell中，后台命令之间是不区分先来后到关系的。所以各后台子进程会抢夺资源进行运算。 
 wait命令： 
 wait  [n] 
 n 表示当前shell中某个执行的后台命令的pid，wait命令会等待该后台进程执行完毕才允许下一个shell语句执行；如果没指定则代表当前shell后台执行的语句，wait会等待到所有的后台程序执行完毕为止。 
 如果没有wait，后面的shell语句是不会等待后台进程的，一些对前面后台进程有依赖关系的命令执行就不正确了 


![20210609203837964.png](https://img-blog.csdnimg.cn/20210609203837964.png)

## 自定义线程数

```
#!/bin/bash  
Nproc=20 #最大并发进程数  
function PushQue { #将PID值追加到队列中  
    Que="$Que $1"  
    Nrun=$(($Nrun+1))  
}  
function GenQue { #更新队列信息，先清空队列信息，然后检索生成新的队列信息  
    OldQue=$Que  
    Que=""; Nrun=0  
    for PID in $OldQue; do  
    if [[ -d /proc/$PID ]]; then  
    PushQue $PID  
    fi  
    done  
}  
function ChkQue { #检查队列信息，如果有已经结束了的进程的PID，那么更新队列信息  
    OldQue=$Que  
    for PID in $OldQue; do  
    if [[ ! -d /proc/$PID ]]; then  
    GenQue; break  
    fi  
    done  
}  
for i in `cat /opt/wei/pam_ip.txt`  
do  
{  
    cc="ssh deployer@$i \"sudo cat /etc/ssh/sshd_config | grep -Ev '^#' | grep UsePAM\" "  
    kk=`echo $cc|bash`  
    if [ ! -n "$kk" ]; then  
      echo "IP: $i UsePAM no seting"  
      sudo echo "IP: $i UsePAM no seting" &gt;&gt; /opt/wei/pam_no.txt  
    else  
      echo "IP: $i  $kk"   
      sudo echo "IP: $i  $kk" &gt;&gt; /opt/wei/pam_yes.txt  
    fi  
}&amp;  
    sleep 0.1  #考虑有序，开启这个参数，速度优先，则注释掉
    PID=$!  
    PushQue $PID  
    while [[ $Nrun -ge $Nproc ]]; do # 如果Nrun大于Nproc，就一直ChkQue  
        ChkQue  
        sleep 0.1  
        done  
done  
wait  
echo -e "time-consuming: $SECONDS seconds" #显示脚本执行耗时#!/bin/bash  

```

**使用模拟队列来控制进程数量**

>  
 要控制后台同一时刻的进程数量，需要在原有循环的基础上增加管理机制。 
 一个方法是以for循环的子进程PID做为队列元素，模拟一个限定最大进程数的队列（只是一个长度固定的数组，并不是真实的队列）。队列的初始长度为0，循环每创建一个进程，就让队列长度+1。当队列长度到达设置的并发进程限制数之后，每隔一段时间检查队列，如果队列长度还是等于限制值，那么不做操作，继续轮询；如果检测到有并发进程执行结束了，那么队列长度-1，轮询检测到队列长度小于限制值后，会启动下一个待执行的进程，直至所有等待执行的并发进程全部执行完。 


定义20线程，速度从原来的311S，降到40S，大大提高效率

![20210609204036133.png](https://img-blog.csdnimg.cn/20210609204036133.png)
