---
author: 南宫乘风
categories:
- 项目实战
date: 2023-03-27 10:18:30
description: 本文将介绍如何在中集成阿波罗和，并使用和实现配置管理和服务注册与发现的功能。什么是阿波罗阿波罗是携程开源的分布式配置中心，支持多种编程语言和框架。它提供了一套完整的配置管理解决方案，可以帮助开发者实现。。。。。。。
image: http://image.ownit.top/4kdongman/17.jpg
tags:
- Java
- spring
- boot
- java-consul
- consul
title: SpringBoot集成Apollo和自动注册Consul
---

<!--more-->

本文将介绍如何在 Spring Boot 中集成阿波罗（Apollo）和 Consul，并使用 Apollo 和 Consul 实现配置管理和服务注册与发现的功能。

# 1\. 什么是阿波罗

阿波罗是携程开源的分布式配置中心，支持多种编程语言和框架。它提供了一套完整的配置管理解决方案，可以帮助开发者实现配置管理、版本控制、灰度发布等功能。

Apollo（阿波罗）是携程框架部门研发的分布式配置中心，能够集中化管理应用不同环境、不同集群的配置，配置修改后能够实时推送到应用端，并且具备规范的权限、流程治理等特性，适用于微服务配置管理场景。服务端基于 Spring Boot 和 Spring Cloud 开发，打包后可以直接运行，不需要额外安装 Tomcat 等应用容器。

Apollo 支持 4 个维度管理 Key-Value 格式的配置：

1.  application \(应用\)
2.  environment \(环境\)
3.  cluster \(集群\)
4.  namespace \(命名空间 Namespace 是配置项的集合，类似于一个配置文件的概念\)

