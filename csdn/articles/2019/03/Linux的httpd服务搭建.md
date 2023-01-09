+++
author = "南宫乘风"
title = "Linux的httpd服务搭建"
date = "2019-03-12 19:30:27"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/89.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88427082](https://blog.csdn.net/heian_99/article/details/88427082)

在服务搭建前，还要了解一下httpd的日志。

日志有助有工作人员，查看服务器出错状况，更能统计数据分析网页运行情况。

# **PV和UV两大分析**

### PV  Page View 页面访问量<br> UV  User View 用户访问量

1)指定错误日志的名称及级别

**错误日志的路径：**/var/log/httpd/error_log

**错误级别：** debug, info, notice, warn, error, crit

**访问日志：** /var/log/httpd/access_log

```
[root@wei httpd]# head -n 1 /var/log/httpd/access_log
```

![2019031219235115.png](https://img-blog.csdnimg.cn/2019031219235115.png)<br>（2）定义访问日志的格式

LogFormat "%h %l %u %t \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

```
192.168.196.1 - - [07/Mar/2019:05:33:39 +0800] "GET / HTTP/1.1" 200 1766 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
```

       <br>       ** %h 远端主机<br>        %l 远端登录名(由identd而来，如果支持的话)，除非IdentityCheck设为"On"，否则将得到一个"-"。<br>        %u 远程用户名(根据验证信息而来；如果返回status(%s)为401，可能是假的)<br>        %t 时间，用普通日志时间格式(标准英语格式)<br>        %r 请求的第一行<br>        %&gt;s:HTTP状态码<br>        %b 以CLF格式显示的除HTTP头以外传送的字节数，也就是当没有字节传送时显示’-'而不是0。<br>        %{Referer}i：记录超链接地址<br>        %{User-Agent}i：记录客户端的浏览器类型**

<br>（3）指定访问日志的名称及格式

 CustomLog "logs/access_log" combined

 

# **虚拟主机 VirtualHost**

    作用：在一台物理服务器上运行多个网站<br>     <br>     类型：<br>          基于域名的虚拟主机（常用）<br>          基于IP地址的虚拟主机<br>          基于端口的虚拟主机<br>          <br> 配置虚拟主机

```
&lt;VirtualHost 10.1.2.3:80&gt;
  ServerAdmin webmaster@host.example.com
  DocumentRoot /www/docs/host.example.com
  ServerName host.example.com
  ErrorLog logs/host.example.com-error_log
  TransferLog logs/host.example.com-access_log
&lt;/VirtualHost&gt;
```

### <br>示例：基于主机名的虚拟主机

  www.a.org    网页目录：/var/www/html/a.org   日志：/var/log/httpd/a.org<br>  

 www.a.org  

(1)准备目录

```
[root@wei ~]# mkdir /var/www/html/a.org
[root@wei ~]# vim /var/www/html/a.org/index.html
[root@wei ~]# mkdir /var/log/httpd/a.org
```

（2）编写配置文件

```
[root@wei ~]# vim /etc/httpd/conf.d/a.org.conf
```

```
&lt;VirtualHost 192.168.196.132:80&gt;
  DocumentRoot /var/www/html/a.org
  ServerName www.a.org
  ErrorLog /var/log/httpd/a.org/error_log
  CustomLog /var/log/httpd/a.org/access_log combined

&lt;/VirtualHost&gt;
```

<br> （3）检测配置文件语法

```
[root@wei ~]# httpd -t
```

（4）重启服务

```
[root@wei ~]# systemctl restart httpd
```

<br>  

<br>  
