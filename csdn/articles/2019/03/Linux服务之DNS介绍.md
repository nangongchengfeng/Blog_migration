+++
author = "南宫乘风"
title = "Linux服务之DNS介绍"
date = "2019-03-05 18:46:29"
tags=['linux']
categories=[' Linux服务应用']
image = "post/4kdongman/62.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88195866](https://blog.csdn.net/heian_99/article/details/88195866)

**DNS-------Domain Name System域名系统**

**介绍：DNS就是把域名和IP地址联系在一起的服务，有了DNS服务器，你就不用输入IP地址来访问一个网站，可以通过输入网址访问。**

 

**         <img alt="" class="has" src="https://gss0.baidu.com/-4o3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D600%2C800/sign=0e7681ce9d8fa0ec7f926c0b16a775d6/d043ad4bd11373f0eea42c62a80f4bfbfaed04b7.jpg">**

 

**作用：（1）将域名，主机名解析对应的ip地址       正向解析<br>            （2）将IP地址解析成对应的主机名，域名     反向解析    **

<br>**区域zone：<br>     正向区域              nangong.com<br>     反向区域              X.X.X.in-addr.arpa   192.168.196.0/24    196.168.1962.in-addr.arpa**

 

**记录Record<br>     <br>     A记录      主机记录        www.nangong.com   A   192.168.1.1<br>     <br>     NS记录     标识DNS服务器自身的名称<br>         <br>         NS     dns1.nangong.com.<br>         dns1.nangong.com         A    192.168.1.2<br>         <br>     MX记录     标识邮件服务器的名称<br>        <br>        MX      10    mail.nangong.com.<br>        mail.nangong.com          A    192.168.196.3<br>        <br>        <br>     CNAME记录  别名记录    <br>         <br>        m.mail.com   CNAME   mail.nangong.com.<br>               <br>     <br>     PTR记录     反向指针记录<br>         <br>         192.168.1.1    PTR     www.nangong.com.<br>         **

**DNS域名结构：**

**    .  根域<br>        com<br>            jd      www.jd.com----------&gt;www.jd.com.<br>            baidu<br>            taobao<br>         cn <br>         edu<br>         org<br>         <br> DNS解析方式：<br>      <br>      递归<br>          客户端只需要向DNS服务器发送一次请求<br>          <br>     迭代<br>          客户端需要发送多次DNS请求**
