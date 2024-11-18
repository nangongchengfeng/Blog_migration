---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-03 16:49:46
description: 系统中一切皆文件。有文件，当然少不了目录。目录和目录有着很大的不同，目录类似一个树，最顶层是其根目录。在此我介绍一下初学者需要先了解的目录，关于跟高深的目录，后期会做出相应的讲解根目录用户的家目录宿主。。。。。。。
image: ../../title_pic/37.jpg
slug: '201901031649'
tags:
- linux
title: linux目录结构
---

<!--more-->

**linux系统中一切皆文件。**

**有文件，当然少不了目录。**

**Linux目录和Windows目录有着很大的不同，Linux目录类似一个树，最顶层是其根目录。**

**![](../../image/20190103163530210.png)**

**在此我介绍一下初学者需要先了解的linux目录，关于跟高深的linux目录，后期会做出相应的讲解 **

<table border="1" cellpadding="1" cellspacing="1" style="width:500px;"><tbody><tr><td><strong>/</strong></td><td><strong>根目录</strong></td></tr><tr><td><strong>/root</strong></td><td><strong>root用户的家目录/宿主目录</strong></td></tr><tr><td><strong>/boot</strong></td><td><strong>启动分区（内核，启动配置文件）</strong></td></tr><tr><td><strong>/dev</strong></td><td><strong>设备文件目录</strong></td></tr><tr><td><strong>/proc,/sys</strong></td><td><strong>为根系统</strong></td></tr><tr><td><strong>/etc</strong></td><td><strong>应用程序的配置文件 &nbsp;&nbsp; *.conf</strong></td></tr><tr><td><strong>/home</strong></td><td><strong>普通用户的家目录/宿主目录</strong></td></tr><tr><td><strong>带有/bin,/sbin</strong></td><td><strong>可执行程序（二进制程序）</strong></td></tr><tr><td><strong>/var</strong></td><td><strong>放置系统执行过程中经常变化的文件，如随时更改的日志文件</strong></td></tr><tr><td><strong>/tmp</strong></td><td><strong>存放临时文件目录，一些命令和应用程序会用的到这个目录</strong></td></tr></tbody></table>

**/：**根目录，位于Linux文件系统目录结构的顶层，一般根目录下只存放目录，不要存放文件，/etc、/bin、/dev、/lib、/sbin应该和根目录放置在一个分区中。  
**/bin，/usr/bin**：该目录为命令文件目录，也称为二进制目录。包含了供系统管理员及普通用户使用的重要的linux命令和二进制（可执行）文件，包含shell解释器等。  
/boot： 该目录中存放系统的内核文件和引导装载程序文件，/boot/vmlinuz为linux的内核文件，以及/boot/gurb。建议单独分区，分区大小100M即可。  
**/dev**： 设备（device）文件目录，存放linux系统下的设备文件，访问该目录下某个文件，相当于访问某个设备，存放连接到计算机上的设备（终端、磁盘驱动器、光驱及网卡等）的对应文件，包括字符设备和块设备等，常用的是挂载光驱mount /dev/cdrom/mnt。   
**/etc**： 系统配置文件存放的目录，该目录存放系统的大部分配置文件和子目录，不建议在此目录下存放可执行文件，重要的配置文件有/etc/inittab、/etc/fstab、/etc/init.d、/etc/X11（X Window系统有关）、/etc/sysconfig（与网络有关）、/etc/xinetd.d修改配置文件之前记得备份。该目录下的文件由系统管理员来使用，普通用户对大部分文件有只读权限。  
**/home**： 系统默认的用户宿主目录，新增用户账号时，用户的宿主目录都存放在此目录下，\~表示当前用户的宿主目录，\~test表示用户test的宿主目录。建议单独分区，并设置较大的磁盘空间，方便用户存放数据。  
**/lib，/usr/lib，/usr/local/lib**：系统使用的函数库的目录，程序在执行过程中，需要调用一些额外的参数时需要函数库的协助，该目录下存放了各种编程语言库。典型的linux系统包含了C、C++和FORTRAN语言的库文件。/lib目录下的库映像文件可以用来启动系统并执行一些命令，目录/lib/modules包含了可加载的内核模块，/lib目录存放了所有重要的库文件，其他的库文件则大部分存放在/usr/lib目录下。  
**/proc**： 此目录的数据都在内存中，如系统核心，外部设备，网络状态，由于数据都存放于内存中，所以不占用磁盘空间，比较重要的目录有/proc/cpuinfo、/proc/interrupts、/proc/dma、/proc/ioports、/proc/net/\*等。  
**/root**：系统管理员root的宿主目录，系统第一个启动的分区为/，所以最好将/root和/放置在一个分区下。  
**/sbin，/usr/sbin，/usr/local/sbin**：放置系统管理员使用的可执行命令，如fdisk、shutdown、mount等。与/bin不同的是，这几个目录是给系统管理员root使用的命令，一般用户只能"查看"而不能设置和使用。  
**/usr**： 应用程序存放目录，/usr/bin 存放应用程序， /usr/share 存放共享数据，/usr/lib  
 存放不能直接运行的，却是许多程序运行所必需的一些函数库文件，/usr/local 存放软件升级包，/usr/share/doc 系统说明文件存放目录。  
**/usr/share/man**:  程序说明文件存放目录，使用 man ls时会查询/usr/share/man/man1/ls.1.gz的内容建议单独分区，设置较大的磁盘空间。  
**/var**： 放置系统执行过程中经常变化的文件，如随时更改的日志文件 /var/log。/var/log/message：  
 所有的登录文件存放目录。/var/spool/mail： 邮件存放的目录。 /var/run: 程序或服务启动后。建议单独分区，设置较大的磁盘空间。  
**/tmp**：存放临时文件目录，一些命令和应用程序会用的到这个目录。该目录下的所有文件会被定时删除，以避免临时文件占满整个磁盘。