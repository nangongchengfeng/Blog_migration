---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-02-03 20:38:40
description: 文件服务器的搭建服务作用：共享目录软件：服务器，客户端配置文件：服务：端口：提供文件共享功能提供解析计算机名称配置文件：全局配置设置工作组名称显示软件版本信息？服务监听的地址设置仅允许那些主机访问拒绝。。。。。。。
image: http://image.ownit.top/4kdongman/36.jpg
tags:
- linux
title: Linux文件服务管理之Samba
---

<!--more-->

 

Linux文件服务器的搭建  
       
     Samba  
     vsftpd  
     nfs  
       
Samba服务  
      ![](http://image.ownit.top/csdn/2019020319415694.png)  
        
      作用：共享目录  
      软件：Samba 服务器 ，Samba-client 客户端  
      配置文件：/etc/smaba/smb.conf  
      服务：smb,nmb  
      端口：smb \--->139/tcp , 445/tcp  提供文件共享功能  
            nmb \--->137/udp , 138/udp  提供解析计算机名称  
              
配置文件：/etc/smaba/smb.conf

全局配置  
       
       
      workgroup = SAMBA      \---设置工作组名称  
      server string =Samba Server Version \%v   \----显示samba软件版本信息  
        
      interface = lo eth0 192.168.196.131？24   \---samba服务监听的ip地址  
        
      hosts allow=127.192.168.12 192.168.196.0  \-----设置仅允许那些主机访问  
      hosts deny=192.168.12.  192.168.1.1/24     \-----拒绝那些主机访问  
        
      security =user     \-------基于用户认证访问  
                share    \-------匿名访问  
                  
                  
共享目录配置  
       \[共享名称\]  
         
           comment=                ====描述信息  
           path = /bj              ====指定目录名称  
           browseable = yes        ====可下载文件  
           writable = yes          ====可上传文件  
           public = yes            ====运行所有用户访问  
           write list =user1       ====仅允许user1可上传文件

#   
        
示例：

  
      
    环境描述：  
         Linux   192.168.196.131       Centos7            文件共享服务器  
           
windows/Linux客户端  
      
    需求：通过samba软件将本地的/caiwu 目录共享，客户端可以通过hei用户访问，仅允许下载文件      
           
前提：selinux和防火墙全部关闭  
（1）安装软件  
 

```
[root@wei ~]#  yum -y install samba samba-client
```

  
   
创建共享用户

```
[root@wei ~]# useradd hei
[root@wei ~]# smbpasswd -a hei
```

![](http://image.ownit.top/csdn/20190203194601751.png)  
      
       

查看共享用户

```
[root@wei ~]# pdbedit -L
```

![](http://image.ownit.top/csdn/20190203194857739.png)

配置文件/etc/smaba/smb.conf

```
[root@wei ~]# vim /etc/samba/smb.conf
```

```
[caiwu]
        comment = caiwu
        path = /caiwu
        browseable = yes
```

![](http://image.ownit.top/csdn/20190203195401688.png)

重启samba服务

\[root\@wei \~\]# systemctl start smb  
 

```
[root@wei ~]# systemctl start smb
```

 

# 测试访问：   
   
 windows访问：\\\\192.168.196.131

![](http://image.ownit.top/csdn/20190203195738821.png)

已经共享成功

![](http://image.ownit.top/csdn/20190203195820428.png)

 

 

##  Linux客户端：  
 

```
[root@wei ~]#  yum -y install samba-client
[root@zhang ~]# smbclient //192.168.196.131/caiwu-U hei
```

![](http://image.ownit.top/csdn/20190203200158864.png)

 

# 文件的上传

如果想要上传文件，这需要修改文件权限w为其他共享用户

如果不给权限会出现下面的情况

**windows客户端**

![](http://image.ownit.top/csdn/20190203200624830.png)

 

**Linux客户端**

![](http://image.ownit.top/csdn/20190203200719482.png)

重点修改文件权限w为其他共享用户

修改单个用户权限则可以使用下面这段命令

```
[root@wei ~]# setfacl -m u:hei:rwx /caiwu/
```

![](http://image.ownit.top/csdn/20190203201501406.png)

修改配置文件

![](http://image.ownit.top/csdn/20190203203249583.png)

## 重启就可以上传文件了

![](http://image.ownit.top/csdn/20190203203518173.png)

 

 

# 多用户示例：

 

  **        通过samba软件将本地的/shanghai目录共享，允许hei用户下载文件，允许admin用户上传文件**  
            
（1）创建目录，创建共享用户

```
[root@zhang ~]# mkdir /shichang
[root@zhang ~]# touch /shichang/{1..5}.jpg
[root@zhang ~]# useradd admin
[root@zhang ~]# useradd zhang
[root@zhang ~]# smbpasswd -a zhang
[root@zhang ~]# smbpasswd -a admin
```

配置文件修改下面这样

```
[shichang]
path = /shichang
browseable = yes
write list = admin
```

（2）重启服务访问

 

（3）测试访问：

    清除windows的共享缓存  
      net use \* /del

![](http://image.ownit.top/csdn/20190203203814524.png)