![](http://image.ownit.top/csdn/256a3b00b422c88626e98bc63efa701f.jpeg)

上图是Apollo配置中心中一个项目的配置首页

- 在页面左上方的环境列表模块展示了所有的环境和集群，用户可以随时切换。
- 页面中央展示了两个namespace\(application和FX.apollo\)的配置信息，默认按照表格模式展示、编辑。用户也可以切换到文本模式，以文件形式查看、编辑。
- 页面上可以方便地进行发布、回滚、灰度、授权、查看更改历史和发布历史等操作。

![](http://image.ownit.top/csdn/25f4be0c80b62161d10eff07ac53df42.jpeg)

## 1.1 集成 Apollo 的原理

Spring Boot 集成阿波罗可以通过引入 `apollo-client` 客户端库，并在 Spring Boot 应用程序中配置连接信息和获取配置信息来实现。具体流程如下：

1.  Spring Boot 应用程序启动时，先加载 `bootstrap.yml` 或者 `bootstrap.properties` 文件中的配置信息。

2.  在 `bootstrap.yml` 或者 `bootstrap.properties` 中配置阿波罗的连接信息（例如，阿波罗的地址、应用程序名称等）。

3.  在 Spring Boot 应用程序中注入 `@Value` 注解中指定的阿波罗配置项的值，即可使用阿波罗管理的配置信息。

4.  如果阿波罗的配置信息发生改变，Spring Boot 应用程序会自动从阿波罗更新最新的配置信息，并重新加载应用程序的配置。

## 1.2. 集成 Apollo 的优势

集成阿波罗可以带来以下优势：

1.  管理多个环境的配置：阿波罗提供了环境切换和灰度发布的功能，可以轻松管理多个环境（例如，开发环境、测试环境、生产环境等）的配置信息。

2.  实时更新配置：阿波罗支持实时更新配置信息，可以在不重启应用程序的情况下动态更新配置信息。

3.  版本控制：阿波罗提供了版本控制的功能，可以记录每个配置项的历史版本，方便回滚和恢复数据。

4.  集成多种框架：阿波罗支持多种编程语言和框架，可以轻松集成到各种应用程序中。

# 2、SpringBoot实战集成Apollo

![](http://image.ownit.top/csdn/fcbacc65f870473e9afdc9cd95181583.png)

 

## 1、引入依赖

```java
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.4</version>
        <relativePath/>
    </parent>

    <groupId>com.springboot.demo</groupId>
    <artifactId>web-demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>web-demo</name>
    <description>web-demo</description>
    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Finchley.RELEASE</spring-cloud.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>


        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.ctrip.framework.apollo</groupId>
            <artifactId>apollo-client</artifactId>
            <version>1.5.1</version>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>2020.0.3</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

## 2、增加配置文件

```java
apollo:
  bootstrap:
    enabled: true
    eagerLoad:
      enabled: true
    namespaces: application,tech.java.consul,tech.java.logback
```

## 3、Apollo配置（公用配置，引用）

![](http://image.ownit.top/csdn/d0d94716de2d47919f092b044f20507c.png)

 

```bash
spring.cloud.consul.host = localhost
spring.cloud.consul.port = 8500
spring.cloud.consul.discovery.prefer-ip-address = true
spring.cloud.consul.discovery.instance-id = ${spring.application.name}-${POD_IP:localhost}-${server.port}
consul.datacenter = uat
spring.cloud.consul.discovery.healthCheckPath = ${management.context-path}/health
consul.cluster = uat
management.context-path = /actuator
consul.version = 1.5.3




log.pattern = %d{yyyy-MM-dd HH:mm:ss.SSS} %level | [%t] %logger{36} [%L] | %msg%n
log.dir = /app/logs/app
```

##  4、Apollo项目配置

上面为公共的配置引用，可以被多个项目使用

接下来创建一个单独的Apollo项目。

创建一个单独的 Apollo 项目可以分为以下几个步骤：

1.  登录阿波罗控制台：在浏览器中输入 `https://config.xxx.com` 地址，使用阿波罗管理员账号登录阿波罗控制台。

2.  创建新项目：在阿波罗控制台中，点击左侧导航栏中的“AppList”，然后点击“Create App”按钮，在弹出的对话框中填写应用程序名称、所属集群、所属命名空间等信息，并点击“Create”按钮创建新项目。

3.  添加配置项：进入新创建的项目页面后，点击右侧的“Namespace List”标签页，然后选择需要添加配置项的命名空间。在命名空间页面中，点击“Add Item”按钮，填写配置项的 Key 和 Value，并选择该配置项所属的环境（如 dev、test、prod 等）和版本号。

4.  下载客户端库：在阿波罗控制台中，点击右上角的“Portal”菜单，进入开发者门户网站。在网站中，选择对应的编程语言和框架，然后下载对应的客户端库（例如，Java + Spring Boot 应用程序需要下载 `apollo-client` 客户端库）。

  5.  集成客户端库：将下载好的客户端库引入应用程序的依赖中，然后在应用程序中添加连接阿波罗的配置信息，并使用客户端库从阿波罗获取配置信息。例如，在 Spring Boot 应用程序中，可以在 `bootstrap.yml` 文件中添加以下配置信息：

```java
yaml
spring:
  application:
    name: your-application-name
  profiles:
    active: dev
apollo:
  meta: http://apollo-config-server-url
  bootstrap:
    enabled: true
```

其中，`your-application-name` 是应用程序的名称，`dev` 是配置环境的名称。`http://apollo-config-server-url` 是阿波罗的配置服务 URL。

        6.启动应用程序：将集成了 Apollo 的应用程序打包并启动，通过日志和控制台输出可以查看到应用程序从阿波罗获取配置信息的情况。

以上就是创建一个单独的 Apollo 项目的流程，需要注意的是在实际应用中还需根据具体情况进行调整和优化。

![](http://image.ownit.top/csdn/e78ad2f8ded249b9806f4c2d422bc5b6.png)

 

```bash

name = qqqqqqqqqqqqqqqqqqqqqqqqqqqqq

server.port = 8081
spring.application.name = fqdemo4
spring.profiles.active = uat

spring.cloud.consul.host = 192.168.102.20
spring.cloud.consul.port = 8500
spring.cloud.enabled = true
spring.cloud.consul.discovery.enabled = true
spring.cloud.consul.discovery.hostname = 127.0.0.1
spring.cloud.consul.discovery.register = true
spring.cloud.consul.discovery.deregister = true
spring.cloud.consul.discovery.prefer-ip-address = true
spring.cloud.consul.discovery.instance-id = ${spring.application.name}
spring.cloud.consul.discovery.service-name = ${spring.application.name}
spring.cloud.consul.discovery.health-check-url = http://${spring.cloud.consul.discovery.hostname}:${server.port}/
```

## 5、SpringBoot代码

### WebDemoApplication 启动类

```java
package com.springboot.demo.webdemo;

import com.ctrip.framework.apollo.spring.annotation.EnableApolloConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
@EnableDiscoveryClient
@EnableApolloConfig
public class WebDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(WebDemoApplication.class, args);
    }

    #apollo的变量获取
    @GetMapping("/")
    @Value("${name}")
    public String hello(@RequestParam(value = "name", defaultValue = "${name}") String name) {
        return String.format("Hello %s!", name);
    }

}
```

### HelloWorldController类

```java
package com.springboot.demo.webdemo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;

@RestController
@RequestMapping("/hello")
public class HelloWorldController {
    @GetMapping
    public String hello(){
        return "hello SpringBoot 搭建成功啦";
    }

}



```

### EmployeeController 类

```java
package com.springboot.demo.webdemo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;

@RestController
@RequestMapping("/employee")
public class EmployeeController {

    @GetMapping
    public HashMap<String, String> index(){
        HashMap<String, String> hashmap = new HashMap<String, String>();
        hashmap.put("姓名", "王二");
        hashmap.put("年龄", "27");
        hashmap.put("工龄", "6");

        return hashmap;
    }
}
```

![](http://image.ownit.top/csdn/083549268e9a485e9117c8d0a88d3dc2.png)

##  6、启动测试

```bash
-Dapp.id=156 -Dapollo.meta=http://config.uat.bdata.api.fjf -Denv=uat -javaagent:pinpoint-agent-2.3.3/pinpoint-bootstrap.jar -Dpinpoint.applicationName=fanqiang.uat
```

![](http://image.ownit.top/csdn/be43b11d384c44168b9405544ef3248f.png)

 ![](http://image.ownit.top/csdn/555b2cb1f77a4dc59b5b09b51dbb55d0.png)

### name变量

![](http://image.ownit.top/csdn/b90420edb71145278f6a8a1fb6c7b81b.png)

![](http://image.ownit.top/csdn/f4aa8b2aa46c43af92e03fb1165ae04f.png)

 修改name变量，无需重启项目

 ![](http://image.ownit.top/csdn/1353820e7c2e44938afe7232ec598306.png)

 ![](http://image.ownit.top/csdn/f3c251cbea55437ba85a4a4b51f7a4eb.png)

###  测试两个接口

![](http://image.ownit.top/csdn/f023addc829d42eca688dd290aeb1d42.png)

 ![](http://image.ownit.top/csdn/4868ecdb0c3844d082c732f6cb74aa0c.png)

###  Consul已经自动注册上

![](http://image.ownit.top/csdn/a726b3a09f794795a4542207ff46ffd2.png)

 ![](http://image.ownit.top/csdn/5aeea8fe4a014e04a73153172b940ac7.png)

 

本文介绍了如何在 Spring Boot 中集成阿波罗，并详细说明了其原理和优势。通过使用阿波罗，可以轻松管理多个环境的配置信息，实现配置管理、版本控制、灰度发布等功能。同时，本文还给出了集成阿波罗的最佳实践，希望能够对开发者和运维在实际项目中使用阿波罗提供一些参考和帮助。

 参考文档：

<https://www.cnblogs.com/mrhelloworld/p/apollo1.html>

[spring cloud apollo 配置中心 \- 掘金](https://juejin.cn/post/7051878293783445541 "spring cloud apollo 配置中心 \- 掘金")

[Spring Boot 集成 Apollo 配置中心，真香、真强大！\_51CTO博客\_apollo集成springcloud](https://blog.51cto.com/u_15162069/2897810 "Spring Boot 集成 Apollo 配置中心，真香、真强大！_51CTO博客_apollo集成springcloud")