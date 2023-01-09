+++
author = "南宫乘风"
title = "Linux虚拟机（lvm）报Unmount and run xfs_repair"
date = "2022-03-09 16:39:45"
tags=['linux', '运维', '服务器']
categories=['错误问题解决', ' Linux实战操作']
image = "post/4kdongman/78.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/123380912](https://blog.csdn.net/heian_99/article/details/123380912)

![26026e6e4ee44b2f90bb96bf2941de1f.png](https://img-blog.csdnimg.cn/26026e6e4ee44b2f90bb96bf2941de1f.png)

原因：因为突然断电，导致机器关闭

结果：发现有一台虚拟机无法启动，一直报错 **Unmount and run xfs_repair**

分析：主机异常掉电后里面的虚拟机无法启动，主要是损坏的分区

**解决办法：**

原因：看出来应该是dm-0分区损坏，修复就可以了

1：启动虚拟机E进入单用户模式

![f9c0e1a5f93d4cf3bfb7a794d32ff8bc.png](https://img-blog.csdnimg.cn/f9c0e1a5f93d4cf3bfb7a794d32ff8bc.png)



2：在linux16开头的哪一行后面添加rd.break，ctrl+x进入救援模式

![67f7e52f60bd4486b52ed8438e12c274.png](https://img-blog.csdnimg.cn/67f7e52f60bd4486b52ed8438e12c274.png)

 

3：分析dm-0

```
ls -l /dev/mapper
```

 

![fc4e19ae5524481884e6ea5a2f76236a.png](https://img-blog.csdnimg.cn/fc4e19ae5524481884e6ea5a2f76236a.png)

4:卸载目录

```
umount /dev/mapper/centos-root
```

![c02824361f7e4efa91da5ce61776a3ad.png](https://img-blog.csdnimg.cn/c02824361f7e4efa91da5ce61776a3ad.png)

 5:修复目录

```
xfs_repair -L /dev/mapper/centos-root
```

![aa06491d5580417bb8788c77006c4568.png](https://img-blog.csdnimg.cn/aa06491d5580417bb8788c77006c4568.png)

 6：重启机器

```
init 6
```

修复完成

![ff745f35825943b68cc4d91ce9459013.png](https://img-blog.csdnimg.cn/ff745f35825943b68cc4d91ce9459013.png)

 

```
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




