---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2022-05-06 17:06:55
description: 首先我们日常运维中，服务器会跑大量的任务。我们可以通和展示整个服务器的内存和磁盘的趋势可以每台部署相应的脚本，可以定位到每个时间段执行的业务，所消耗的各项资源统计前十的消耗应用降序统计前十的内存消耗应。。。。。。。
image: ../../title_pic/43.jpg
slug: '202205061706'
tags:
- Linux实战操作
- 运维
- shell
- linux
title: Linux任务分析脚本
---

<!--more-->

首先我们日常运维中，服务器会跑大量的任务。

（1）我们可以通prometheus和grafana 展示整个服务器的cpu 内存 和磁盘IO的趋势

（2）可以每台部署相应的脚本，可以定位到每个时间段执行的业务，所消耗的各项资源

# 统计前十的CUP消耗应用（降序 ）

```bash
ps aux|head -1 && ps aux|grep -v PID|sort -rn -k +3|head
```

![](../../image/c0b10584b7c74e3ead9efe214b64fab2.png)

# 统计前十的内存消耗应用（降序 ）

```bash
ps aux|head -1 &&  ps aux|grep -v PID|sort -rn -k +4|head
```

# ![](../../image/adc8cabd72284c58bc6575e2234db291.png)统计前十的磁盘IO消耗应用（降序 ）

```bash
/usr/sbin/iotop -btoq --iter=1 |awk 'NR>3{print}'|sort -rn -k 11
```

切记需要安装iotop

![](../../image/096d5156682a41a9bbcf6bf34183479f.png)

# 统计网络状态标识（状态） 

```bash
netstat  -nt | grep -e 127.0.0.1 -e 0.0.0.0 -e ::: -v | awk '/^tcp/ {++state[$NF]} END {for(i in state) print i,"\t",state[i]}'
```

![](../../image/5f5e6644c9d8485ea6a9458caa27355d.png)

#  统计网络状态标识（IP）

```bash
netstat -n | awk '/^tcp/ {print $0}'  | awk '{print $(NF-1),$NF}' |  awk -F ':| ' '{print $1,$NF}' |awk 'BEGIN{print "IP\t\t状态\t次数统计"} {a[$1" "$2]++}END{for(i in a) print(i,a[i])}' |sort -nk 3
```

![](../../image/c8d1612f342f3e22cfad05e7abd808ed.png)

[连接状态\_学习笔记-TCP连接状态解析\_六十度灰的博客-CSDN博客前面两篇详细的给大家介绍过了TCP的三次握手和四次挥手流程\(详见学习笔记-TCP三次握手， 学习笔记-TCP四次挥手 \)，本文主要是介绍在TCP连接过程中的各种状态变化。状态介绍CLOSED:表示初始状态。LISTEN:表示服务器端的某个SOCKET处于，可以接受连接了。SYN\_RCVD:这个状态表示接受到了SYN，在正常情况下，这个状态是服务器端的SOCKET在建立TCP连接时的会话过程中的一个...![](../../image/favicon32.ico.jpg)https://blog.csdn.net/weixin\_31304599/article/details/112671431\?utm\_medium=distribute.pc\_relevant.none-task-blog-2\~default\~baidujs\_baidulandingword\~default-0.pc\_relevant\_default\&spm=1001.2101.3001.4242.1\&utm\_relevant\_index=3](https://blog.csdn.net/weixin_31304599/article/details/112671431?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0.pc_relevant_default&spm=1001.2101.3001.4242.1&utm_relevant_index=3 "连接状态_学习笔记-TCP连接状态解析_六十度灰的博客-CSDN博客")

# 相关脚本

```bash
#!/bin/bash
#时间
time=$(date "+%Y-%m-%d %H:%M:%S")
day=$(date "+%Y-%m-%d")
#首生成日志目录
mkdir -p /system/log/{cpu,mem,io,net}
cpudir='/system/log/cpu'
memdir='/system/log/mem'
iodir='/system/log/io'
netdir='/system/log/net'
#统计前10的cpu
echo "=========================================${time}======================================================" >> ${cpudir}/${day}.log
ps aux|head -1 >> ${cpudir}/${day}.log
ps aux|grep -v PID|sort -rn -k +3|head >> ${cpudir}/${day}.log
#统计前10的内存
echo "=========================================${time}======================================================" >> ${memdir}/${day}.log
ps aux|head -1 >> ${memdir}/${day}.log
ps aux|grep -v PID|sort -rn -k +4|head >> ${memdir}/${day}.log
#统计前10的磁盘io
echo "=========================================${time}======================================================" >> ${iodir}/${day}.log
/usr/sbin/iotop -btoq --iter=1 |head -n 3 >> ${iodir}/${day}.log
/usr/sbin/iotop -btoq --iter=1 |awk 'NR>3{print}'|sort -rn -k 11 >> ${iodir}/${day}.log
#统计机器的网络状态(ip,状态)

echo "=========================================${time}======================================================" >> ${netdir}/${day}.log
netstat  -nt | grep -e 127.0.0.1 -e 0.0.0.0 -e ::: -v | awk '/^tcp/ {++state[$NF]} END {for(i in state) print i,"\t",state[i]}' >> ${netdir}/${day}.log
echo  -n " "  >> ${netdir}/${day}.log
netstat -n | awk '/^tcp/ {print $0}'  | awk '{print $(NF-1),$NF}' |  awk -F ':| ' '{print $1,$NF}' |awk 'BEGIN{print "IP\t\t状态\t次数统计"} {a[$1" "$2]++}END{for(i in a) print(i,a[i])}' |sort -nk 3 >> ${netdir}/${day}.log

#删除老化的文件（保留7天）
find /system/log/ -type f -mtime +7  -exec rm -f {} \;
```

# 设置定时任务

```
#拷贝文件
ansible hadoop -i ./hadoopip -m copy -a "src=/system/check_system.sh dest=/system/check_system.sh " -f 20
#给权限
ansible hadoop -i ./hadoopip -m shell  -a "chmod a+x /system/check_system.sh " -f 20
#安装依赖
 ansible hadoop -i ./hadoopip -m shell  -a "yum install -y iotop " -f 20
#设置定时任务
ansible hadoop -i ./hadoopip -m cron -a "minute=*/5 job='sh /system/check_system.sh' name=check_system disabled=no" -f 20
```

![](../../image/1567b8bc824e42ef99838e47e024f1ac.png)

#  运行结果

![](../../image/f027112e1cea4ee78bf0ae854e5513d4.png)

# 日志格式 

![](../../image/f68b6de6deaf494980f25e7646e80d55.png)

![](../../image/aaa67ceeddef4538be43439caa654105.png)