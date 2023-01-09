+++
author = "南宫乘风"
title = "Linux服务管理之SSH"
date = "2019-02-01 21:34:06"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/48.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86743862](https://blog.csdn.net/heian_99/article/details/86743862)

**Linux服务SSH**

**ssh服务：<br> 管理服务器的方式：<br>           <br>           本地管理类   （安装系统，故障修复）<br>           SHH远程连接方式<br>                <br>                Linux：ssh命令<br>                windows:Xshell , SecureCRT , Putty<br>                <br> 提供ssh服务/ssh客户端工具的软件：<br> openssh-clients-7.4p1-16.el7.x86_64<br> openssh-server-7.4p1-16.el7.x86_64**

**查看ssh状态**

```
[hei@wei ~]$ systemctl status sshd
```

**![20190201185013920.png](https://img-blog.csdnimg.cn/20190201185013920.png)**

**查看ssh的端口：**

```
[root@wei ~]# ss -antp | grep sshd
```

**![20190201185103754.png](https://img-blog.csdnimg.cn/20190201185103754.png)<br>                <br> 1.远程连接主机**

**# shh [user@]host**

**    # ssh 192.168.196.132<br>     <br>     # ssh marin@192.168.196.132<br>     <br> 2.远程连接主机执行命令**

**# ssh 192.168.196.132 ‘hostname’     <br>                **

```
[root@wei ~]# ssh hei@192.168.196.132 'hostname'
hei@192.168.196.132's password: 
wei
```

**3.远程复制文件工具**

**     scp       rsync<br>      <br> # scp /etc/fstab 192.168.196.132:/tmp# scp 192.168.196.132:/etc/passwd /tmp<br>  <br>      -r: 复制目录<br>      **

```
[root@wei ~]# scp /etc/fstab 192.168.196.132:/tmp
root@192.168.196.132's password: 
fstab                                                            100%  465    17.4KB/s   00:00    
[root@wei ~]# scp 192.168.196.132:/etc/passwd /tmp
root@192.168.196.132's password: 
passwd 


```

<br>**rsync**

**# rsync -av /bj/ 192.168.196.132:/bj  #拷贝文件**

**# rsync -av /bj 192.168.196.132:/bj   #拷贝目录**

**配置文件：/etc/ssh/sshd_config、**

**注意：下面几项操作在配置文件中进行**

**(1)关闭SSH的主机名解析<br>        <br>        <br>        GSSAPIAuthentication no<br>        ![20190201211704865.png](https://img-blog.csdnimg.cn/20190201211704865.png)<br>        UseDNS no<br>        ![20190201211635121.png](https://img-blog.csdnimg.cn/20190201211635121.png)**

```
    [root@zhang ~]# systemctl restart sshd
```

<br>**（2）禁用root用户远程连接**

**      PermitRootLogin no**

**![20190201211849837.png](https://img-blog.csdnimg.cn/20190201211849837.png)**

**（3）修改默认端口<br>     <br>     Port 1999**

**![20190201211914429.png](https://img-blog.csdnimg.cn/20190201211914429.png)**

**注意：此时连接需要加端口（-p） root用户已经登录不上**

```
[root@wei ~]# ssh hei@192.168.196.132 -p 1999
```

**（4）监听ip**

**          ListenAddress 192.168.196.131**

**![20190201211914529.png](https://img-blog.csdnimg.cn/20190201211914529.png)**

#  

# **SSH认证方式：**

### <br>**      <br>       基于用户名，密码：默认<br>       基于密钥<br>       **

**基于密钥的配置方法：<br>            1.在客户端生成密钥对<br>            2.把公钥传给服务器<br>            <br> （1）在客户端生成密钥对**

**注意：默认生成的密钥会存储在/root/.ssh/目录下**

```
[root@wei ~]# ssh-keygen -t rsa


```

**          **![20190201213031258.png](https://img-blog.csdnimg.cn/20190201213031258.png)** **

<br>**（2）把公钥传送给服务器**

**注意：传递的公钥会存储在/root/.ssh/目录下**

```
[root@wei .ssh]# ssh-copy-id -i -p 1999 192.168.196.132
```

![20190201213339720.png](https://img-blog.csdnimg.cn/20190201213339720.png)

 

<br>**注意：可以给普通用户复制公钥，但是要修改目录和公钥的权限为普通用户的**

![20190201212614669.png](https://img-blog.csdnimg.cn/20190201212614669.png)
