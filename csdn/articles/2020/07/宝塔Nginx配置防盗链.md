+++
author = "南宫乘风"
title = "宝塔Nginx配置防盗链"
date = "2020-07-13 10:34:13"
tags=['宝塔', 'nginx', '防盗链', '图片', '流量']
categories=[' Linux实战操作']
image = "post/4kdongman/23.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/107293684](https://blog.csdn.net/heian_99/article/details/107293684)

# Nginx配置防盗链

## **1.什么是资源盗链**

简单地说，就是某些不法网站未经许可，通过在其自身网站程序里非法调用其他网站的资源，然后在自己的网站上显示这些调用的资源，达到填充自身网站的效果。这一举动不仅浪费了调用资源网站的网络流量，还造成其他网站的带宽及服务压力吃紧，甚至宕机。

![20200712001931869.png](https://img-blog.csdnimg.cn/20200712001931869.png)

## ** 2.网站资源被盗链带来的问题**

若网站图片及相关资源被盗链，最直接的影响就是网络带宽占用加大了，带宽费用多了，网络流量也可能忽高忽低，Nagios/Zabbix等报警服务频繁报警

![20200712002043920.png](https://img-blog.csdnimg.cn/20200712002043920.png)

最严重的情况就是网站的资源被非法使用，使网站带宽成本加大和服务器压力加大，这有可能导致数万元的损失，且网站的正常用户访问也会受到影响

## 3.企业真实案例：网站资源被盗链，出现严重问题

某日，接到从事运维工作的朋友的紧急求助，其公司的CDN源站，源站的流量没有变动，但CDN加速那边的流量无故超了好几个GB，不知道怎么处理。

该故障的影响：由于是购买的CDN网站加速服务，因此虽然流量多了几个GB，但是业务未受影响。只是，这么大的异常流量，持续下去可直接导致公司无故损失数万元。解决这个问题可体现运维的价值。

## 4.常见防盗链解决方案的基本原理

### （1）根据HTTP referer实现防盗链

在HTTP协议中，有一个表头字段叫referer，使用URL格式来表示是哪里的链接用了当前网页的资源。通过referer可以检测访问的来源网页，如果是资源文件，可以跟踪到显示它的网页地址，一旦检测出来源不是本站，马上进行阻止或返回指定的页面。

HTTP referer是header的一部分，当浏览器向Web服务器发送请求时，一般会带上referer，告诉服务器我是从哪个页面链接过来的，服务器借此获得一些信息用于处理。Apache、Nginx、Lighttpd三者都支持根据HTTP referer实现防盗链，referer是目前网站图片、附件、html等最常用的防盗链手段

![20200712002247128.png](https://img-blog.csdnimg.cn/20200712002247128.png)

### （2）根据cookie防盗链

对于一些特殊的业务数据，例如流媒体应用通过ActiveX显示的内容（例如，Flash、Windows Media视频、流媒体的RTSP协议等），因为它们不向服务器提供referer header，所以若采用上述的referer的防盗链手段，就达不到想要的效果。

对于Flash、Windows Media视频这种占用流量较大的业务数据，防盗链是比较困难的，此时可以采用Cookie技术，解决Flash、Windows Media视频等的防盗链问题。

例如：ActiveX插件不传递referer，但会传递Cookie，可以在显示ActiveX的页面的&lt;head&gt;&lt;/head&gt;标签内嵌入一段JavaScript代码，设置“Cookie：Cache=av”如下：

```
&lt;script&gt; document.cookie="Cache=av；

domain=domain.com；

path=/"；

 &lt;/script&gt;
```

然后就可以通过各种手段来判断这个Cookie的存在，以及验证其值的操作了。

根据Cookie来防盗链的技术非本书的内容，读者了解即可，如果企业确实有需要，可以阅读其他书籍或进入交流群获取这部分的知识。

## （3）通过加密变换访问路径实现防盗链

此种方法比较适合视频及下载类业务数据的网站。例如：Lighttpd有类似的插件mod_secdownload来实现此功能。先在服务器端配置此模块，设置一个固定用于加密的字符串，比如oldboy，然后设置一个url前缀，比如/mp4/，再设置一个过期时间，比如1小时，然后写一段PHP代码，利用加密字符串和系统时间等通过md5算法生成一个加密字符串。最终获取到的文件的URL链接中会带有一个时间戳和一个加密字符的md5数值，在访问时系统会对这两个数据进行验证。如果时间不在预期的时间段内（如1小时内）则失效；如果时间戳符合条件，但是加密的字符串不符合条件也会失效，从而达到防盗链的效果。

```
&lt;php
$secret = "oldboy"；
     // 加密字符串，必须和
lighttpd.conf里的保持一致
$uri_prefix = "/mp4/"；
     // 虚拟的路径、前缀，必须和
lighttpd.conf里的保持一致
$file = "/test.mp4"；
     // 实际文件名，必须加
"/"斜杠
$timestamp = time（）；
     // current timestamp
$t_hex = sprintf（
"%08x"，
 $timestamp）；
$m = md5（
$secret.$file.$t_hex）；
printf（
'%s'，
 $uri_prefix，
 $m，
 $t_hex，
 $file，
 $file）；
     //生成
url地址串
&gt;
```

## Nginx Web服务实现防盗链实战

在默认情况下，只需要进行简单的配置，即可实现防盗链处理

利用referer，并且针对扩展名rewrite重定向

第一步

![20200713102729988.png](https://img-blog.csdnimg.cn/20200713102729988.png)

第二步

![20200713102916129.png](https://img-blog.csdnimg.cn/20200713102916129.png)

第三步

![20200713103058257.png](https://img-blog.csdnimg.cn/20200713103058257.png)

相关配置

```
配置前


    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
        error_log off;
        access_log /dev/null;
    }



配置后


	location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
{
 valid_referers *.heian99.top heian99.top;
 if ($invalid_referer) {
  rewrite ^/ https://ftp.bmp.ovh/imgs/2020/06/75d45131a596abbd.jpg;
  #return 404;
 }
 expires  30d;
}



```

效果图

打开这个图片，放到别的浏览器查看

![20200713103143191.png](https://img-blog.csdnimg.cn/20200713103143191.png)

就会变成下面这个图片了

![20200713103259330.png](https://img-blog.csdnimg.cn/20200713103259330.png)
