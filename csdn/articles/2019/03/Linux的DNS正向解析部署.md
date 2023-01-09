+++
author = "南宫乘风"
title = "Linux的DNS正向解析部署"
date = "2019-03-05 19:20:34"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/72.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88196569](https://blog.csdn.net/heian_99/article/details/88196569)

前面介绍了DNS的作用及其相关的结果。[Linux服务之DNS介绍](https://blog.csdn.net/heian_99/article/details/88195866)

下面开始有关DNS的服务部署。&lt;DNS正向解析示例&gt;

工具：虚拟机

          centos7 

配置：Linux   IP 192.168.196.132

                      DSN   192.168.196.132

要求：

          web.wei.com      192.168.1.1<br>           ftp.wei.com      192.168.1.2    <br>           mail.wei.com     192.168.1.3<br>          

准备工作：（可以看前期教程）<br>      关闭SElinux，防火墙<br>      配置yum源

# 容易犯错的地方：查看/etc/resolv.conf 确保你的DNS是否正确

# ![20190305192006505.png](https://img-blog.csdnimg.cn/20190305192006505.png)

 

# DNS正向解析

（1）安装软件 bind  bind-chroot

```
[root@wei csdn]# yum install -y bind bind-chroot

```

2.编辑DNS的主配置文件，创建区域wei.com

新建named.conf

```
[root@wei named]# vim /var/named/chroot/etc/named.conf 
```

 填写内容

```
options{
   directory “/var/named";
};
zone "wei.com"{
  type master;
  file "wei.com.zone"
}:
```

 ![20190305190515255.png](https://img-blog.csdnimg.cn/20190305190515255.png)

 3.复制记录文件的模板，并编辑

模板：/usr/share/doc/bind-9.9.4/sample/var/named/named.localhost

```
[root@wei named]# cd /usr/share/doc/bind-9.9.4/sample/var/named/

[root@wei named]# cp named.localhost /var/named/chroot/var/named/wei.com.zone 	
```

 

```
$TTL 1D
@       IN SOA  wei.com. 123456.qq.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        NS      dns01.wei.com.
dns01   A       192.168.196.132
web     A       192.168.1.1
ftp     A       192.168.1.2
        MX  10  mail.wei.com.
mail    A       192.168.1.3

```

 

 

![20190305190809177.png](https://img-blog.csdnimg.cn/20190305190809177.png)

 

4.启动named服务

```
[root@wei named]# systemctl start named-chroot

[root@wei named]# systemctl start named
```

开机自启

```
[root@wei named]# systemctl enable named-chroot

[root@wei named]# systemctl enable named
```

查看端口53

![20190305191001671.png](https://img-blog.csdnimg.cn/20190305191001671.png)

 

5.测试

（1）nslookup

![20190305191444361.png](https://img-blog.csdnimg.cn/20190305191444361.png)

<br> （2）dig

[root@wei named]# dig -t A web.wei.com

![20190305191749596.png](https://img-blog.csdnimg.cn/20190305191749596.png)

 

 

 
