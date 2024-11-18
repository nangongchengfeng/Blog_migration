---
author: 南宫乘风
categories:
- 错误问题解决
date: 2022-03-09 16:39:45
description: 原因：因为突然断电，导致机器关闭结果：发现有一台虚拟机无法启动，一直报错分析：主机异常掉电后里面的虚拟机无法启动，主要是损坏的分区解决办法：原因：看出来应该是分区损坏，修复就可以了：启动虚拟机进入单用。。。。。。。
image: ../../title_pic/32.jpg
slug: '202203091639'
tags:
- Linux实战操作
- linux
- 运维
- 服务器
title: Linux虚拟机（lvm）报Unmount and run xfs_repair
---

<!--more-->

![](../../image/26026e6e4ee44b2f90bb96bf2941de1f.png)

原因：因为突然断电，导致机器关闭

结果：发现有一台虚拟机无法启动，一直报错 **Unmount and run xfs\_repair**

分析：主机异常掉电后里面的虚拟机无法启动，主要是损坏的分区

**解决办法：**

原因：看出来应该是dm-0分区损坏，修复就可以了

1：启动虚拟机E进入单用户模式

![](../../image/f9c0e1a5f93d4cf3bfb7a794d32ff8bc.png)

2：在linux16开头的哪一行后面添加rd.break，ctrl+x进入救援模式

![](../../image/67f7e52f60bd4486b52ed8438e12c274.png)

 

3：分析dm-0

```bash
ls -l /dev/mapper
```

 

![](../../image/fc4e19ae5524481884e6ea5a2f76236a.png)

4:卸载目录

```
umount /dev/mapper/centos-root
```

![](../../image/c02824361f7e4efa91da5ce61776a3ad.png)

 5:修复目录

```bash
xfs_repair -L /dev/mapper/centos-root
```

![](../../image/aa06491d5580417bb8788c77006c4568.png)

 6：重启机器

```bash
init 6
```

修复完成

![](../../image/ff745f35825943b68cc4d91ce9459013.png)

 

```bash
xfs_repair -h
xfs_repair: invalid option -- 'h'
Usage: xfs_repair [options] device

Options:
-f The device is a file
-L Force log zeroing. Do this as a last resort.
-l logdev Specifies the device where the external log resides.
-m maxmem Maximum amount of memory to be used in megabytes.
-n No modify mode, just checks the filesystem for damage.
-P Disables prefetching.
-r rtdev Specifies the device where the realtime section resides.
-v Verbose output.
-c subopts Change filesystem parameters - use xfs_admin.
-o subopts Override default behaviour, refer to man page.
-t interval Reporting interval in minutes.
-d Repair dangerously.
-V Reports version and exits.
```