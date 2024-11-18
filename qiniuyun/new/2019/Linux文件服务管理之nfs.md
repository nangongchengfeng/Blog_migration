---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-02-04 19:56:38
description: 即网络文件系统，是支持的文件系统中的一种，它允许网络中的计算机之间通过网络共享资源。在的应用中，本地的客户端应用可以透明地读写位于远端服务器上的文件，就像访问本地文件一样。网络文件系统作用：在服务器间。。。。。。。
image: http://image.ownit.top/4kdongman/32.jpg
tags:
- linux
title: Linux文件服务管理之nfs
---

<!--more-->

**NFS（Network File System）即网络文件系统，  
是FreeBSD支持的文件系统中的一种，它允许网络中的计算机之间通过TCP/IP网络共享资源。  
在NFS的应用中，本地NFS的客户端应用可以透明地读写位于远端NFS服务器上的文件，就像访问本地文件一样。**

**NFS              \-----------Network File Syste    网络文件系统**

  
**作用：在Linux服务器间实现数据共享**

**软件：nfs-utils  
      rpcbind  
       
目录导出文件----/etc/exports**

**文件格式：**

  
**       目录名称    客户端地址（权限）  
         
       客户端地址：  
                 IP地址：192.168.196.131  
                 网关：192.168.196.0/24  
        权限：  
             ro         只读  
             rw         读写  
             sync       同步  
             async      异步  
               
            all\_squash             客户端所有用户上传的文件的所属均为nfsnobody  
             root\_squash            客户端root用户上传的文件的所属会被映射为nfsnobody  
             no\_root\_squash         客户端root用户上传的文件所属仍为root  
               
             anonuid=\<number>  
             anongid=\<number>  
  **

## **Linux服务器：192.168.196.131**

## **Linux客户端：192.168.196.131**

**            
示例：  
    通过nfs共享本地目录/wedata 允许192.168.196.132以只读方式挂载**

  
**（1）安装软件**

```
[root@wei ~]# yum -y install rpcbind nfs-utils
```

**（2）创建文件**

```
[root@wei ~]# mkdir /wedata
[root@wei ~]# touch /wedata/{1..10}.html
```

**（3）修改配置文件/etc/exports**

```
[root@wei ~]# vim /etc/exports
```

```
/wedata    192.168.196.132(ro)

```

  
**（4）重启服务**

```
[root@wei ~]# systemctl restart rpcbind
[root@wei ~]# systemctl restart nfs-server
```

或者下面的命令

![](http://image.ownit.top/csdn/20190204195131540.png)

 

**（5）查看本地共享目录**

```
[root@wei ~]# showmount -e localhost
Export list for localhost:
/wedata 192.168.196.132
```

**（6）客户端访问（软件也需要安装）**

```
[root@zhang ~]# mount 192.168.196.131:/wedata /web/
[root@zhang ~]# ls /web/
10.html  1.html  2.html  3.html  4.html  5.html  6.html  7.html  8.html  9.html
```

  
**设置为开机挂载    
        修改配置文件/etc/fstab   
        **

```
[root@zhang ~]# vim /etc/fstab 
```

```
    192.168.196.131:/wedata   /web  nfs defaults 0 0
```

![](http://image.ownit.top/csdn/20190204195305806.png)

![](http://image.ownit.top/csdn/20190204195424733.png)

至于权限修改，根据情况可以来修改

![](http://image.ownit.top/csdn/20190204195620309.png)