---
author: 南宫乘风
categories:
- Linux服务应用
date: 2019-03-05 18:46:29
description: 域名系统介绍：就是把域名和地址联系在一起的服务，有了服务器，你就不用输入地址来访问一个网站，可以通过输入网址访问。作用：将域名，主机名解析对应的地址正向解析将地址解析成对应的主机名，域名反向解析区域：。。。。。。。
image: http://image.ownit.top/4kdongman/13.jpg
tags:
- linux
title: Linux服务之DNS介绍
---

<!--more-->

**DNS-------Domain Name System域名系统**

**介绍：DNS就是把域名和IP地址联系在一起的服务，有了DNS服务器，你就不用输入IP地址来访问一个网站，可以通过输入网址访问。**

 

**         ![](http://image.ownit.top/csdn/d043ad4bd11373f0eea42c62a80f4bfbfaed04b7.jpg)**

 

**作用：（1）将域名，主机名解析对应的ip地址       正向解析  
           （2）将IP地址解析成对应的主机名，域名     反向解析    **

  
**区域zone：  
    正向区域              nangong.com  
    反向区域              X.X.X.in-addr.arpa   192.168.196.0/24    196.168.1962.in-addr.arpa**

 

**记录Record  
      
    A记录      主机记录        www.nangong.com   A   192.168.1.1  
      
    NS记录     标识DNS服务器自身的名称  
          
        NS     dns1.nangong.com.  
        dns1.nangong.com         A    192.168.1.2  
          
    MX记录     标识邮件服务器的名称  
         
       MX      10    mail.nangong.com.  
       mail.nangong.com          A    192.168.196.3  
         
         
    CNAME记录  别名记录      
          
       m.mail.com   CNAME   mail.nangong.com.  
                
      
    PTR记录     反向指针记录  
          
        192.168.1.1    PTR     www.nangong.com.  
        **

**DNS域名结构：**

**    .  根域  
       com  
           jd      www.jd.com---------->www.jd.com.  
           baidu  
           taobao  
        cn   
        edu  
        org  
          
DNS解析方式：  
       
     递归  
         客户端只需要向DNS服务器发送一次请求  
           
    迭代  
         客户端需要发送多次DNS请求**