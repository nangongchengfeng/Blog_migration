---
author: 南宫乘风
categories:
- Java
date: 2019-09-26 17:52:53
description: 随着技术的更新对于开发速度的追求，我们越来越不能忍受的是框架对于集成开发以后大量的配置问题。所以应运而生，框架其实就是在框架的外边包裹上了一层纸，包括减少配置文件，内置服务器等等。在这里我们就使用工具。。。。。。。
image: http://image.ownit.top/4kdongman/33.jpg
tags:
- 技术记录
title: IEDA创建Springboot项目
---

<!--more-->

 

     随着技术的更新对于开发速度的追求，我们越来越不能忍受的是Spring框架对于集成开发以后大量的配置问题。所以SprigBoot应运而生，SpringBoot框架其实就是在Spring框架的外边包裹上了一层纸，包括减少配置文件，内置Tomcat服务器等等。在这里我们就使用IDEA工具为代表讲解一下SpringBoot在开发过程中会使用到的开发技术。官方推荐的编辑器是STS，STS就是对Eclipes做了封装，其实没有什么具体的改变，所以这里就是用更加快捷方便的开发工具IDEA，没有多大的影响。

　　创建项目：

![](http://image.ownit.top/csdn/20190926172148611.png)

 

![](http://image.ownit.top/csdn/20190926172321309.png)

接下来就是给项目命名了，我偷懒了选择默认吧 \(=v=\)

web项目开发就少不了它啦

项目名称、项目位置

![](http://image.ownit.top/csdn/20190926172658850.png)

 

![](http://image.ownit.top/csdn/20190926172717916.png)

![](http://image.ownit.top/csdn/20190926172807660.png)

![](http://image.ownit.top/csdn/20190926172824831.png)

点击Finish后，idea就帮我们创建项目

目录结构

![](http://image.ownit.top/csdn/20190926172915881.png)

java \----源码，要注意的是Application要放在当前工程groupId下，举个栗子（=.=）

                       \<groupId>com.example\</groupId>

                       所以上面的 DemoApplication 位置是要放在 com.example 目录下

resource

        \-----static ：web的静态资源

        \-----templates ：页面模板（.html / .ftl）

        \-----application.properties ：配置文件 ，不过常用的是以 .yml 为后缀，application.yml

接下来写一个简单的测试代码

UserController.java

```java
package com.demo.ssm.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Controller
@RequestMapping("")
public class UserController {

    @RestController

    public class TestController {

        @RequestMapping("/test")

        public String hello() {
            System.out.println("TestController的方法被调用了");
            return "welcome to the new age !";
        }
    }
}
```

  
因为Springboot 内嵌 web 服务器（有很多，可根据情况所需配置），默认是 Tomcat，因此直接运行 Application类

application.properties  
   
 

```
# 服务端口
server.port=8080



# 日志级别
logging.level.root=error
```

 

![](http://image.ownit.top/csdn/20190926175206200.png)

打开浏览器，在地址栏输入请求URL

![](http://image.ownit.top/csdn/20190926173926857.png)

控制台输出

![](http://image.ownit.top/csdn/20190926174413567.png)

  
打开浏览器，在地址栏输入请求URL

控制台输出

没有spring繁琐的配置，也不用部署到Tomcat，开发也可以如此快捷方便。