---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-03-05 21:35:15
description: 下面的部署是在的正向解析部署上进行修改的。如果有什么问题或者错误，可以访问上篇帖子下面开始有关的服务部署。主从服务器环境描述：主服务器从服务器将主服务器的上的区域的记录与从服务器同步主服务器：编辑主配。。。。。。。
image: ../../title_pic/44.jpg
slug: '201903052135'
tags:
- linux
title: Linux的DNS主从服务器部署
---

<!--more-->

下面的部署是在[Linux的DNS正向解析部署](https://blog.csdn.net/heian_99/article/details/88196569)上进行修改的。

如果有什么问题或者错误，可以访问上篇帖子

下面开始有关DNS的服务部署。\<DNS主从服务器>

环境描述：  
          

          192.168.196.132     DNS主服务器  
          192.168.196.131     DNS从服务器  
            
      
将主服务器的上的wei.com区域的记录与从服务器同步

# **主服务器：**

（1）编辑主配置文件named.conf

```
[root@wei named]# vim /var/named/chroot/etc/named.conf 
```

```
options {
      directory "/var/named";
};


zone "wei.com" {
     type master;
     allow-transfer { 192.168.196.131;};  >>>指定从服务器的IP
     file "wei.com.zone";
};
            
zone "1.168.192.in-addr.arpa" {
      type master;
      file "192.168.1.zone";  
};       
```

  

（2）编辑wei.com的区域的记录文件，添加从服务器的NS记录

```
[root@wei named]# vim /var/named/chroot/var/named/wei.com.zone 
```

```
$TTL 1D
@       IN SOA  wei.com. 123456.qq.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      dns01.wei.com.
        NS      dns02.wei.com.
dns01   A       192.168.196.132
dns02   A       192.168.196.131
web     A       192.168.1.1
web     A       192.168.1.11
wei.com.   A  192.168.1.1
*.wei.com.   A  192.168.1.1
ftp     A       192.168.1.2
        MX  10  mail.wei.com.
mail    A       192.168.1.3
```

  
      
（3）重启服务

```
[root@wei named]# systemctl restart named-chroot

[root@wei named]# systemctl restart named
```

#   
从服务器：

（1）安装软件

```
[root@wei named]# yum install -y bind bind-chroot
```

（2）编辑主配置文件

```
[root@wei csdn]# vim /var/named/chroot/etc/named.conf
```

```
options {
      directory "/var/named";
};


zone "wei.com" {
     type slave;
     masters { 192.168.196.132;}; >>>>指向主服务器
     file "slaves/wei.com.zone";
};
```

（3）重启服务

```
[root@wei named]# systemctl restart named-chroot

[root@wei named]# systemctl restart named
```

（4）测试

```
[root@wei slaves]# cd /var/named/chroot/var/named/slaves

[root@wei slaves]# ls
wei.com.zone
```

已经成功加载

![](../../image/20190305212740195.png)  
（5）nslookup检查

![](../../image/20190305213010130.png)

 

好的，这就已经完成主从服务器的搭建了。

我们去主服务器新加区域，看能否同步解析

![](../../image/2019030521333539.png)

重启主服务器。

现在去测试从服务器的同步情况，已经成功了，ok。

![](../../image/20190305213438942.png)