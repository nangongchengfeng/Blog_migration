---
author: 南宫乘风
categories:
- Linux基础
date: 2019-01-26 15:18:19
description: 书山有路勤为径，学海无涯苦作舟自学已经有几天了，感觉还可以。坚持下去，就会有收获。每个系统都用相应的软件的管理，也不例外。下面讲解的管理软件。软件管理：：二进制格式软件源码软件软件管理光盘镜像文件软件。。。。。。。
image: ../../title_pic/19.jpg
slug: '201901261518'
tags:
- linux
title: Linux的rpm管理
---

<!--more-->

# **                        书山有路勤为径，学海无涯苦作舟**

 

**自学linux已经有几天了，感觉还可以。坚持下去，就会有收获。**

**每个系统都用相应的软件的管理，Linux也不例外。下面讲解Linux 的rpm管理软件。**

 

**Linux软件管理**

**    windows：.exe  .mai  
         
    centos/RHEL/Fedoea  ：二进制格式软件\(\*.rpm\)      redhat package management  
                                              源码软件\(\*.tar.gz , \*.tar.bz2\)   
    **

**rpm软件管理**

**     光盘iso镜像文件  
         
rpm软件名称的组成  
      
     zlib-devel-1.2.7-17.el7.x86\_64.rpm  
       
     zlib-devel：软件名称  
     1.2.7：版本  
     el7.x86\_64 ： 软件运行平台  
     el7.noarch ： 无系统架构，可以安装任何版本**

**下面的两个网站可以下载rpm包（网站是国外的，可能比较慢）**

**rpm下载：                          https://pkgs.org/  
        
 rpm下载：                        http://rpmfind.net/**

 

**注意：你下载的rpm包要对应你服务器的版本号和运行平台**

 

## **查看系统平台信息**

```
[root@wei ~]# uname -r
```

**![](../../image/20190126145759719.png)**

 

# **注意：本地系统没有rpm软件包，那么只能挂载iso镜像文件**

**（1）有和运行平台相对应的iso镜像文件（我的centos7的）**

**![](../../image/20190126150352248.png)**

**（2）设置虚拟机，加载镜像文件**

**![](../../image/20190126150546255.png)**

 

**（3）光盘挂载**

```
[root@wei dev]# mount /dev/sr0 /mnt/
```

  
**![](../../image/201901261510333.png)**

  
**光盘卸载**

```
[root@wei dev]# umount /dev/sr0 
```

  
**![](../../image/20190126151142850.png)**

 

 

**管理rpm软件**

**1.查询软件是否安装**

**\# rpm \-q 软件名称**

![](../../image/20190126151323714.png)

**\# rpm \-qa | grep 软件名称**

![](../../image/20190126151403364.png)

**2.查询软件的说明信息**

**#rpm \-qi 软件名称**

![](../../image/2019012615144295.png)

**3.查看软件生成的文件**

**\# rpm \-ql 软件名称**

![](../../image/20190126151533822.png)

  
**\[root\@wei \~\]# rpm \-ql bash | less**

  
**4.查看文件由那个软件生成**

**\# rpm \-qf 文件名称**

```
[root@wei ~]# which chmod
/usr/bin/chmod
[root@wei ~]# rpm -qf /usr/bin/chmod 
coreutils-8.22-21.el7.x86_64
```

![](../../image/20190126151637953.png)

  
**5.查看软件的配置文件**

**\# rpm \-qc 软件名称**

```
[root@wei ~]# rpm -qc vim-enhanced
/etc/profile.d/vim.csh
/etc/profile.d/vim.sh
```

  
**管理操作：**

**（1）安装软件**

**\# rpm \-ivh 软件安装包名称  
          
         i: 安装 install  
         v：显示详细信息 verbose  
         h：显示软件安装进度  
           
安装vsftpd软件**

```
[root@wei ~]# mount /dev/sr0 /mnt/

[root@wei ~]# rpm -ivh /mnt/Packages/vsftpd-3.0.2-22.el7.x86_64.rpm 
准备中...                          ################################# [100%]
正在升级/安装...
   1:vsftpd-3.0.2-22.el7              ################################# [100%]
```

  
**安装dhcp软件**

```
[root@wei ~]# rpm -ivh /mnt/Packages/dhcp-4.2.5-68.el7.centos.x86_64.rpm 
准备中...                          ################################# [100%]
正在升级/安装...
   1:dhcp-12:4.2.5-68.el7.centos      ################################# [100%]
```

**安装软件出现依赖问题**

**    选项--nodeps 忽略依赖关系安装  
    **

**（2）卸载软件**

**\# rpm \-e 软件名称**

 

```
[root@wei ~]# rpm -q dhcp
dhcp-4.2.5-68.el7.centos.x86_64
[root@wei ~]# rpm -e dhcp
[root@wei ~]# rpm -q dhcp
未安装软件包 dhcp 
```

**选项--nodeps 忽略依赖关系卸载**

**（3）升级软件**

**\# rpm \-Uvh 软件安装包名称**

**       注意：自动卸载就版本软件**