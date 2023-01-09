+++
author = "南宫乘风"
title = "Linux文件服务管理之Samba"
date = "2019-02-03 20:38:40"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/71.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86760760](https://blog.csdn.net/heian_99/article/details/86760760)

 

Linux文件服务器的搭建<br>      <br>      Samba<br>      vsftpd<br>      nfs<br>      <br> Samba服务<br>       ![2019020319415694.png](https://img-blog.csdnimg.cn/2019020319415694.png)<br>       <br>       作用：共享目录<br>       软件：Samba 服务器 ，Samba-client 客户端<br>       配置文件：/etc/smaba/smb.conf<br>       服务：smb,nmb<br>       端口：smb ---&gt;139/tcp , 445/tcp  提供文件共享功能<br>             nmb ---&gt;137/udp , 138/udp  提供解析计算机名称<br>             <br> 配置文件：/etc/smaba/smb.conf

全局配置<br>      <br>      <br>       workgroup = SAMBA      ---设置工作组名称<br>       server string =Samba Server Version %v   ----显示samba软件版本信息<br>       <br>       interface = lo eth0 192.168.196.131？24   ---samba服务监听的ip地址<br>       <br>       hosts allow=127.192.168.12 192.168.196.0  -----设置仅允许那些主机访问<br>       hosts deny=192.168.12.  192.168.1.1/24     -----拒绝那些主机访问<br>       <br>       security =user     -------基于用户认证访问<br>                 share    -------匿名访问<br>                 <br>                 <br> 共享目录配置<br>        [共享名称]<br>        <br>            comment=                ====描述信息<br>            path = /bj              ====指定目录名称<br>            browseable = yes        ====可下载文件<br>            writable = yes          ====可上传文件<br>            public = yes            ====运行所有用户访问<br>            write list =user1       ====仅允许user1可上传文件

# <br>       <br>示例：

<br>     <br>     环境描述：<br>          Linux   192.168.196.131       Centos7            文件共享服务器<br>          <br> windows/Linux客户端<br>     <br>     需求：通过samba软件将本地的/caiwu 目录共享，客户端可以通过hei用户访问，仅允许下载文件    <br>          <br> 前提：selinux和防火墙全部关闭<br> （1）安装软件<br>  

```
[root@wei ~]#  yum -y install samba samba-client
```

<br>  <br> 创建共享用户

```
[root@wei ~]# useradd hei
[root@wei ~]# smbpasswd -a hei
```

![20190203194601751.png](https://img-blog.csdnimg.cn/20190203194601751.png)<br>     <br>        

查看共享用户

```
[root@wei ~]# pdbedit -L
```

![20190203194857739.png](https://img-blog.csdnimg.cn/20190203194857739.png)

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

![20190203195401688.png](https://img-blog.csdnimg.cn/20190203195401688.png)

重启samba服务

[root@wei ~]# systemctl start smb<br>  

```
[root@wei ~]# systemctl start smb

```

 

# 测试访问： <br>  <br>  windows访问：\\192.168.196.131

![20190203195738821.png](https://img-blog.csdnimg.cn/20190203195738821.png)

已经共享成功

![20190203195820428.png](https://img-blog.csdnimg.cn/20190203195820428.png)

 

 

##  Linux客户端：<br>  

```
[root@wei ~]#  yum -y install samba-client
[root@zhang ~]# smbclient //192.168.196.131/caiwu-U hei
```

![20190203200158864.png](https://img-blog.csdnimg.cn/20190203200158864.png)

 

# 文件的上传

如果想要上传文件，这需要修改文件权限w为其他共享用户

如果不给权限会出现下面的情况

**windows客户端**

![20190203200624830.png](https://img-blog.csdnimg.cn/20190203200624830.png)

 

**Linux客户端**

![20190203200719482.png](https://img-blog.csdnimg.cn/20190203200719482.png)

重点修改文件权限w为其他共享用户

修改单个用户权限则可以使用下面这段命令

```
[root@wei ~]# setfacl -m u:hei:rwx /caiwu/
```

![20190203201501406.png](https://img-blog.csdnimg.cn/20190203201501406.png)

修改配置文件

![20190203203249583.png](https://img-blog.csdnimg.cn/20190203203249583.png)

## 重启就可以上传文件了

![20190203203518173.png](https://img-blog.csdnimg.cn/20190203203518173.png)

 

 

# 多用户示例：

 

  **        通过samba软件将本地的/shanghai目录共享，允许hei用户下载文件，允许admin用户上传文件**<br>           <br> （1）创建目录，创建共享用户

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

    清除windows的共享缓存<br>       net use * /del

![20190203203814524.png](https://img-blog.csdnimg.cn/20190203203814524.png)

 

 
