+++
author = "南宫乘风"
title = "Centos7集群时间同步（Chrony）"
date = "2020-04-20 11:50:43"
tags=['时间同步', '集群', 'Centos7', 'Linux']
categories=[' Linux实战操作']
image = "post/4kdongman/73.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/105631692](https://blog.csdn.net/heian_99/article/details/105631692)

### 概述

集群对时间同步要求高，实际使用环境中必须确保集群中所有系统时间保持一致

Chrony是一个开源的自由软件，像CentOS 7或基于RHEL 7操作系统，已经是默认服务，默认配置文件在 /etc/chrony.conf 它能保持系统时间与时间服务器（NTP）同步，让时间始终保持同步。相对于NTP时间同步软件，占据很大优势。

![20200420111940887.png](https://img-blog.csdnimg.cn/20200420111940887.png)

需要注意的是，配置完/etc/chrony.conf后，需重启chrony服务，否则可能会不生效
|主机名称|IP地址
|Master|192.168.1.10
|Node1|192.168.1.20
|Node2|192.168.1.30

![20200420112112851.png](https://img-blog.csdnimg.cn/20200420112112851.png)

### 1、安装chrony

CentOS7中已经默认安装了chrony，其配置文件路径在

```
/etc/chrony.conf
```

如果系统内没有chrony，请按照如下进行安装，启动并检查相关状态

```
 yum install chrony -y

systemctl enable chronyd.service
systemctl restart chronyd.service
systemctl status chronyd.service
```

在防火墙内放行，因NTP使用123/UDP端口协议，所以允许NTP服务即可。（如果已关闭防火墙请无视）

```
firewall-cmd --add-service=ntp --permanent
firewall-cmd --reload
```

### 2、检查设置时区

![20200420112313217.png](https://img-blog.csdnimg.cn/20200420112313217.png)

```
# timedatectl
      Local time: Fri 2018-2-29 13:31:04 CST
  Universal time: Fri 2018-2-29 05:31:04 UTC
        RTC time: Fri 2018-2-29 08:17:20
       Time zone: Asia/Shanghai (CST, +0800)
     NTP enabled: yes
NTP synchronized: yes
 RTC in local TZ: no
      DST active: n/a

#如果你当前的时区不正确，请按照以下操作设置。

#查看所有可用的时区：

# timedatectl list-timezones

#筛选式查看在亚洲S开的上海可用时区：

# timedatectl list-timezones |  grep  -E "Asia/S.*"

Asia/Sakhalin
Asia/Samarkand
Asia/Seoul
Asia/Shanghai
Asia/Singapore
Asia/Srednekolymsk

#设置当前系统为Asia/Shanghai上海时区：

# timedatectl set-timezone Asia/Shanghai

#设置完时区后，强制同步下系统时钟：

# chronyc -a makestep
200 OK
```

### 3、Master节点配置chrony

此处选用的是阿里云的ntp服务server，地址为

```
ntp1.aliyun.com
```

当前是Master，ip地址为**192.168.1.10**，网段是**192.168.1.0/24**，配置详情如下，红色为更改部分

```
vim /etc/chrony.conf


server ntp1.aliyun.com iburst

# Record the rate at which the system clock gains/losses time.
driftfile /var/lib/chrony/drift

# Allow the system clock to be stepped in the first three updates
# if its offset is larger than 1 second.
makestep 1.0 3

# Enable kernel synchronization of the real-time clock (RTC).
rtcsync

# Enable hardware timestamping on all interfaces that support it.
#hwtimestamp *

# Increase the minimum number of selectable sources required to adjust
# the system clock.
#minsources 2

# Allow NTP client access from local network.
#allow 192.168.0.0/16
allow 192.168.1.0/24

# Serve time even if not synchronized to a time source.
local stratum 10

# Specify file containing keys for NTP authentication.
#keyfile /etc/chrony.keys

# Specify directory for log files.
logdir /var/log/chrony

# Select which information is logged.
#log measurements statistics tracking

```

**重启**

```
# systemctl restart chronyd.service
# systemctl status chronyd.service
```

![20200420112830302.png](https://img-blog.csdnimg.cn/20200420112830302.png)

```
强制同步下系统时钟：
# chronyc -a makestep

查看时间同步源状态：
# chronyc sourcestats

查看时间同步源：
# chronyc sources -v
```

![20200420113129524.png](https://img-blog.csdnimg.cn/20200420113129524.png)

### 4、Node节点配置chrony

**node节点**(192.168.26.136)只需要注释掉原来的ip，新增Master主机的IP地址即可（记得**重启**chrony服务）

![20200420113245814.png](https://img-blog.csdnimg.cn/20200420113245814.png)

```
# systemctl restart chronyd.service
# systemctl status chronyd.service
```

![20200420113321607.png](https://img-blog.csdnimg.cn/20200420113321607.png)

```
强制同步下系统时钟：
# chronyc -a makestep

查看时间同步源状态：
# chronyc sourcestats

查看时间同步源：
# chronyc sources -v
```

![2020042011341518.png](https://img-blog.csdnimg.cn/2020042011341518.png)

**Node2也是以上步骤**

 

### 5、 chrony.conf文件详解

**以下是系统默认配置文件的说明(CentOS7)，了解一下各个配置是做什么。**

```
# 使用pool.ntp.org项目中的公共服务器。以server开，理论上你想添加多少时间服务器都可以。
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
server 0.centos.pool.ntp.org iburst
server 1.centos.pool.ntp.org iburst
server 2.centos.pool.ntp.org iburst
server 3.centos.pool.ntp.org iburst

# 根据实际时间计算出服务器增减时间的比率，然后记录到一个文件中，在系统重启后为系统做出最佳时间补偿调整。
driftfile /var/lib/chrony/drift

# chronyd根据需求减慢或加速时间调整，
# 在某些情况下系统时钟可能漂移过快，导致时间调整用时过长。
# 该指令强制chronyd调整时期，大于某个阀值时步进调整系统时钟。
# 只有在因chronyd启动时间超过指定的限制时（可使用负值来禁用限制）没有更多时钟更新时才生效。
makestep 1.0 3

# 将启用一个内核模式，在该模式中，系统时间每11分钟会拷贝到实时时钟（RTC）。
rtcsync

# Enable hardware timestamping on all interfaces that support it.
# 通过使用hwtimestamp指令启用硬件时间戳
#hwtimestamp eth0
#hwtimestamp eth1
#hwtimestamp *

# Increase the minimum number of selectable sources required to adjust
# the system clock.
#minsources 2

# 指定一台主机、子网，或者网络以允许或拒绝NTP连接到扮演时钟服务器的机器
#allow 192.168.0.0/16
#deny 192.168/16

# Serve time even if not synchronized to a time source.
local stratum 10

# 指定包含NTP验证密钥的文件。
#keyfile /etc/chrony.keys

# 指定日志文件的目录。
logdir /var/log/chrony

# Select which information is logged.
#log measurements statistics tracking
```

![20200420114231122.png](https://img-blog.csdnimg.cn/20200420114231122.png)

![2020042011425943.png](https://img-blog.csdnimg.cn/2020042011425943.png)

### 6、chrony的优势

chrony的优势更快的同步只需要数分钟而非数小时时间，从而最大程度减少了时间和频率误差，这对于并非全天 24 小时运行的台式计算机或系统而言非常有用。

能够更好地响应时钟频率的快速变化，这对于具备不稳定时钟的虚拟机或导致时钟频率发生变化的节能技术而言非常有用。

在初始同步后，它不会停止时钟，以防对需要系统时间保持单调的应用程序造成影响。

在应对临时非对称延迟时（例如，在大规模下载造成链接饱和时）提供了更好的稳定性。

无需对服务器进行定期轮询，因此具备间歇性网络连接的系统仍然可以快速同步时钟。

![20200420114950310.png](https://img-blog.csdnimg.cn/20200420114950310.png)

 

 
