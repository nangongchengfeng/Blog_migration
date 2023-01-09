+++
author = "南宫乘风"
title = "三层架构介绍和MVC设计模型介绍"
date = "2019-08-30 15:03:46"
tags=['springmvc']
categories=[]
image = "post/4kdongman/62.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100158832](https://blog.csdn.net/heian_99/article/details/100158832)



# springmvc是什么?

Spring Web MVC是一种基于Java的实现了Web MVC设计模式的请求驱动类型的轻量级Web框架，即使用了MVC架构模式的思想，将web层

进行职责解耦，基于请求驱动指的就是使用请求-响应模型，框架的目的就是帮助我们简化开发，Spring Web MVC也是要简化我们日常Web开发的。

# 服务器端分成三层框架

 

表现层：SpringMVC           包含JSP和Servlet等与WEB相关的内容

 

业务层：Spring框架            业务层中不包含JavaWeb API，它只关心业务逻辑

 

持久层：MyBatis                封装了对数据库的访问细节

![20190830145419312.png](https://img-blog.csdnimg.cn/20190830145419312.png)

# MVC设计模型

<img alt="" class="has" height="347" src="https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWFnZXMyMDE1LmNuYmxvZ3MuY29tL2Jsb2cvNzc0MzI1LzIwMTYwMy83NzQzMjUtMjAxNjAzMjkxNDUyMjMzOTQtMjQ4MDMyODIuZ2lm" width="440">

MVC 是一种使用 MVC（Model View Controller 模型-视图-控制器）设计创建 Web 应用程序的模式：
-  Model（模型）表示应用程序核心（比如数据库记录列表）。 -  View（视图）显示数据（数据库记录）。 -  Controller（控制器）处理输入（写入数据库记录）。 
MVC 模式同时提供了对 HTML、CSS 和 JavaScript 的完全控制。

**Model（模型）**是应用程序中用于处理应用程序数据逻辑的部分。<br> 　　通常模型对象负责在数据库中存取数据。

**View（视图）**是应用程序中处理数据显示的部分。<br> 　　通常视图是依据模型数据创建的。

**Controller（控制器）**是应用程序中处理用户交互的部分。<br> 　　通常控制器负责从视图读取数据，控制用户输入，并向模型发送数据。

 

 
