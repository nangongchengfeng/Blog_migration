+++
author = "南宫乘风"
title = "Linux的web服务的介绍"
date = "2019-03-06 20:26:44"
tags=['Linux']
categories=[' Linux服务应用']
image = "post/4kdongman/81.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88254043](https://blog.csdn.net/heian_99/article/details/88254043)

**web（World Wide Web）即全球广域网，也称为万维网，它是一种基于超文本和HTTP的、全球性的、动态交互的、跨平台的分布式图形信息系统。是建立在Internet上的一种网络服务，为浏览者在Internet上查找和浏览信息提供了图形化的、易于访问的直观界面，其中的文档及超级链接将Internet上的信息节点组织成一个互为关联的网状结构<br>      <br>     网页类型：<br>           静态网页   HTML超文本标记语言   *.html<br>           动态网站<br>                类似于脚本文件，根据传递的参数不同，返回的页面结果不同的<br>                <br>                PHP               *.php<br>                Java(JSP)         *.jsp<br>                Python(Django模块)*.wsgi<br>                <br>                <br> HTTP-------------HyperText Transfer Protocol   超文本传输协议**

**HTTP/0.9：仅纯文本（超链接），ASCLL<br>     HTTP ：HyperText Mark Language 超文本标记语言<br>     &lt;h1&gt;I am cehngfneg.&lt;/h1&gt;<br>     <br>     <br>HTTP/1.0<br>                MIME机制：Multipurpose Internet Mail Extensions，多用途互联网邮件扩展<br>                将非文本数据在传输前重新编码为文本格式再传输，接收方能够用相反的方式将其还原成以前的格式，还能够调用相应的程序打开此文件<br>           <br>         缓存机制<br>         <br>HTTP/1.1（无状态连接）<br>       增强了缓存机制的管理<br>       长连接keepalive机制<br>            超时时间<br>            每个长连接请求文件个数的限制<br>            <br>HTTP报文：请求报文，响应报文<br>            <br>HTTP请求报文语法：**

**&lt;method&gt;&lt;request-URL&gt;&lt;version&gt;<br> &lt;headers&gt;**

**&lt;entity-body&gt;**

**请求报文：**

**GET /1.gif HTTP/1.1<br> Host:www.bj.com<br> Connection:keep-alive**

**HTTP方法：<br>       GET，PUT，POST，DELETE，HEAD<br>       <br> URI：Uniform Resource Identifier，统一资源标识符        /.jpg<br>      全局范围内，唯一标识某个资源的名称<br>      统一：路径格式上的统一<br>      <br> URL：Uniform Resource Locator  统一资源定位符<br>      protocal://Host:Port/path/to/file<br>      <br>      http://192.168.1.1/1.jpg<br>      <br>      http://192.168.1.1:8000/1.jpg**

**HTTP响应报文语法：**

**&lt;version&gt;&lt;status&gt;&lt;reason-phrase&gt;<br> &lt;headers&gt;**

**&lt;entity-body&gt;**

<br>** 状态代码:<br>  <br> 1xx:纯信息<br> 2xx:成功类信息<br> 3xX:重定向类信息I<br>      301:永久重定向<br>      302:临时重定向<br>      304: not-modified, 使用缓存的内容响应客户端<br> 4xx:客户端错误类信息<br> 5xx:服务器端错误类信息**

<br>**响应报文:<br> HTTP/1.1 200 OK<br> X-Powerd=By: PHP/5.2.17<br> vary: Accept-Encoding, Cookie, User-Agent<br> Cache-Control: max-age=3, must-revalidate<br> Content-Encoding: gzip<br> Content -Length: 6931**

**上面两个报文的第一 行通常称为报文的“起始行(start line)"; 后面的标签格式称为报文首部域(Header<br> field)，每个首部域都由名称(name)和值(value)组成，中间用逗号分隔。另外，响应报文通常还有- - 个称作Body的信息主体，即响应给客户端的内容**

<br>**web服务器的主要操作:**

**1、建立连接----接受或拒绝客户端连接请求<br> 2、接收请求----通过网络读取HTTP请求报文<br> 3、处理请求----解析请求报文并做出相应的动作<br> 4、访问资源----访问请求报文中所请求的资源<br> 5、构建响应----使用正确的首部生成HTTP响应报文<br> 6、发送响应----向客户端发送生成的响应报文<br> 7、记录日志----当已经完成的HTTP事务记录进日志文件**

<br>**web服务器响应并发连接(qps--&gt; query per second) 的方式:**

**1、单进程/单线程机制<br>     依次处理每个请求<br> 2、多进程/多线程机制(稳定)<br>     每个请求生成子进程响应<br> 3、一一个进程响应多个请求(单进程多线程)<br>       事件驱动机制<br>       通知机制<br> 4、多进程响应多个请求**
