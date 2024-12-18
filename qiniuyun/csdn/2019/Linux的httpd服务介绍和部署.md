---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-03-08 21:48:28
description: 软件介绍客户端代理软件，，，服务器端软件，，，，应用程序服务器，，，，，安装及配置：软件安装源码软件特性事先创建进程按需维持适当的进程模块化设计，核心较小，各种功能都能通过模块添加模块可以在运行时启用。。。。。。。
image: ../../title_pic/65.jpg
slug: '201903082148'
tags:
- llinux
title: Linux的httpd服务介绍和部署
---

<!--more-->

**软件介绍**

**客户端代理软件  
    IE，firefox，chroome，opera  
      
服务器端软件  
     httpd，Nginx，Tengine，ISS，Lighthttp  
       
应用程序服务器  
      ISS，Tomcat（JSP，open sourec），Websphere（IBM，JSP，commodity）Weblogic\(oracle,JSP,commodity\)  
      JBoss\(redhat,JSP\),Resin,php**

  
**httpd安装及配置**

**ASF：Apache Software Foundation   http://www.apache.org/  
     web:httpd  
         Tomcat  
         Hadoop  
           
httpd:           http://httpd.apache.org/  
      Web Server,Open Sourec  
      2.4,2.2,2.0  
        
httpd软件安装:  
     rpm  
     源码软件**

**httpd特性:  
    事先创建进程  
    按需维持适当的进程  
    模块化设计，核心较小，各种功能都能通过模块添加:模块可以在运行时启用  
          支持运行配置，支持单独编译模块  
    支持多种虚拟主机的配置  
          基于IP的虚拟主机  
          基于端口的虚拟主机  
          基于域名的虚拟主机  
    支持https协议\(mod\_ ss1\)  
    支持用户认证  
    支持基于IP或主机名的访问控制机制  
    支持每目录的访问控制  
    支持URL重写**

**安装httpd软件**

```
[root@wei ~]# yum install -y httpd
```

**开启服务**

```
[root@wei ~]# systemctl start httpd
```

**开机自启**

```
[root@wei ~]# systemctl enable httpd
```

**查看端口号**

```
[root@wei ~]# ss -antp |grep httpd
```

**![](../../image/20190308213345807.png)**

**查看它启动的进程**

```
[root@wei ~]# ps aux|grep httpd
```

**![](../../image/20190308213451440.png)**

**httpd目录:**

**      /etc/httpd/ conf                 主配置文件  httpd. conf  
      /etc/httpd/conf.d/\* . conf       子配置文件  
      /var/log/httpd  日志  
                access\_ .log  访问日志  
                error\_ log  错误日志**

**      /var/www/html  默认静态页面的目录  
      /var/www/cgi-bin  默认动态页面的目录**

**![](../../image/20190308213717876.png)CGI: Comnon Gateway Interface通用网关接口  
    让web服务器启动某应用程序解析动态页面的机制开发动态网页的语言:  
      perl, python, java \(Servlet JSP\), php**

**      PHP    LAMP , LNMP  
      JSP    Tomcat, Weblogical  
      Python  mod\_ wsgi模块**

##   
** httpd配置文件 ----  /etc/httpd/conf/httpd.conf ;**

**diretive value  
    指令不区分大小写  
    value区分大小写**

**1）设置httpd的主目录**

**ServerRoot "/etc/httpd"    **

**2）监听ip的地址和端口**

**    #Listen 12.34.56.78:80  
     Listen 80  
        
3）指定子配置文件的路径及名称**

** Include conf.modules.d/\*.conf**

**4\)设置运行httpd进程的用户及用户组名称**

**User apache  
Group apache**

**5\)长连接相关的配置**

**KeepAlive on  
MaxKeepAliveRequests 100  
KeepAliveTimeout 15**

**6\)设置管理员的邮箱**

**ServerAdmin root\@localhost**

**7\)设置网站的主机名**

**ServerName www.a. org**

**8\)设置网页目录**

**DocumentRoot "/var/www/html" **

**9\)设置网页的首页名称**

**DirectoryIndex index. html**

**10）针对目录权限**

**\<Directory "/var/www/html">  
  Options Indexes FollowSymLinks  
    AllowOverride None  
    Require all granted  
\</Directory>**

  
**A） Require all granted  
    允许所有的客户端访问该目录的页面文件  
      
B）Options Indexes FollowSymLinks  
   定义目录下的网页文件被访问时的访问属性  
       None：不支持任何选项  
       Indexes：无index.html 时，列出所有的文件，禁用  
       FollowSymLinks：存在软链接网页文件时，是否只可以访问对应原网页文件的内容，禁用  
       SymLinksifOwnerMatch:允许访问软链接，但所属必须和运行httpd进程的所属一致  
       Includes:允许执行服务器端包含\(SSI格式的网页文件\)，禁用  
       ExeCGI:允许运行CGI脚本  
       Multiviews:内容协商机制\(根据客户端的语言不同显示不同的网页\)，多视图:禁用  
       A11:启用所有选项**

**C）Allowoverride None**

**      是否允许建立.htaccess文件覆盖提权配置**

  
**查看帮助手册**

**\[root\@wei csdn\]# yum \-y install httpd-manual**

  
**http://192.168.196.131/manual/**

#   
**支持用户认证**

### **示例：客户端通过用户hei访问首页（/var/www/html）**

**\(1\)创建用户名称和密码**

```
[root@wei ~]# htpasswd -c /etc/httpd/.webuser hei
New password: 
Re-type new password: 
Adding password for user hei
```

**（2）编辑配置文件**

```
[root@wei ~]# vim /etc/httpd/conf/httpd.conf
```

 

```
<Directory "/var/www/html">
   
    Options Indexes FollowSymLinks
    AllowOverride AuthConfig
    AuthType Basic
    AuthName "Resttrict test"
    AuthUserFile /etc/httpd/.webuser
    Require valid-user
   #Require user 用户名称   只允许指定用户访问

</Directory>
```

**检测配置文件语法**

```

[root@wei ~]# httpd -t

Syntax OK
```

**\(3\)重启服务**

```
[root@wei ~]# systemctl restart httpd
```

![](../../image/20190308214756306.png)

 

**（4）再次创建一个用户wei  
创建用户名称和密码**

```
[root@wei ~]# htpasswd  /etc/httpd/.webuser wei

[root@wei ~]# cat /etc/httpd/.webuser 
hei:$apr1$nBaKumC0$lsSLO6LqDQ58CWLjXIfJT0
wei:$apr1$ovl.gsGg$SHvY5Aksj9MdZv9u8E5XF1
```

###   
**基于客户端ip地址的认证**

**1\) 允许所有喜户端访问**

**      Require all granted**

**2\)拒绝所有端访问**

**      Require al1 denied3\)仅允许某主机访问**

**      Require ip 192.168.1.14\) 明确拒绝某主机访问**

## ** \<RequireAll>  
       Require all granted  
       Require not ip 192.168.96.1  
     \</RequireAll>  
 windos访问效果图**

![](../../image/20190308214144293.png)  
**       
检测配置文件语法  
\[root\@wei \~\]# httpd \-t**

**Syntax OK**

**重启服务**

**\[root\@wei \~\]# systemctl restart httpd  
       
     **