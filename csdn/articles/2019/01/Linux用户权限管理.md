+++
author = "南宫乘风"
title = "Linux用户权限管理"
date = "2019-01-24 22:28:18"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/52.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86634177](https://blog.csdn.net/heian_99/article/details/86634177)

#  

# Linux操作系统： 多用户多任务的操作系统

 

## 用户类型分为：<br>     管理员用户 ： root<br>     普通用户分为：系统用户/程序用户

**用户相关的文件：**

**    /etc/passwd      用户信息<br>          格式：x:UID:GID:说明信息:SHELL<br>          <br>          <br>          UID:<br>               1000----60000    创建用户<br>               0-----999        系统用户<br>          <br>          SHELL：<br>                /bin/bash        默认<br>                /sbin/nologin    系统用户<br>          <br>          <br>     /etc/shadow      用户密码信息**

 

### 用户：<br>      基本组<br>      附加组           userA----&gt; 用户组userA：

1.创建用户

# useradd [option] 用户名称

option选项：

<br> (1) -u  UID 指定用户的uid

```
[root@wei ~]# useradd -u 1200 wei2
[root@wei ~]# id wei2
uid=1200(wei2) gid=1200(wei2) 组=1200(wei2)
```

(2)指定用户的基本组,附加组<br>   <br>         -g gid/组名称<br>         -G gid/组名称,,,<br>         

```
[root@wei ~]# groupadd nan
[root@wei ~]# useradd -g wei2 -G nan wei3
[root@wei ~]# id wei3
uid=1201(wei3) gid=1200(wei2) 组=1200(wei2),1201(nan)
```

(3)指定用户shell名称<br>   <br>       -s shell名称<br>       -M  不创建宿主目录<br>       

```
[root@wei ~]# useradd -s /sbin/nologin -M zhangmiao
```

<br> (4)创建系统用户<br>       <br>        -r <br>        

```
[root@wei ~]# useradd -r nangong 
```

<br> (5)指定用户的宿主目录

       -d <br>        

```
[root@wei ~]# useradd -d /tmp/hei hei
[root@wei ~]# ls /tmp/
hei  vmware-root
[root@wei ~]# grep "hei" /etc/passwd
hei:x:1203:1203::/tmp/hei:/bin/bash
```

2，切换用户

# su - 用户名称

3，查看用户id

# id 用户名称

```
[root@wei ~]# id wei
uid=1000(wei) gid=1000(wei) 组=1000(wei)
```

id的选项：

```
[root@wei ~]# id wei3
uid=1201(wei3) gid=1200(wei2) 组=1200(wei2),1201(nan)
[root@wei ~]# id -u wei3
1201
[root@wei ~]# id -g wei3
1200
[root@wei ~]# id -G wei3
1200 1201
[root@wei ~]# id -u -n wei3
wei3
[root@wei ~]# id -g -n wei3
wei2
[root@wei ~]# id -G -n wei3
wei2 nan
```

3,设置用户密码

# passwd 用户名

```
[root@wei ~]# passwd wei
```

(1)查看用户密码状态

```
[root@wei ~]# passwd -S wei
wei PS 2019-01-24 0 99999 7 -1 (密码已设置，使用 SHA512 算法。)
```

(2)锁定用户密码

```
[root@wei ~]# passwd -l wei
锁定用户 wei 的密码 。
passwd: 操作成功


```

(3)解锁用户密码

```
[root@wei ~]# passwd -u wei
解锁用户 wei 的密码。
passwd: 操作成功


```

(4)强制用户密码过期

```
[root@wei ~]# passwd -e wei
正在终止用户 wei 的密码。
passwd: 操作成功

```

<br> 4,修改用户信息

# usermod  [option] 用户名称 <br>   <br>   <br>       -u UID<br>       -g 组名称<br>       -G 组名称<br>       -s shell名称<br> 替换原有附加组

```
[root@wei ~]# id wei3
uid=1201(wei3) gid=1200(wei2) 组=1200(wei2),1201(nan)
[root@wei ~]# groupadd shicahng
[root@wei ~]# usermod -G shicahng wei3
[root@wei ~]# id wei3
uid=1201(wei3) gid=1200(wei2) 组=1200(wei2),1204(shicahng)
```

添加多个附加组

```
[root@wei ~]# usermod -aG nan wei3
[root@wei ~]# id wei3
uid=1201(wei3) gid=1200(wei2) 组=1200(wei2),1201(nan),1204(shicahng)
```

<br> 6,删除用户

# userdel [option] 用户名称

```
[root@wei ~]# userdel wei

[root@wei ~]# userdel -r wei2  &gt;&gt;同时删除用户的宿主文件
```

<br> 用户组管理

1,创建用户组

# groupadd 用户组名称

2,删除用户组

# groupdel 用户组名称

```
[root@wei ~]# groupadd jishu
[root@wei ~]# useradd tom
[root@wei ~]# useradd tom1
[root@wei ~]# usermod -G jishu tom
[root@wei ~]# usermod -G jishu tom1
[root@wei ~]# grep "jishu" /etc/group
jishu:x:1205:tom,tom1
[root@wei ~]# gpasswd -d tom jishu
正在将用户“tom”从“jishu”组中删除
[root@wei ~]# grep "jishu" /etc/group
jishu:x:1205:tom1
```

 

 

 

 

 

 

 
