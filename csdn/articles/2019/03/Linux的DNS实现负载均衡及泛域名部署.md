+++
author = "南宫乘风"
title = "Linux的DNS实现负载均衡及泛域名部署"
date = "2019-03-05 20:02:38"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/70.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88199567](https://blog.csdn.net/heian_99/article/details/88199567)

DNS负载均衡技术的实现原理是在DNS服务器中为同一个主机名配置多个IP地址，在应答DNS查询时，DNS服务器对每个查询将以DNS文件中主机记录的IP地址按顺序返回不同的解析结果，将客户端的访问引导到不同的机器上去，使得不同的客户端访问不同的服务器，从而达到负载均衡的目的

<img alt="" class="has" src="http://segmentfault.com/img/bVkYML"><img alt="" class="has" src="http://segmentfault.com/img/bVkYML">

<img alt="" class="has" src="%E2%80%8B%E2%80%8B%E2%80%8B%E2%80%8Bhttps%3A//image-static.segmentfault.com/365/448/3654482496-54f6c9fe72e0d_articlex"><img alt="" class="has" height="380" src="https://image-static.segmentfault.com/365/448/3654482496-54f6c9fe72e0d_articlex" width="497">

 

下面的部署是在[Linux的DNS正向解析部署](https://blog.csdn.net/heian_99/article/details/88196569)上进行修改的。

如果有什么问题或者错误，可以访问上篇帖子

下面开始有关DNS的服务部署。&lt;DNS实现负载均衡及泛域名&gt;

工具：虚拟机

          centos7 

配置：Linux   IP 192.168.196.132

                      DSN   192.168.196.132

## 负载平衡

利用DNS记录实现负载均衡效果

web     A       192.168.1.1<br> web     A       192.168.1.11

同一主机名解析到不同的ip上

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
dns01   A       192.168.196.132
web     A       192.168.1.1
web     A       192.168.1.11
ftp     A       192.168.1.2
        MX  10  mail.wei.com.
mail    A       192.168.1.3
```

## 重启服务

```
[root@wei named]# systemctl restart named-chroot

[root@wei named]# systemctl restart named
```

## 效果图

![20190305195654675.png](https://img-blog.csdnimg.cn/20190305195654675.png)

## 泛域名记录

wei.com.   A     192.168.1.1<br> *.wei.com  A     192.168.1.1

```
[root@wei named]# vim /var/named/chroot/var/named/wei.com.zone 
```

<br>  

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
web     A       192.168.1.1
web     A       192.168.1.11
wei.com.   A  192.168.1.1    # 使用wei.com就可以访问域名
*.wei.com.   A  192.168.1.1  # 无论前面加什么，都会解析到192.168.1.1上
ftp     A       192.168.1.2
        MX  10  mail.wei.com.
mail    A       192.168.1.3


```

## 重启服务

```
[root@wei named]# systemctl restart named-chroot

[root@wei named]# systemctl restart named
```

## 效果图

![20190305200202194.png](https://img-blog.csdnimg.cn/20190305200202194.png)

 
