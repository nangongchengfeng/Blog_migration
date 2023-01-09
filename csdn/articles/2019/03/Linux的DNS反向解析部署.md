+++
author = "南宫乘风"
title = "Linux的DNS反向解析部署"
date = "2019-03-05 21:19:25"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/01.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88204612](https://blog.csdn.net/heian_99/article/details/88204612)

下面的部署是在[Linux的DNS正向解析示例](https://blog.csdn.net/heian_99/article/details/88196569)上进行修改的。

如果有什么问题或者错误，可以访问上篇帖子

下面开始有关DNS的服务部署。&lt;DNS反向解析&gt;

工具：虚拟机

          centos7 

配置：Linux   IP 192.168.196.132

                      DSN   192.168.196.132

 

建立DAS反向区域，实现反向解析

（1）编辑主配置文件named.conf

```
[root@wei named]# vim /var/named/chroot/etc/named.conf 
```

<br> 添加下面的代码

```
zone "1.168.192.in-addr.arpa" {
      type master;
      file "192.168.1.zone";  
};  
```

![20190305211607230.png](https://img-blog.csdnimg.cn/20190305211607230.png)

（2）建立反向区域

可以复制正向解析的文件作为模板

```
[root@wei named]# cp /var/named/chroot/var/named/wei.com.zone /var/named/chroot/var/named/192.168.1.zone
```

修改192.168.1.zone脚本

```
[root@wei named]# vim /var/named/chroot/var/named/192.168.1.zone
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
dns01   A       192.168.196.132
1       PTR     web.wei.com.
11      PTR     web.wei.com.
2       PTR     ftp.wei.com.
3       PTR     mail.wei.com.
```

（3）重启服务<br>  

```
[root@wei named]# systemctl restart named-chroot

[root@wei named]# systemctl restart named
```

（4）使用nslookup测试查看

![20190305211902801.png](https://img-blog.csdnimg.cn/20190305211902801.png)

 

 
