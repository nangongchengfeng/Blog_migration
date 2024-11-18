---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-02-01 21:34:06
description: 服务服务：管理服务器的方式：本地管理类安装系统，故障修复远程连接方式：命令提供服务客户端工具的软件：查看状态查看的端口：远程连接主机远程连接主机执行命令远程复制文件工具复制目录拷贝文件拷贝目录配置文件。。。。。。。
image: ../../title_pic/61.jpg
slug: '201902012134'
tags:
- linux
title: Linux服务管理之SSH
---

<!--more-->

**Linux服务SSH**

**ssh服务：  
管理服务器的方式：  
            
          本地管理类   （安装系统，故障修复）  
          SHH远程连接方式  
                 
               Linux：ssh命令  
               windows:Xshell , SecureCRT , Putty  
                 
提供ssh服务/ssh客户端工具的软件：  
openssh-clients-7.4p1-16.el7.x86\_64  
openssh-server-7.4p1-16.el7.x86\_64**

**查看ssh状态**

```
[hei@wei ~]$ systemctl status sshd
```

**![](../../image/20190201185013920.png)**

**查看ssh的端口：**

```
[root@wei ~]# ss -antp | grep sshd
```

**![](../../image/20190201185103754.png)  
                 
1.远程连接主机**

**\# shh \[user\@\]host**

**    # ssh 192.168.196.132  
      
    # ssh marin\@192.168.196.132  
      
2.远程连接主机执行命令**

**\# ssh 192.168.196.132 ‘hostname’       
               **

```
[root@wei ~]# ssh hei@192.168.196.132 'hostname'
hei@192.168.196.132's password: 
wei
```

**3.远程复制文件工具**

**     scp       rsync  
       
\# scp /etc/fstab 192.168.196.132:/tmp# scp 192.168.196.132:/etc/passwd /tmp  
   
     \-r: 复制目录  
     **

```
[root@wei ~]# scp /etc/fstab 192.168.196.132:/tmp
root@192.168.196.132's password: 
fstab                                                            100%  465    17.4KB/s   00:00    
[root@wei ~]# scp 192.168.196.132:/etc/passwd /tmp
root@192.168.196.132's password: 
passwd 

```

  
**rsync**

**\# rsync \-av /bj/ 192.168.196.132:/bj  #拷贝文件**

**\# rsync \-av /bj 192.168.196.132:/bj   #拷贝目录**

**配置文件：/etc/ssh/sshd\_config、**

**注意：下面几项操作在配置文件中进行**

**\(1\)关闭SSH的主机名解析  
         
         
       GSSAPIAuthentication no  
       ![](../../image/20190201211704865.png)  
       UseDNS no  
       ![](../../image/20190201211635121.png)**

```
    [root@zhang ~]# systemctl restart sshd
```

  
**（2）禁用root用户远程连接**

**      PermitRootLogin no**

**![](../../image/20190201211849837.png)**

**（3）修改默认端口  
      
    Port 1999**

**![](../../image/20190201211914429.png)**

**注意：此时连接需要加端口（-p） root用户已经登录不上**

```
[root@wei ~]# ssh hei@192.168.196.132 -p 1999
```

**（4）监听ip**

**          ListenAddress 192.168.196.131**

**![](../../image/20190201211914529.png)**

 

# **SSH认证方式：**

###   
**        
      基于用户名，密码：默认  
      基于密钥  
      **

**基于密钥的配置方法：  
           1.在客户端生成密钥对  
           2.把公钥传给服务器  
             
（1）在客户端生成密钥对**

**注意：默认生成的密钥会存储在/root/.ssh/目录下**

```
[root@wei ~]# ssh-keygen -t rsa

```

![](../../image/20190201213031258.png)

  
**（2）把公钥传送给服务器**

**注意：传递的公钥会存储在/root/.ssh/目录下**

```
[root@wei .ssh]# ssh-copy-id -i -p 1999 192.168.196.132
```

![](../../image/20190201213339720.png)

 

  
**注意：可以给普通用户复制公钥，但是要修改目录和公钥的权限为普通用户的**

![](../../image/20190201212614669.png)